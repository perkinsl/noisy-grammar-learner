library(reshape) ## to load melt()
library(dplyr)
library(ggplot2)
library(tidyr)
library(lme4)
library(cowplot)

cbPalette <- c("#074C19","#7FD4C3","#7CB0FF","#0C7BDC")
cbPalette2 <- c("#074C19","#7FD4C3","#7CB0FF","#0C7BDC", "#332288", "#B93500","#E66100","#FFC20A","#FFDF56")
cbPalette3 = c("#332288","#0C7BDC","#7CB0FF","#7FD4C3","#FFDF56","#FFC20A")
cbPalette4 = c("#332288","#0C7BDC","#FFC20A","#FFDF56")
cbPalette5 = c("#7CB0FF","#0C7BDC","#332288","#FFC20A")
cbPalette6 = c("#0C7BDC","#332288","#FFC20A","#FFDF56")
cbPalette7 = c("#0C7BDC","#332288","#FFC20A","#FFDF56","#7FD4C3")
cbPalette8 = c("#332288","#FFC20A","#7FD4C3","#0C7BDC","#0C7BDC")
cbPaletteBinary <- c("#FFC20A","#0C7BDC")
cbPaletteBinary2 <- c("#0C7BDC","#FFC20A")
cbPaletteTernary <- c("#FFC20A","#0C7BDC","#332288")
cbPaletteTernary2 <- c("#332288","#3EBAA2","#FFC20A")
cbPaletteTernary3 <- c("#FFC20A","#332288","#3EBAA2")


## PREPARING DATA
## CATEGORICAL LEARNERS

data.8grammars <- read.csv("8grammars_journ50k.csv")
data.8grammars$run <- as.factor(data.8grammars$run)
data.8grammars.long <- reshape(data.8grammars, 
                               varying = c("SOV", "SVO", "OVS", "VOS",
                                           "SV", "VS", "OV", "VO"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS",
                                         "SV", "VS", "OV", "VO"),
                               direction = "long",
                               new.row.names = 1:10000)

# converting 8-grammar run into 4-grammar probabilities by renormalizing
data.4grammars <- subset(data.8grammars, select = c("model","run","language"))
data.4grammars$SVO <- data.8grammars$SVO / (data.8grammars$SVO + data.8grammars$OVS + data.8grammars$SOV + data.8grammars$VOS)
data.4grammars$SOV <- data.8grammars$SOV / (data.8grammars$SVO + data.8grammars$OVS + data.8grammars$SOV + data.8grammars$VOS)
data.4grammars$OVS <- data.8grammars$OVS / (data.8grammars$SVO + data.8grammars$OVS + data.8grammars$SOV + data.8grammars$VOS)
data.4grammars$VOS <- data.8grammars$VOS / (data.8grammars$SVO + data.8grammars$OVS + data.8grammars$SOV + data.8grammars$VOS)
data.4grammars.long <- reshape(data.4grammars, 
                           varying = c("SOV", "SVO", "OVS", "VOS"), 
                           v.names = "proportion",
                           timevar = "grammar",
                           times = c("SOV", "SVO", "OVS", "VOS"),
                           direction = "long",
                           new.row.names = 1:10000)

data.9grammars <- read.csv("9grammars_journ50k.csv")
data.9grammars$run <- as.factor(data.9grammars$run)
data.9grammars.long <- reshape(data.9grammars, 
                               varying = c("SOV", "SVO", "OVS", "VOS",
                                           "SV", "VS", "OV", "VO", "FREE"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS",
                                         "SV", "VS", "OV", "VO", "FREE"),
                               direction = "long",
                               new.row.names = 1:10000)
## smaller datasets
data.8grammars10 <- read.csv("8grammars10.csv")
data.8grammars10$run <- as.factor(data.8grammars10$run)
data.8grammars10.long <- reshape(data.8grammars10, 
                               varying = c("SOV", "SVO", "OVS", "VOS",
                                           "SV", "VS", "OV", "VO"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS",
                                         "SV", "VS", "OV", "VO"),
                               direction = "long",
                               new.row.names = 1:10000)

