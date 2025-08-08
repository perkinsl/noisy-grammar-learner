library(reshape) ## to load melt()
library(dplyr)
library(ggplot2)
library(tidyr)
library(lme4)
library(cowplot)
library(Cairo)
library(stringr)

cbPalette <- c("#074C19","#7FD4C3","#7CB0FF","#0C7BDC")
cbPalette2 <- c("#074C19","#7FD4C3","#7CB0FF","#0C7BDC", "#332288", "#B93500","#E66100","#FFC20A","#FFDF56")
cbPalette3 = c("#332288","#0C7BDC","#7CB0FF","#7FD4C3","#FFDF56","#FFC20A")
cbPalette4 = c("#332288","#0C7BDC","#FFC20A","#FFDF56")
cbPalette5 = c("#7CB0FF","#0C7BDC","#332288","#FFC20A")
cbPalette6 = c("#0C7BDC","#332288","#FFC20A","#FFDF56")
cbPaletteBinary <- c("#FFC20A","#0C7BDC")
cbPaletteBinary2 <- c("#0C7BDC","#FFC20A")
cbPaletteBinary3 <- c("#332288","#FFC20A")
cbPaletteTernary <- c("#FFC20A","#0C7BDC","#332288")


data <- read.csv("austin_data.csv")

## Plot bar graphs of regularization simulation, by alpha and forgetting rate
data$run <- as.factor(data$run)
data$alpha <- as.factor(data$alpha)
data$retained <- 1 - data$forgetting
data$datasize <- round(data$retained * 126)
data$retained <- as.factor(data$retained)
data$datasize <- as.factor(data$datasize)
data$prob_bo <- 1 - data$prob_ka

data.summarized <- summarise(group_by(data, alpha, retained, datasize, model), meanka=mean(prob_ka), meanbo=mean(prob_bo),
                                       n = length(prob_ka), sd=sd(prob_ka), se=sd/sqrt(n))

data.summarized$alpha <- factor(data.summarized$alpha, levels = c(0.0001,0.05,0.5,1))
levels(data.summarized$alpha) <- c('0.0001 (strong bias)','0.05 (medium bias)','0.5 (weak bias)','1 (no bias)')

ggplot(filter(data.summarized, model=='Regularization'), aes(x=alpha, y=meanka, fill=retained)) + 
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette3) + 
  scale_y_continuous(name='MAP estimate of \u03b8',limits=c(0,1)) + scale_x_discrete(name='\u03b1') + labs(fill = "Forgetting rate") +
  geom_errorbar(aes(ymin=meanka-se, ymax=meanka+se), width=.2, position=position_dodge(.9)) + 
  geom_hline(yintercept = 0.66666, linetype = "dashed") + theme_bw()

data.summarized$retained <- factor(data.summarized$retained, levels = c(0.02, 0.05, 0.1, 0.2, 0.6, 1))
levels(data.summarized$retained) <- c('2%', '5%', '10%', '20%', '60%', '100%')

ggplot(filter(data.summarized, model=='Regularization', retained != '2%'), aes(x='', y=meanka, fill=alpha)) + facet_grid(~retained) +
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette5) + 
  scale_y_continuous(name="MAP estimate of \u03b8",limits=c(0,1)) + labs(fill = "\u03b1") +
  ggtitle("Percentage of data learned from") +
  geom_errorbar(aes(ymin=meanka-se, ymax=meanka+se), width=.2, position=position_dodge(.9)) + 
  geom_hline(yintercept = 0.66666, linetype = "dashed") + theme_bw() +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  theme(plot.title = element_text(hjust = 0.5,size = 11))

ggsave("plot_austin_regularization.pdf", device = cairo_pdf)

## Noisy grammar posterior plots
data.summarized.long <- gather(data.summarized, grammar, posterior, meanka:meanbo, factor_key=TRUE)
levels(data.summarized.long$grammar) <- c('Gka','Gbo')

ggplot(filter(data.summarized.long, model=='NoisyGrammars',retained != '2%'), aes(x='', y=posterior, fill=grammar)) + facet_grid(~retained) +
  geom_bar(stat="identity", position=position_dodge(1.05),width=0.9) + 
  scale_fill_manual(values=cbPaletteBinary2,labels=c(expression(italic('G')[ka]),expression(italic('G')[bo]))) + 
  scale_y_continuous(name="Posterior probability",limits=c(0,1)) + labs(fill = "Grammar") +
  ggtitle("Percentage of data learned from") +
  geom_errorbar(aes(ymin=posterior-se, ymax=posterior+se), width=.2, position=position_dodge(1.05)) + theme_bw() +
  theme(panel.grid.major.x = element_blank()) + theme_bw() +   
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank()) +
  theme(plot.title = element_text(hjust = 0.5,size = 10)) +
  geom_segment(aes(x = 0.3, xend = 0.95, y = 0.66667, yend = 0.66667),linetype="dashed") +
  geom_segment(aes(x = 1.06, xend = 1.7, y = 0.33333, yend = 0.33333),linetype="dashed")

ggsave("plot_posterior_kabo.pdf", device = cairo_pdf)

## COINS

# plots of Beta distributions
Binv <- function(p, q) {
  exp(lgamma(p+q)-lgamma(p)-lgamma(q))
}

betapdf<- function(p,q,x){
  Binv(p,q) * x**(p-1) * (1-x)**(q-1)
} 