data.4grammars10 <- subset(data.8grammars10, select = c("model","run","language"))
data.4grammars10$SVO <- data.8grammars10$SVO / (data.8grammars10$SVO + data.8grammars10$OVS + data.8grammars10$SOV + data.8grammars10$VOS)
data.4grammars10$SOV <- data.8grammars10$SOV / (data.8grammars10$SVO + data.8grammars10$OVS + data.8grammars10$SOV + data.8grammars10$VOS)
data.4grammars10$OVS <- data.8grammars10$OVS / (data.8grammars10$SVO + data.8grammars10$OVS + data.8grammars10$SOV + data.8grammars10$VOS)
data.4grammars10$VOS <- data.8grammars10$VOS / (data.8grammars10$SVO + data.8grammars10$OVS + data.8grammars10$SOV + data.8grammars10$VOS)
data.4grammars10.long <- reshape(data.4grammars10, 
                               varying = c("SOV", "SVO", "OVS", "VOS"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS"),
                               direction = "long",
                               new.row.names = 1:10000)

data.8grammars20 <- read.csv("8grammars20.csv")
data.8grammars20$run <- as.factor(data.8grammars20$run)
data.8grammars20.long <- reshape(data.8grammars20, 
                                 varying = c("SOV", "SVO", "OVS", "VOS",
                                             "SV", "VS", "OV", "VO"), 
                                 v.names = "proportion",
                                 timevar = "grammar",
                                 times = c("SOV", "SVO", "OVS", "VOS",
                                           "SV", "VS", "OV", "VO"),
                                 direction = "long",
                                 new.row.names = 1:10000)

data.4grammars20 <- subset(data.8grammars20, select = c("model","run","language"))
data.4grammars20$SVO <- data.8grammars20$SVO / (data.8grammars20$SVO + data.8grammars20$OVS + data.8grammars20$SOV + data.8grammars20$VOS)
data.4grammars20$SOV <- data.8grammars20$SOV / (data.8grammars20$SVO + data.8grammars20$OVS + data.8grammars20$SOV + data.8grammars20$VOS)
data.4grammars20$OVS <- data.8grammars20$OVS / (data.8grammars20$SVO + data.8grammars20$OVS + data.8grammars20$SOV + data.8grammars20$VOS)
data.4grammars20$VOS <- data.8grammars20$VOS / (data.8grammars20$SVO + data.8grammars20$OVS + data.8grammars20$SOV + data.8grammars20$VOS)
data.4grammars20.long <- reshape(data.4grammars20, 
                                 varying = c("SOV", "SVO", "OVS", "VOS"), 
                                 v.names = "proportion",
                                 timevar = "grammar",
                                 times = c("SOV", "SVO", "OVS", "VOS"),
                                 direction = "long",
                                 new.row.names = 1:10000)

data.8grammars30 <- read.csv("8grammars30.csv")
data.8grammars30$run <- as.factor(data.8grammars30$run)
data.8grammars30.long <- reshape(data.8grammars30, 
                                 varying = c("SOV", "SVO", "OVS", "VOS",
                                             "SV", "VS", "OV", "VO"), 
                                 v.names = "proportion",
                                 timevar = "grammar",
                                 times = c("SOV", "SVO", "OVS", "VOS",
                                           "SV", "VS", "OV", "VO"),
                                 direction = "long",
                                 new.row.names = 1:10000)

data.4grammars30 <- subset(data.8grammars30, select = c("model","run","language"))
data.4grammars30$SVO <- data.8grammars30$SVO / (data.8grammars30$SVO + data.8grammars30$OVS + data.8grammars30$SOV + data.8grammars30$VOS)
data.4grammars30$SOV <- data.8grammars30$SOV / (data.8grammars30$SVO + data.8grammars30$OVS + data.8grammars30$SOV + data.8grammars30$VOS)
data.4grammars30$OVS <- data.8grammars30$OVS / (data.8grammars30$SVO + data.8grammars30$OVS + data.8grammars30$SOV + data.8grammars30$VOS)
data.4grammars30$VOS <- data.8grammars30$VOS / (data.8grammars30$SVO + data.8grammars30$OVS + data.8grammars30$SOV + data.8grammars30$VOS)
data.4grammars30.long <- reshape(data.4grammars30, 
                                 varying = c("SOV", "SVO", "OVS", "VOS"), 
                                 v.names = "proportion",
                                 timevar = "grammar",
                                 times = c("SOV", "SVO", "OVS", "VOS"),
                                 direction = "long",
                                 new.row.names = 1:10000)

## subject-drop grammars
data.9grammars.subjdrop <- read.csv("9grammars_subjdrop.csv")
data.9grammars.subjdrop$run <- as.factor(data.9grammars.subjdrop$run)
data.9grammars.subjdrop.long <- reshape(data.9grammars.subjdrop, 
                               varying = c("SOV", "SVO", "OVS", "VOS",
                                           "SV", "VS", "OV", "VO", "FREE"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS",
                                         "SV", "VS", "OV", "VO", "FREE"),
                               direction = "long",
                               new.row.names = 1:10000)

# converting 9-grammar run into 5-grammar probabilities by renormalizing
data.9grammars.Bayes <- subset(data.9grammars, model == "Bayesian")
data.5grammars <- subset(data.9grammars.Bayes, select = c("model","run","language"))
data.5grammars$SVO <- data.9grammars.Bayes$SVO / (data.9grammars.Bayes$SVO + data.9grammars.Bayes$OVS + data.9grammars.Bayes$SOV + data.9grammars.Bayes$VOS + data.9grammars.Bayes$FREE)
data.5grammars$SOV <- data.9grammars.Bayes$SOV / (data.9grammars.Bayes$SVO + data.9grammars.Bayes$OVS + data.9grammars.Bayes$SOV + data.9grammars.Bayes$VOS + data.9grammars.Bayes$FREE)
data.5grammars$OVS <- data.9grammars.Bayes$OVS / (data.9grammars.Bayes$SVO + data.9grammars.Bayes$OVS + data.9grammars.Bayes$SOV + data.9grammars.Bayes$VOS + data.9grammars.Bayes$FREE)
data.5grammars$VOS <- data.9grammars.Bayes$VOS / (data.9grammars.Bayes$SVO + data.9grammars.Bayes$OVS + data.9grammars.Bayes$SOV + data.9grammars.Bayes$VOS + data.9grammars.Bayes$FREE)
data.5grammars$FREE <- data.9grammars.Bayes$FREE / (data.9grammars.Bayes$SVO + data.9grammars.Bayes$OVS + data.9grammars.Bayes$SOV + data.9grammars.Bayes$VOS + data.9grammars.Bayes$FREE)
data.5grammars <- rbind(data.5grammars, subset(data.9grammars, model == "Data Coverage", select = c("model","run","language","SVO","SOV","OVS","VOS","FREE")))

data.5grammars.long <- reshape(data.5grammars, 
                               varying = c("SOV", "SVO", "OVS", "VOS","FREE"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS","FREE"),
                               direction = "long",
                               new.row.names = 1:10000)

# converting 9-subjdrop grammar run into 4-grammar probabilities by renormalizing
data.9grammars.subjdrop.Bayes <- subset(data.9grammars.subjdrop, model == "Bayesian")
data.4grammars.subjdrop <- subset(data.9grammars.subjdrop.Bayes, select = c("model","run","language"))
data.4grammars.subjdrop$SVO <- data.9grammars.subjdrop.Bayes$SVO / (data.9grammars.subjdrop.Bayes$SVO + data.9grammars.subjdrop.Bayes$OVS + data.9grammars.subjdrop.Bayes$SOV + data.9grammars.subjdrop.Bayes$VOS + data.9grammars.subjdrop.Bayes$FREE)
data.4grammars.subjdrop$SOV <- data.9grammars.subjdrop.Bayes$SOV / (data.9grammars.subjdrop.Bayes$SVO + data.9grammars.subjdrop.Bayes$OVS + data.9grammars.subjdrop.Bayes$SOV + data.9grammars.subjdrop.Bayes$VOS + data.9grammars.subjdrop.Bayes$FREE)
data.4grammars.subjdrop$OVS <- data.9grammars.subjdrop.Bayes$OVS / (data.9grammars.subjdrop.Bayes$SVO + data.9grammars.subjdrop.Bayes$OVS + data.9grammars.subjdrop.Bayes$SOV + data.9grammars.subjdrop.Bayes$VOS + data.9grammars.subjdrop.Bayes$FREE)
data.4grammars.subjdrop$VOS <- data.9grammars.subjdrop.Bayes$VOS / (data.9grammars.subjdrop.Bayes$SVO + data.9grammars.subjdrop.Bayes$OVS + data.9grammars.subjdrop.Bayes$SOV + data.9grammars.subjdrop.Bayes$VOS + data.9grammars.subjdrop.Bayes$FREE)

data.4grammars.subjdrop.long <- reshape(data.4grammars.subjdrop, 
                               varying = c("SOV", "SVO", "OVS", "VOS"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV", "SVO", "OVS", "VOS"),
                               direction = "long",
                               new.row.names = 1:10000)


## FULLY-FLEXIBLE LEARNERS
data.alt <- read.csv("flexlearner_journ50k.csv")
data.alt$run <- as.factor(data.alt$run)
data.alt$dataset <- "50 strings"

## subset runs
data.alt.10 <- read.csv("flexlearner10.csv")
data.alt.10$run <- as.factor(data.alt.10$run)
data.alt.10$dataset <- "10 strings"

data.alt.20 <- read.csv("flexlearner20.csv")
data.alt.20$run <- as.factor(data.alt.20$run)
data.alt.20$dataset <- "20 strings"

data.alt.30 <- read.csv("flexlearner30.csv")
data.alt.30$run <- as.factor(data.alt.30$run)
data.alt.30$dataset <- "30 strings"

data.alt.combined <- rbind(data.alt, data.alt.10, data.alt.20, data.alt.30)

## CASE-MARKING LEARNERS
data.8grammars.case <- read.csv("casemarking_8grammars_journ50k.csv")
data.8grammars.case$run <- as.factor(data.8grammars.case$run)
data.8grammars.case.long <- reshape(data.8grammars.case, 
                               varying = c("SOV_12", "SOV_21", "SVO_12", "SVO_21",
                                           "OVS_12", "OVS_21", "VOS_12", "VOS_21"), 
                               v.names = "proportion",
                               timevar = "grammar",
                               times = c("SOV_12", "SOV_21", "SVO_12", "SVO_21",
                                         "OVS_12", "OVS_21", "VOS_12", "VOS_21"),
                               direction = "long",
                               new.row.names = 1:10000)

data.2grammars.case <- read.csv("casemarking_2grammars_journ50k.csv")
data.2grammars.case$run <- as.factor(data.2grammars.case$run)
data.2grammars.case.long <- reshape(data.2grammars.case, 
                                    varying = c("SOV_12", "SOV_21"), 
                                    v.names = "proportion",
                                    timevar = "grammar",
                                    times = c("SOV_12", "SOV_21"),
                                    direction = "long",
                                    new.row.names = 1:10000)

data.alt.case <- read.csv("flexcasemarking_journ50k.csv")
data.alt.case$run <- as.factor(data.alt.case$run)
data.alt.case.bu <- read.csv("flexcasemarking_bottomup.csv")
data.alt.case.bu$run <- as.factor(data.alt.case.bu$run)

data.alt.SOV <- read.csv("flexcaseSOV_journ50k.csv")
data.alt.SOV$run <- as.factor(data.alt.SOV$run)
data.alt.SOV.bu <- read.csv("flexcaseSOV_bottomup.csv")
data.alt.SOV.bu$run <- as.factor(data.alt.SOV.bu$run)

## CATEGORICAL GRAMMAR ANALYSIS
# 4 GRAMMARS
data.4grammars.summarized <- summarise(group_by(data.4grammars.long, grammar, language, model), mean=mean(proportion), 
                                       n = length(proportion), sd=sd(proportion), se=sd/sqrt(n))

data.4grammars.summarized$grammar <- factor(data.4grammars.summarized$grammar, levels = c('SVO','SOV','OVS','VOS'))
data.4grammars.summarized$model <- factor(data.4grammars.summarized$model, levels = c('Data Coverage', 'Bayesian')) 
levels(data.4grammars.summarized$model) <- c('Prop. data covered', 'Posterior probability')

ggplot(filter(data.4grammars.summarized, model=='Posterior probability'), aes(x=grammar, y=mean, fill=grammar)) + facet_grid(.~language) +
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette) +
  scale_y_continuous(name='Mean posterior probability') + scale_x_discrete(name='') + labs(fill = "Grammar") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(legend.position="none") + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank())

## analysis
Eng.SOV <- t.test(filter(data.4grammars, language == 'English')$SVO, filter(data.4grammars, language == 'English')$SOV)
Eng.OVS <- t.test(filter(data.4grammars, language == 'English')$SVO, filter(data.4grammars, language == 'English')$OVS)
Eng.VOS <- t.test(filter(data.4grammars, language == 'English')$SVO, filter(data.4grammars, language == 'English')$VOS)

Fr.SOV <- t.test(filter(data.4grammars, language == 'French')$SVO, filter(data.4grammars, language == 'French')$SOV)
Fr.OVS <- t.test(filter(data.4grammars, language == 'French')$SVO, filter(data.4grammars, language == 'French')$OVS)
Fr.VOS <- t.test(filter(data.4grammars, language == 'French')$SVO, filter(data.4grammars, language == 'French')$VOS)

J.SVO <- t.test(filter(data.4grammars, language == 'Japanese')$SOV, filter(data.4grammars, language == 'Japanese')$SVO)
J.OVS <- t.test(filter(data.4grammars, language == 'Japanese')$SOV, filter(data.4grammars, language == 'Japanese')$OVS)
J.VOS <- t.test(filter(data.4grammars, language == 'Japanese')$SOV, filter(data.4grammars, language == 'Japanese')$VOS)


Eng.prop.SVO <- mean(filter(data.4grammars, language == 'English')$SVO)
Eng.prop.SOV <- mean(filter(data.4grammars, language == 'English')$SOV)
Eng.prop.OVS <- mean(filter(data.4grammars, language == 'English')$OVS)
Eng.prop.VOS <- mean(filter(data.4grammars, language == 'English')$VOS)

Fr.prop.SVO <- mean(filter(data.4grammars, language == 'French')$SVO)
Fr.prop.SOV <- mean(filter(data.4grammars, language == 'French')$SOV)
Fr.prop.OVS <- mean(filter(data.4grammars, language == 'French')$OVS)
Fr.prop.VOS <- mean(filter(data.4grammars, language == 'French')$VOS)

## smaller datasets
## 10-, 20-, and 30-sentence runs combined
data.4grammars.summarized$dataset <- "50 strings"
data.4grammars10.summarized <- summarise(group_by(data.4grammars10.long, grammar, language, model), mean=mean(proportion, na.rm = TRUE), 
                                         n = length(proportion), sd=sd(proportion, na.rm = TRUE), se=sd/sqrt(n))
data.4grammars10.summarized$grammar <- factor(data.4grammars10.summarized$grammar, levels = c('SVO','SOV','OVS','VOS'))
data.4grammars10.summarized$dataset <- "10 strings"
data.4grammars20.summarized <- summarise(group_by(data.4grammars20.long, grammar, language, model), mean=mean(proportion, na.rm = TRUE), 
                                         n = length(proportion), sd=sd(proportion, na.rm = TRUE), se=sd/sqrt(n))
data.4grammars20.summarized$grammar <- factor(data.4grammars20.summarized$grammar, levels = c('SVO','SOV','OVS','VOS'))
data.4grammars20.summarized$dataset <- "20 strings"
data.4grammars30.summarized <- summarise(group_by(data.4grammars30.long, grammar, language, model), mean=mean(proportion, na.rm = TRUE), 
                                         n = length(proportion), sd=sd(proportion, na.rm = TRUE), se=sd/sqrt(n))
data.4grammars30.summarized$grammar <- factor(data.4grammars30.summarized$grammar, levels = c('SVO','SOV','OVS','VOS'))
data.4grammars30.summarized$dataset <- "30 strings"
data.4grammars.combined <- rbind(filter(data.4grammars.summarized,model=="Bayesian"), data.4grammars10.summarized, data.4grammars20.summarized, data.4grammars30.summarized)
data.4grammars.combined$grammar <- factor(data.4grammars.combined$grammar, levels = c('SVO','SOV','OVS','VOS'))

ggplot(data.4grammars.combined, aes(x=grammar, y=mean, fill=grammar)) + facet_grid(dataset~language) +
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette6) +
  scale_y_continuous(name='Mean posterior probability') + scale_x_discrete(name='') + labs(fill = "Grammar") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(legend.position="none") + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank())

## 5 GRAMMARS
data.5grammars.summarized <- summarise(group_by(data.5grammars.long, grammar, language, model), mean=mean(proportion, na.rm = TRUE), 
                                       n = length(proportion), sd=sd(proportion, na.rm=TRUE), se=sd/sqrt(n))

data.5grammars.summarized$grammar <- factor(data.5grammars.summarized$grammar, levels = c('SVO','SOV','OVS','VOS','FREE')) 
data.5grammars.summarized$model <- factor(data.5grammars.summarized$model, levels = c('Data Coverage', 'Bayesian')) 
levels(data.5grammars.summarized$model) <- c('Prop. data covered', 'Posterior probability')

ggplot(data.5grammars.summarized, aes(x=grammar, y=mean, fill=grammar)) + 
  facet_grid(model~language, scales = "free_y", ) +
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette7) +
  scale_y_continuous(name='') + scale_x_discrete(name='') + labs(fill = "Grammar") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(legend.position="none") + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank())

## analysis
Eng.SOV <- t.test(filter(data.5grammars, language == 'English')$SVO, filter(data.5grammars, language == 'English')$SOV)
Eng.OVS <- t.test(filter(data.5grammars, language == 'English')$SVO, filter(data.5grammars, language == 'English')$OVS)
Eng.VOS <- t.test(filter(data.5grammars, language == 'English')$SVO, filter(data.5grammars, language == 'English')$VOS)
Eng.FREE <- t.test(filter(data.5grammars, language == 'English')$SVO, filter(data.5grammars, language == 'English')$FREE)