col_grid <- rgb(235, 235, 235, 100, maxColorValue = 255)

ggplot() + xlim(c(0,1)) + 
  geom_function(fun=betapdf, args=list(p=1,q=1), aes(color = "\u03b1 = 1")) +
  geom_function(fun=betapdf, args=list(p=5,q=5), aes(color = "\u03b1 = 5")) +
  geom_function(fun=betapdf, args=list(p=0.5,q=0.5), aes(color = "\u03b1 = 0.5")) +
  geom_function(fun=betapdf, args=list(p=0.05,q=0.05), aes(color = "\u03b1 = 0.05")) +
  scale_y_continuous(name="Probability density") + scale_x_continuous(name="\u03b8") +
  scale_color_manual(values=cbPalette6, name="") + theme_bw() +
  theme(panel.grid = element_line(color = col_grid))
  
ggsave("plot_beta_examples.pdf", device = cairo_pdf)

# plots of likelihoods under hypothesis N-phi=0 and N-phi=6, Bag H
f10 <- function(psi) {
  choose(10,8) * (psi**8) * ((1-psi)**2)
}
f04 <- function(psi) {
  choose(4,2) * (psi**2) * ((1-psi)**2)
}

ggplot() + xlim(c(0,1)) + 
  geom_function(fun=f04, aes(color = "N\u03a6=6")) +
  geom_function(fun=f10, aes(color = "N\u03a6=0")) +
  scale_y_continuous(name="Likelihood",lim=c(0,0.4)) + 
  scale_x_continuous(name=expression('Probability'~italic(psi)~'of heads on any single flip of a'~italic(Psi)~'coin'))+
                       #"Probability \u03C8 of heads on single flip of a \u03A8 coin") +
  scale_color_manual(values=cbPaletteBinary, name="", 
                     labels=c(expression(italic('N'[Phi])~'= 0'), expression(italic('N'[Phi])~'= 6'))) + 
  theme_bw() + theme(panel.grid = element_line(color = col_grid))

ggsave("plot_coins_psi_graph.pdf", device = cairo_pdf)

# likelihood of 8H+2T with n two-headed coins (and 10-n head-tail coins) from Bag H
lh <- function(n) {
  choose(10-n, 8-n) * beta(8-n+1, 3)
}

# likelihood of 8H+2T with n two-headed coins (and 10-n head-tail coins) from Bag T
lt <- function(n) {
  choose(10-n, 2-n) * beta(9, 2-n+1)
}

likelihoods <- data.frame(c(0:10))
colnames(likelihoods) <- c("nPhi")
likelihoods$BagH <- lh(likelihoods$nPhi)
likelihoods$BagT <- lt(likelihoods$nPhi)
likelihoods.long <- gather(likelihoods, bag, likelihood, BagH:BagT, factor_key=TRUE)
likelihoods.long$nPhi <- factor(likelihoods.long$nPhi)
levels(likelihoods.long$bag) <- c(expression(italic('G')[ka]),expression(italic('G')[bo]))

ggplot(likelihoods.long, aes(x=nPhi, y=likelihood, fill=bag)) + 
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPaletteBinary2) + 
  scale_y_continuous(name="Likelihood") + scale_x_discrete(name="Number of flips of \u03a6 coins") +
  labs(fill = NULL) + theme_bw() + theme(axis.ticks.x = element_blank(), panel.grid.major.x = element_blank())

ggsave("plot_coins_columngraph.pdf", device = cairo_pdf)

## Renaming legends to be G_ka and G_bo
likelihoods <- data.frame(c(0:10))
colnames(likelihoods) <- c("nPhi")
likelihoods$Gka <- lh(likelihoods$nPhi)
likelihoods$Gbo <- lt(likelihoods$nPhi)
likelihoods.long <- gather(likelihoods, bag, likelihood, Gka:Gbo, factor_key=TRUE)
likelihoods.long$nPhi <- factor(likelihoods.long$nPhi)
levels(likelihoods.long$bag) <- c("Gka","Gbo")

ggplot(likelihoods.long, aes(x=nPhi, y=likelihood, fill=bag)) + 
  geom_bar(stat="identity", position=position_dodge()) + 
  scale_fill_manual(values=cbPaletteBinary2,labels=c(expression(italic('G')[ka]),expression(italic('G')[bo]))) + 
  scale_y_continuous(name="Likelihood") + scale_x_discrete(name="Number of flips of \u03a6 coins") +
  labs(fill = NULL) + theme_bw() + theme(axis.ticks.x = element_blank(), panel.grid.major.x = element_blank()) +
  theme(axis.title=element_text(size=14), legend.text=element_text(size=12))

ggsave("plot_coinskabo_columngraph.pdf", device = cairo_pdf)


## barplot of posteriors
posteriors <- data.frame(c("Bag H", "Bag T"))
colnames(posteriors) <- c("bag")
posteriors$prob <- c(0.834, 0.166)

ggplot(posteriors, aes(x=bag, y=prob, fill=bag)) + 
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPaletteBinary2) + 
  scale_y_continuous(name="Posterior probability") + 
  theme_bw() + theme(legend.position = "none", axis.title.x=element_blank(), panel.grid.major.x = element_blank())

ggsave("plot_posterior_bags.pdf", device = cairo_pdf)