Fr.SOV <- t.test(filter(data.5grammars, language == 'French')$SVO, filter(data.5grammars, language == 'French')$SOV)
Fr.OVS <- t.test(filter(data.5grammars, language == 'French')$SVO, filter(data.5grammars, language == 'French')$OVS)
Fr.VOS <- t.test(filter(data.5grammars, language == 'French')$SVO, filter(data.5grammars, language == 'French')$VOS)
Fr.FREE <- t.test(filter(data.5grammars, language == 'French')$SVO, filter(data.5grammars, language == 'French')$FREE)

J.SVO <- t.test(filter(data.5grammars, language == 'Japanese')$SOV, filter(data.5grammars, language == 'Japanese')$SVO)
J.OVS <- t.test(filter(data.5grammars, language == 'Japanese')$SOV, filter(data.5grammars, language == 'Japanese')$OVS)
J.VOS <- t.test(filter(data.5grammars, language == 'Japanese')$SOV, filter(data.5grammars, language == 'Japanese')$VOS)
J.FREE <- t.test(filter(data.5grammars, language == 'Japanese')$SOV, filter(data.5grammars, language == 'Japanese')$FREE)

# 4 GRAMMARS WITHOUT OBLIGATORY SUBJECTS
data.4grammars.subjdrop.summarized <- summarise(group_by(data.4grammars.subjdrop.long, grammar, language), mean=mean(proportion), 
                                       n = length(proportion), sd=sd(proportion), se=sd/sqrt(n))

data.4grammars.subjdrop.summarized$grammar <- factor(data.4grammars.subjdrop.summarized$grammar, levels = c('SVO','SOV','OVS','VOS'))

ggplot(data.4grammars.subjdrop.summarized, aes(x=grammar, y=mean, fill=grammar)) + facet_grid(.~language) +
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette6) +
  scale_y_continuous(name='Posterior probability') + scale_x_discrete(name='') + labs(fill = "Grammar") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(legend.position="none") + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank())

# analyses
Eng.SOV <- t.test(filter(data.4grammars.subjdrop, language == 'English')$SVO, filter(data.4grammars.subjdrop, language == 'English')$SOV)
Eng.OVS <- t.test(filter(data.4grammars.subjdrop, language == 'English')$SVO, filter(data.4grammars.subjdrop, language == 'English')$OVS)
Eng.VOS <- t.test(filter(data.4grammars.subjdrop, language == 'English')$SVO, filter(data.4grammars.subjdrop, language == 'English')$VOS)

Fr.SVO <- t.test(filter(data.4grammars.subjdrop, language == 'French')$SOV, filter(data.4grammars.subjdrop, language == 'French')$SVO)
Fr.OVS <- t.test(filter(data.4grammars.subjdrop, language == 'French')$SOV, filter(data.4grammars.subjdrop, language == 'French')$OVS)
Fr.VOS <- t.test(filter(data.4grammars.subjdrop, language == 'French')$SOV, filter(data.4grammars.subjdrop, language == 'French')$VOS)
Fr.SVO.OVS <- t.test(filter(data.4grammars.subjdrop, language == 'French')$SVO, filter(data.4grammars.subjdrop, language == 'French')$OVS)

J.SVO <- t.test(filter(data.4grammars.subjdrop, language == 'Japanese')$SOV, filter(data.4grammars.subjdrop, language == 'Japanese')$SVO)
J.OVS <- t.test(filter(data.4grammars.subjdrop, language == 'Japanese')$SOV, filter(data.4grammars.subjdrop, language == 'Japanese')$OVS)
J.VOS <- t.test(filter(data.4grammars.subjdrop, language == 'Japanese')$SOV, filter(data.4grammars.subjdrop, language == 'Japanese')$VOS)


# CASE MARKING
## SOV only
data.2grammars.case.summarized <- summarise(group_by(data.2grammars.case.long, language, grammar, model), mean=mean(proportion, na.rm = TRUE), 
                                            n = length(proportion), sd=sd(proportion, na.rm=TRUE), se=sd/sqrt(n))

data.2grammars.case.summarized$grammar <- factor(data.2grammars.case.summarized$grammar, levels = c('SOV_12','SOV_21')) 
data.2grammars.case.summarized$model <- factor(data.2grammars.case.summarized$model, levels = c('Data Coverage', 'Bayesian')) 
levels(data.2grammars.case.summarized$model) <- c('Prop. data covered', 'Posterior probability')

data.2grammars.case.summarized$wordorder <- 'SOV'
data.2grammars.case.summarized$case <- 'np-ga: Subj, np-o: Obj'
data.2grammars.case.summarized$case[which((data.2grammars.case.summarized$grammar == 'SOV_21'))] <- 'np-ga: Obj, np-o: Subj'
data.2grammars.case.summarized$case <- factor(data.2grammars.case.summarized$case, levels = c('np-ga: Subj, np-o: Obj','np-ga: Obj, np-o: Subj')) 
data.2grammars.case.summarized$sim <- "Simulation 1"

ggplot(filter(data.2grammars.case.summarized, model == 'Posterior probability'), aes(x=wordorder, y=mean, fill=case)) + 
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=c("#0C7BDC","#FFC20A")) +
  scale_y_continuous(name='Mean posterior probability') + scale_x_discrete(name='') + labs(fill = "Case-Marking") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank()) +
  theme(strip.text.y = element_text(size = 10.5), strip.text.x = element_text(size = 10.5))

# analysis
t.test(filter(data.2grammars.case, model == 'Bayesian')$SOV_12, filter(data.2grammars.case, model == 'Bayesian')$SOV_21)


## 8 grammars and case-marking
data.8grammars.case.summarized <- summarise(group_by(data.8grammars.case.long, language, grammar, model), mean=mean(proportion, na.rm = TRUE), 
                                  n = length(proportion), sd=sd(proportion, na.rm=TRUE), se=sd/sqrt(n))

data.8grammars.case.summarized$grammar <- factor(data.8grammars.case.summarized$grammar, levels = c('SVO_12','SVO_21','SOV_12','SOV_21','OVS_12','OVS_21',
                                                                                'VOS_12','VOS_21')) 
data.8grammars.case.summarized$model <- factor(data.8grammars.case.summarized$model, levels = c('Data Coverage', 'Bayesian')) 
levels(data.8grammars.case.summarized$model) <- c('Prop. data covered', 'Posterior probability')

data.8grammars.case.summarized$wordorder <- 'SVO'
data.8grammars.case.summarized$wordorder[which((data.8grammars.case.summarized$grammar == 'SOV_12')|(data.8grammars.case.summarized$grammar =='SOV_21'))] <- "SOV"
data.8grammars.case.summarized$wordorder[which((data.8grammars.case.summarized$grammar == 'OVS_12')|(data.8grammars.case.summarized$grammar =='OVS_21'))] <- "OVS"
data.8grammars.case.summarized$wordorder[which((data.8grammars.case.summarized$grammar == 'VOS_12')|(data.8grammars.case.summarized$grammar =='VOS_21'))] <- "VOS"

data.8grammars.case.summarized$wordorder <- factor(data.8grammars.case.summarized$wordorder, levels = c('SVO','SOV','OVS','VOS')) 
data.8grammars.case.summarized$case <- 'np-ga: Subj, np-o: Obj'
data.8grammars.case.summarized$case[which((data.8grammars.case.summarized$grammar == 'SOV_21') |
                                (data.8grammars.case.summarized$grammar == 'SVO_21') |
                                (data.8grammars.case.summarized$grammar == 'OVS_21') | 
                                (data.8grammars.case.summarized$grammar == 'VOS_21'))] <- 'np-ga: Obj, np-o: Subj'
data.8grammars.case.summarized$case <- factor(data.8grammars.case.summarized$case, levels = c('np-ga: Subj, np-o: Obj','np-ga: Obj, np-o: Subj')) 
data.8grammars.case.summarized$sim <- "Simulation 2"

ggplot(data.8grammars.case.summarized, aes(x=grammar, y=mean, fill=grammar)) + 
  facet_grid(model~language, scales = "free_y", ) +
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=cbPalette2) +
  scale_y_continuous(name='') + scale_x_discrete(name='') + labs(fill = "Grammar") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(legend.position="none") + theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank()) +
  theme(strip.text.y = element_text(size = 10.5), strip.text.x = element_text(size = 10.5))

ggplot(filter(data.8grammars.case.summarized, model == 'Posterior probability'), aes(x=wordorder, y=mean, fill=case)) + 
  geom_bar(stat="identity", position=position_dodge()) + scale_fill_manual(values=c("#0C7BDC","#FFC20A")) +
  scale_y_continuous(name='Mean posterior probability') + scale_x_discrete(name='') + labs(fill = "Case-Marking") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank()) +
  theme(strip.text.y = element_text(size = 10.5), strip.text.x = element_text(size = 10.5))

library(stringr)
ggplot(filter(data.8grammars.case.summarized, model == 'Posterior probability'), aes(x=wordorder, y=mean, fill=case)) + 
  geom_bar(stat="identity", position=position_dodge(0.9),width=0.8) + 
  scale_fill_manual(values=c("#332288","#FFC20A"), labels = c("ga: subject,\no: object", "ga: object,\no: subject")) +
  scale_y_continuous(name='Posterior probability', breaks = seq(0, 0.45, by = 0.2)) + scale_x_discrete(name='') + labs(fill = "Case-Marking") +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), width=.2, position=position_dodge(.9)) + theme_bw() +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  theme(panel.grid.minor.x = element_blank(), panel.grid.major.x = element_blank()) + theme(legend.title=element_blank()) +
  guides(fill = guide_legend(byrow = TRUE)) + 
  theme(legend.key = element_rect(color = NA),legend.key.size = unit(0.4, 'cm'), legend.spacing.y = unit(0.6, 'lines'))

# analyses
SOV_21 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$SOV_21)
SVO_12 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$SVO_12)
SVO_21 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$SVO_21)
OVS_12 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$OVS_12)
OVS_21 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$OVS_21)
VOS_12 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$VOS_12)
VOS_21 <- t.test(filter(data.8grammars.case, model == 'Bayesian')$SOV_12, filter(data.8grammars.case, model == 'Bayesian')$VOS_21)

## FULLY-FLEXIBLE LEARNER
## calculating S and O initial proportions wrt to other option for true S and O position 
data.alt["Sinitial"] = data.alt$S.NP.VP / (data.alt$S.NP.VP + data.alt$S.VP.NP)
data.alt["Oinitial"] = data.alt$VP.NP.V / (data.alt$VP.NP.V + data.alt$VP.V.NP)
data.alt["SAdjinitial"] = data.alt$S.NP.S / (data.alt$S.NP.S + data.alt$S.S.NP)
data.alt["OAdjinitial"] = data.alt$VP.NP.VP / (data.alt$VP.NP.VP + data.alt$VP.VP.NP)

data.alt <- reshape(data.alt, 
                         varying = c("Sinitial", "SAdjinitial"), 
                         v.names = "Sinitial",
                         timevar = "Sposition",
                         times = c("Argument", 
                                   "Adjunct"),
                         direction = "long",
                         new.row.names = 1:1000000)

data.alt <- reshape(data.alt, 
                    varying = c("Oinitial", "OAdjinitial"), 
                    v.names = "Oinitial",
                    timevar = "Oposition",
                    times = c("Argument", 
                              "Adjunct"),
                    direction = "long",
                    new.row.names = 1:2000000)

## calculating S and O proportions wrt to all other NP positions at the S and VP levels
data.alt["Sinitialv2"] = data.alt$S.NP.VP / (data.alt$S.NP.VP + data.alt$S.VP.NP + data.alt$S.NP.S + data.alt$S.S.NP)
data.alt["Oinitialv2"] = data.alt$VP.NP.V / (data.alt$VP.NP.V + data.alt$VP.V.NP + data.alt$VP.NP.VP + data.alt$VP.VP.NP)
data.alt["Sfinalv2"] = data.alt$S.VP.NP / (data.alt$S.NP.VP + data.alt$S.VP.NP + data.alt$S.NP.S + data.alt$S.S.NP)
data.alt["Ofinalv2"] = data.alt$VP.V.NP / (data.alt$VP.NP.V + data.alt$VP.V.NP + data.alt$VP.NP.VP + data.alt$VP.VP.NP)

data.alt.args <- filter(data.alt, Sposition == "Argument", Oposition == "Argument")
data.alt.adjs <- filter(data.alt, Sposition == "Adjunct", Oposition == "Adjunct")

# HOW MUCH DATA CAN WE ANALYZE?
Eng.unbiased.toplot <- filter(data.alt.args, bias == 'Unbiased', lang == 'English', !is.nan(Sinitial), !is.nan(Oinitial))
length(Eng.unbiased.toplot$sample)

Fr.unbiased.toplot <- filter(data.alt.args, bias == 'Unbiased', lang == 'French', !is.nan(Sinitial), !is.nan(Oinitial))
length(Fr.unbiased.toplot$sample)

J.unbiased.toplot <- filter(data.alt.args, bias == 'Unbiased', lang == 'Japanese', !is.nan(Sinitial), !is.nan(Oinitial))
length(J.unbiased.toplot$sample)

Eng.biasedtoplot <- filter(data.alt.args, bias == 'Biased', lang == 'English', !is.nan(Sinitial), !is.nan(Oinitial))
length(Eng.biasedtoplot$sample)
length(filter(data.alt.args, bias == 'Biased', lang == 'English')$sample)

Fr.biasedtoplot <- filter(data.alt.args, bias == 'Biased', lang == 'French', !is.nan(Sinitial), !is.nan(Oinitial))
length(Fr.biasedtoplot$sample)
length(filter(data.alt.args, bias == 'Biased', lang == 'French')$sample)

J.biasedtoplot <- filter(data.alt.args, bias == 'Biased', lang == 'Japanese', !is.nan(Sinitial), !is.nan(Oinitial))
length(J.biasedtoplot$sample)
length(filter(data.alt.args, bias == 'Biased', lang == 'Japanese')$sample)

# PLOTS
# Scatterplots looking at S and O initial proportions in fully transitive structures only
data.alt.args$bias <- factor(data.alt.args$bias, levels = c('Unbiased','Biased'))

ggplot(data.alt.args, aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.02, width = 0.005, height = 0.005) +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(text = element_text(size=12))

# plotting every 5th sample
ggplot(filter(data.alt.args, id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.05, width = 0.005, height = 0.005) +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(text = element_text(size=12))

## Only the biased learners, to check for unanalyzable data
ggplot(filter(data.alt.args, bias == 'Biased', lang == 'English', id%%5== 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs") + 
  scale_x_continuous(name="Proportion subjects before VPs") +
  theme_bw() + geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) +
  theme(text = element_text(size=12))

ggplot(filter(data.alt.args, bias == 'Biased', lang == 'French', id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs") + 
  scale_x_continuous(name="Proportion subjects before VPs") +
  theme_bw() + geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) +
  theme(text = element_text(size=12))

ggplot(filter(data.alt.args, bias == 'Biased', lang == 'Japanese', id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs") + 
  scale_x_continuous(name="Proportion subjects before VPs") +
  theme_bw() + geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) +
  theme(text = element_text(size=12))

## Only the unbiased learners, to check for unanalyzable data
ggplot(filter(data.alt.args, bias == 'Unbiased', lang == 'English', id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs") + 
  scale_x_continuous(name="Proportion subjects before VPs") +
  theme_bw() + geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) +
  theme(text = element_text(size=12))

ggplot(filter(data.alt.args, bias == 'Unbiased', lang == 'French', id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs") + 
  scale_x_continuous(name="Proportion subjects before VPs") +
  theme_bw() + geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) +
  theme(text = element_text(size=12))

ggplot(filter(data.alt.args, bias == 'Unbiased', lang == 'Japanese', id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs") + 
  scale_x_continuous(name="Proportion subjects before VPs") +
  theme_bw() + geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) +
  theme(text = element_text(size=12))

## analysis
data.alt.args.filtered <- filter(data.alt.args, !is.na(Sinitial), !is.na(Oinitial))
argmeans.byrun <- summarise(group_by(data.alt.args.filtered, bias, lang, run), subjmean=mean(Sinitial,na.rm = TRUE), objmean=mean(1-Oinitial,na.rm = TRUE))
argmeans <- summarise(group_by(argmeans.byrun, bias, lang), subjmean=mean(subjmean), objmean = mean(objmean))

subj.Eng.biased <- t.test(filter(argmeans.byrun, lang == 'English', bias == 'Biased')$subjmean, mu = 0.5)
subj.Fr.biased <- t.test(filter(argmeans.byrun, lang == 'French', bias == 'Biased')$subjmean, mu = 0.5)
subj.J.biased <- t.test(filter(argmeans.byrun, lang == 'Japanese', bias == 'Biased')$subjmean, mu = 0.5)
obj.Eng.biased <- t.test(filter(argmeans.byrun, lang == 'English', bias == 'Biased')$objmean, mu = 0.5)
obj.Fr.biased <- t.test(filter(argmeans.byrun, lang == 'French', bias == 'Biased')$objmean, mu = 0.5)
obj.J.biased <- t.test(filter(argmeans.byrun, lang == 'Japanese', bias == 'Biased')$objmean, mu = 0.5)

## PLOTTING MULTIPLE DATASETS
## calculating S and O initial proportions wrt to other option for true S and O position 
data.alt.combined["Sinitial"] = data.alt.combined$S.NP.VP / (data.alt.combined$S.NP.VP + data.alt.combined$S.VP.NP)
data.alt.combined["Oinitial"] = data.alt.combined$VP.NP.V / (data.alt.combined$VP.NP.V + data.alt.combined$VP.V.NP)
data.alt.combined["SAdjinitial"] = data.alt.combined$S.NP.S / (data.alt.combined$S.NP.S + data.alt.combined$S.S.NP)
data.alt.combined["OAdjinitial"] = data.alt.combined$VP.NP.VP / (data.alt.combined$VP.NP.VP + data.alt.combined$VP.VP.NP)

data.alt.combined <- reshape(data.alt.combined, 
                    varying = c("Sinitial", "SAdjinitial"), 
                    v.names = "Sinitial",
                    timevar = "Sposition",
                    times = c("Argument", 
                              "Adjunct"),
                    direction = "long",
                    new.row.names = 1:1000000)

data.alt.combined <- reshape(data.alt.combined, 
                    varying = c("Oinitial", "OAdjinitial"), 
                    v.names = "Oinitial",
                    timevar = "Oposition",
                    times = c("Argument", 
                              "Adjunct"),
                    direction = "long",
                    new.row.names = 1:2000000)

## calculating S and O proportions wrt to all other NP positions at the S and VP levels
data.alt.combined["Sinitialv2"] = data.alt.combined$S.NP.VP / (data.alt.combined$S.NP.VP + data.alt.combined$S.VP.NP + data.alt.combined$S.NP.S + data.alt.combined$S.S.NP)
data.alt.combined["Oinitialv2"] = data.alt.combined$VP.NP.V / (data.alt.combined$VP.NP.V + data.alt.combined$VP.V.NP + data.alt.combined$VP.NP.VP + data.alt.combined$VP.VP.NP)
data.alt.combined["Sfinalv2"] = data.alt.combined$S.VP.NP / (data.alt.combined$S.NP.VP + data.alt.combined$S.VP.NP + data.alt.combined$S.NP.S + data.alt.combined$S.S.NP)
data.alt.combined["Ofinalv2"] = data.alt.combined$VP.V.NP / (data.alt.combined$VP.NP.V + data.alt.combined$VP.V.NP + data.alt.combined$VP.NP.VP + data.alt.combined$VP.VP.NP)

data.alt.combined.args <- filter(data.alt.combined, Sposition == "Argument", Oposition == "Argument")
data.alt.combined.adjs <- filter(data.alt.combined, Sposition == "Adjunct", Oposition == "Adjunct")

## scatterplots plotting every 5th sample
ggplot(filter(data.alt.combined.args, id%%5 == 0, bias == "Biased", dataset != "50 strings"), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(dataset~lang) + 
  theme_bw() + geom_jitter(aes(color=dataset), size = 2.5, alpha = 0.05, width = 0.005, height = 0.005) +
  scale_color_manual(values=cbPaletteTernary2) + theme(legend.position = "none") +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(axis.title = element_text(size=12), axis.text=element_text(size=8)) + theme(panel.spacing = unit(1.5, "lines"))

## scatterplots including both 50-sentence datasets
data.alt.combined.args$dataset[which(data.alt.combined.args$bias == "Unbiased")] <- "Unbiased"

ggplot(filter(data.alt.combined.args, id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(dataset~lang) + 
  theme_bw() + geom_jitter(aes(color=dataset), size = 2.5, alpha = 0.05, width = 0.005, height = 0.005) +
  scale_color_manual(values=cbPalette8) + theme(legend.position = "none") +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(axis.text=element_text(size=7.5)) + theme(panel.spacing = unit(1.25, "lines")) + 
  theme(axis.title.x = element_blank(), axis.title.y = element_blank())


## FULLY-FLEXIBLE CASE MARKING LEARNER
## calculating S and O initial proportions wrt to other option for true S and O position 
data.alt.case["Sinitial"] = data.alt.case$S.NPS.VP / (data.alt.case$S.NPS.VP + data.alt.case$S.VP.NPS)
data.alt.case["Oinitial"] = data.alt.case$VP.NPO.V / (data.alt.case$VP.NPO.V + data.alt.case$VP.V.NPO)
data.alt.case["SAdjinitial"] = data.alt.case$S.NPA.S / (data.alt.case$S.NPA.S + data.alt.case$S.S.NPA)
data.alt.case["OAdjinitial"] = data.alt.case$VP.NPA.VP / (data.alt.case$VP.NPA.VP + data.alt.case$VP.VP.NPA)

## calculating case marking proportions
# bottom-up proportions (proportion of np1 rewritten as NPS vs. NPO, np2 rewritten as NPS vs. NPO)
data.alt.case.bu["NPS1"] = data.alt.case.bu$NPS.np1 / (data.alt.case.bu$NPS.np1 + data.alt.case.bu$NPO.np1)
data.alt.case.bu["NPS2"] = data.alt.case.bu$NPS.np2 / (data.alt.case.bu$NPO.np2 + data.alt.case.bu$NPS.np2)
data.alt.case.bus <- data.alt.case.bu[, c("bias", "lang", "run", "sample", "NPS1", "NPS2")]

data.alt.case.combined <- merge(data.alt.case, data.alt.case.bus)
data.alt.case.combined["casedarg"] <- "Neither/Both"
data.alt.case.combined$casedarg[which(data.alt.case.combined$NPS1 == 1 & data.alt.case.combined$NPS2 == 1)] <- "Subject"
data.alt.case.combined$casedarg[which(data.alt.case.combined$NPS1 == 0 & data.alt.case.combined$NPS2 == 0)] <- "Object"

## separate out 'adjunct' and 'argument' NP positions
data.alt.case.combined <- reshape(data.alt.case.combined, 
                         varying = c("Sinitial", "SAdjinitial"), 
                         v.names = "Sinitial",
                         timevar = "Sposition",
                         times = c("Argument", 
                                   "Adjunct"),
                         direction = "long",
                         new.row.names = 1:200000)

data.alt.case.combined <- reshape(data.alt.case.combined, 
                         varying = c("Oinitial", "OAdjinitial"), 
                         v.names = "Oinitial",
                         timevar = "Oposition",
                         times = c("Argument", 
                                   "Adjunct"),
                         direction = "long",
                         new.row.names = 1:200000)

data.alt.case.args <- filter(data.alt.case.combined, Sposition == "Argument", Oposition == "Argument")
data.alt.case.adjs <- filter(data.alt.case.combined, Sposition == "Adjunct", Oposition == "Adjunct")


##PLOTS
# Word order:
# Scatterplots looking at S and O initial proportions in fully transitive structures only
ggplot(data.alt.case.args, aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.02, width = 0.0001, height = 0.0001) +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(text = element_text(size=12))

# plotting every 5th sample
ggplot(filter(data.alt.case.args, id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.1, width = 0.0001, height = 0.0001) +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(text = element_text(size=11), plot.title = element_text(size=11)) + 
  ggtitle("Fully-flexible case-marking learner: \nWord order inference")

# color-coding each sample by whether the case-marked argument is the subject or object
data.alt.case.args$casedarg <- factor(data.alt.case.args$casedarg, levels = c("Subject", "Object", "Neither/Both"))
data.alt.case.args$bias <- factor(data.alt.case.args$bias, levels = c("Unbiased", "Biased"))

ggplot(filter(data.alt.case.args, id%%5 == 0), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~.) +
  theme_bw() + geom_jitter(aes(color=casedarg), size = 2.5, alpha = 0.05, width = 0.005, height = 0.005) +
  #geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + ## uncomment to make sure jitter isn't excluding data from plot
  theme(text = element_text(size=12)) + scale_colour_manual(values=cbPaletteTernary3) +
  guides(colour = guide_legend(override.aes = list(alpha=1))) +
  labs(colour = "Cased Argument")

# HOW MUCH DATA CAN WE ANALYZE?
unbiased.toplot.wo <- filter(data.alt.case.args, bias == 'Unbiased', !is.nan(Sinitial), !is.nan(Oinitial))
length(unbiased.toplot.wo$sample)
length(filter(data.alt.case.args, bias == 'Unbiased')$sample)

biased.toplot.wo <- filter(data.alt.case.args, bias == 'Biased', !is.nan(Sinitial), !is.nan(Oinitial))
length(biased.toplot.wo$sample)
length(filter(data.alt.case.args, bias == 'Biased')$sample)

# Checking for unanalyzable data
ggplot(filter(data.alt.case.args, id%%5 == 0, bias == "Biased"), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + 
  geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + 
  theme(text = element_text(size=12), plot.title = element_text(size=12))

ggplot(filter(data.alt.case.args, id%%5 == 0, bias == "Unbiased"), aes(x=Sinitial, y=Oinitial)) +
  scale_y_continuous(name="Proportion objects before verbs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_x_continuous(name="Proportion subjects before VPs", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + 
  geom_point(colour="#0C7BDC", size = 2.5, alpha = 0.1) + 
  theme(text = element_text(size=12), plot.title = element_text(size=12))

## Scatterplots looking at case-marker proportions
ggplot(data.alt.case.args, aes(x=NPS1, y=NPS2)) +
  scale_x_continuous(name="Proportion 'ga' parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_y_continuous(name="Proportion 'o' parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.02, width = 0.005, height = 0.005) +
  theme(text = element_text(size=12))

ggplot(filter(data.alt.case.args, id%%5 == 0), aes(x=NPS1, y=NPS2)) +
  scale_x_continuous(name="Proportion np-ga parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_y_continuous(name="Proportion np-o parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~.) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.05, width = 0.005, height = 0.005) +
  theme(text = element_text(size=12)) 

# HOW MUCH DATA CAN WE ANALYZE?
unbiased.toplot.case <- filter(data.alt.case.args, bias == 'Unbiased', !is.nan(NPS1), !is.nan(NPS2))
length(unbiased.toplot.case$sample)
length(filter(data.alt.case.args, bias == 'Unbiased')$sample)

biased.toplot.case <- filter(data.alt.case.args, bias == 'Biased', !is.nan(NPS1), !is.nan(NPS2))
length(biased.toplot.case$sample)
length(filter(data.alt.case.args, bias == 'Biased')$sample)

## analysis
casemarkers.byrun <- summarise(group_by(data.alt.case.args, bias, run), np1mean=mean(NPS1,na.rm = TRUE), np2mean=mean(NPS2,na.rm = TRUE))
casemeans <- summarise(group_by(casemarkers.byrun, bias), np1mean=mean(np1mean), np2mean = mean(np2mean))

np1.biased <- t.test(filter(casemarkers.byrun, bias == 'Biased')$np1mean, mu = 0.5)
np1.biased
np2.biased <- t.test(filter(casemarkers.byrun, bias == 'Biased')$np2mean, mu = 0.5)
np2.biased
np1.unbiased <- t.test(filter(casemarkers.byrun, bias == 'Unbiased')$np1mean, mu = 0.5)
np1.unbiased
np2.unbiased <- t.test(filter(casemarkers.byrun, bias == 'Unbiased')$np2mean, mu = 0.5)
np2.unbiased

np1 <- t.test(filter(casemarkers.byrun, bias == 'Biased')$np1mean, filter(casemarkers.byrun, bias == 'Unbiased')$np1mean)
np1

np2 <- t.test(filter(casemarkers.byrun, bias == 'Biased')$np2mean, filter(casemarkers.byrun, bias == 'Unbiased')$np2mean)
np2


## plotting NPS -> np1, NPS -> np2, NPO -> np1, and NPO -> np2 probabilities
data.alt.case.args$casedarg <- factor(data.alt.case.args$casedarg, levels = c("Subject", "Object", "Neither/Both"))

subjplot <-
  ggplot(filter(data.alt.case.args, id%%5 == 0), aes(x=NPS.np1, y=NPS.np2)) +
  scale_x_continuous(name=expression("Pr. NPS" %->% "np1"), breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_y_continuous(name=expression("Pr. NPS" %->% "np2"), breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~.) +
  theme_bw() + geom_jitter(aes(color=casedarg), size = 2.5, alpha = 0.1, width = 0.005, height = 0.005) +
  theme(text = element_text(size=11), plot.title = element_text(size=11)) + 
  ggtitle("Subject rewrite probabilities") +
  scale_color_manual(values = cbPaletteTernary) +
  theme(legend.position="none")

subjplot

objplot <-
  ggplot(filter(data.alt.case.args, id%%5 == 0), aes(x=NPO.np1, y=NPO.np2)) +
  scale_x_continuous(name=expression("Pr. NPO" %->% "np1"), breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_y_continuous(name=expression("Pr. NPO" %->% "np2"), breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~.) +
  theme_bw() + geom_jitter(aes(color=casedarg), size = 2.5, alpha = 0.1, width = 0.005, height = 0.005) +
  theme(text = element_text(size=11), plot.title = element_text(size=11)) + 
  ggtitle("Object rewrite probabilities") +
  scale_color_manual(values = cbPaletteTernary) +
  theme(legend.position="none")

objplot

comb <- plot_grid(subjplot, objplot, ncol = 2)
legend <- get_legend(objplot +
                     guides(colour = guide_legend(title.position = "top", title.hjust=0.5, override.aes = list(alpha=1))) +
                     labs(colour = "Cased Argument") + theme(legend.position="bottom",))
plot_grid(comb, legend, nrow=2,rel_heights = c(1, .1))


## CASE-MARKING LEARNER WITH ONLY SOV WORD ORDER

## calculating case marking proportions
data.alt.SOV.bu["NPS1"] = data.alt.SOV.bu$NPS.np1 / (data.alt.SOV.bu$NPS.np1 + data.alt.SOV.bu$NPO.np1)
data.alt.SOV.bu["NPS2"] = data.alt.SOV.bu$NPS.np2 / (data.alt.SOV.bu$NPO.np2 + data.alt.SOV.bu$NPS.np2)

## Scatterplots looking at case-marker porportions
ggplot(data.alt.SOV.bu, aes(x=NPS1, y=NPS2)) +
  scale_x_continuous(name="Proportion 'ga' parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_y_continuous(name="Proportion 'o' parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.02, width = 0.005, height = 0.005) +
  theme(text = element_text(size=12))

ggplot(filter(data.alt.SOV.bu, sample%%5 == 0), aes(x=NPS1, y=NPS2)) +
  scale_x_continuous(name="Proportion 'ga' parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) + 
  scale_y_continuous(name="Proportion 'o' parsed as subject", breaks = c(0.00, 0.25, 0.50, 0.75, 1.00), limits = c(-.02, 1.02)) +
  facet_grid(bias~lang) +
  theme_bw() + geom_jitter(colour="#0C7BDC", size = 2.5, alpha = 0.05, width = 0.005, height = 0.005) +
  theme(text = element_text(size=12)) +
  theme(text = element_text(size=11), plot.title = element_text(size=11)) + 
  ggtitle("Fully-flexible case-marking learner: \nSOV word order only")

# HOW MUCH DATA CAN WE ANALYZE?
unbiasedSOV.toplot.case <- filter(data.alt.SOV.bu, bias == 'Unbiased', !is.nan(NPS1), !is.nan(NPS2))
length(unbiasedSOV.toplot.case$sample)
length(filter(data.alt.SOV.bu, bias == 'Unbiased')$sample)

biasedSOV.toplot.case <- filter(data.alt.SOV.bu, bias == 'Biased', !is.nan(NPS1), !is.nan(NPS2))
length(biasedSOV.toplot.case$sample)
length(filter(data.alt.SOV.bu, bias == 'Biased')$sample)

## analysis
casemarkers.byrun <- summarise(group_by(data.alt.SOV.bu, bias, run), np1mean=mean(NPS1,na.rm = TRUE), np2mean=mean(NPS2,na.rm = TRUE))
casemeans <- summarise(group_by(casemarkers.byrun, bias), np1mean=mean(np1mean), np2mean = mean(np2mean))

np1.biased <- t.test(filter(casemarkers.byrun, bias == 'Biased')$np1mean, mu = 0.5)
np1.biased
np2.biased <- t.test(filter(casemarkers.byrun, bias == 'Biased')$np2mean, mu = 0.5)
np2.biased
np1.unbiased <- t.test(filter(casemarkers.byrun, bias == 'Unbiased')$np1mean, mu = 0.5)
np1.unbiased
np2.unbiased <- t.test(filter(casemarkers.byrun, bias == 'Unbiased')$np2mean, mu = 0.5)
np2.unbiased

