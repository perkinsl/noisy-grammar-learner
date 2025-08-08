## Hastings sampler for sampling s-structure ts from P(ts|w,alpha)

import math
import numpy as np
import random
from collections import OrderedDict, Counter
from functools import reduce
from cky import *
from likelihood import *
from baselines import *
from data import *

## Function that randomly initializes thetas for d-structure rules given alpha
def initialize_rules(hs, alpha):
    thetas = OrderedDict.fromkeys(hs.ds_rules, None)

    for (nonterm, values) in alpha.items():
        rules = OrderedDict((key,value) for key, value in thetas.items() if key[0] == nonterm)
        assert len(values) == len(rules)
        nonzeros = [item for item in values if item != 0]

        if None in nonzeros:

            assert all(x == None for x in nonzeros)
            nonzeroprobs = [1/len(nonzeros) for i in nonzeros]

        else:

            ## Issue with sampling from gamma distribution using np.random.dirichlet() with small alphas
            ## This sometimes returns nan, apparently
            nonzeroprobs = None
            while nonzeroprobs is None:
                dirichlet_samples = [i for i in np.random.dirichlet(nonzeros, size=None)]
                if any([math.isnan(x) for x in dirichlet_samples]):
                    pass
                else:
                    nonzeroprobs = dirichlet_samples

        ruleprobs = []
        i = 0
        for a in values:
            if a == 0:
                ruleprobs.append(0.0)
            else:
                ruleprobs.append(nonzeroprobs[i])
                i += 1
        thetas.update(zip(rules.keys(), ruleprobs))

    return defaultdict(lambda: 0, thetas)


## Acceptance function that takes a current tree and a new proposed tree for a string,
## and all other trees, alpha, and theta_s for these trees,
## and decides whether to accept the new proposed tree, or keep the old one
def accept(dirichlets, hs, p_curr, t, t_prime, ts_i, alpha, theta_s, temp):

    ## Check whether t and t_prime are the same
    # print(t_prime == t)
    if t == t_prime:
        return t_prime, p_curr

    else:
        ## Accept t_prime with prob. equal to
        ## min(1, ((P(t_prime|ts_i,alpha) * P(t|w[i], theta_s)) / (P(t|ts_i,alpha) * P(t_prime|w[i], theta_s))))
        ## Here, using "ts_i" to mean all of the trees except the ith tree that we are considering
        p = prob_t(t, theta_s) ## P(t|w[i], theta_s)
        if p == 0:
            logp = float('-inf')
        else:
            logp = temp*np.log(p)

        p_prime = prob_t(t_prime, theta_s) ## P(t_prime|w[i], theta_s)
        if p_prime == 0:
            logpprime = float('-inf')
        else:
            logpprime = temp*np.log(p_prime)

        ts_prime = ts_i + [t_prime]

        ## We can now piece things together to calculate the conditional probability of the old tree given all other trees
        ## And the conditional probability of the new proposed tree given all other trees
        ## Using the rule of conditional probability: P(a|b) = P(a,b)/P(b)

        ## Probability of all of the ts except the old tree: P(ts_i|alpha)
        p_i = temp*total_ll(dirichlets,hs,ts_i,alpha)

        ## Probability of all trees including the new proposed tree: P(t_prime,ts_i|alpha)
        p_prime = temp*total_ll(dirichlets,hs,ts_prime,alpha)

        ## Conditional probability of old tree P(t|ts_i,alpha) = P(t,ts_i|alpha)/P(ts_i|alpha)
        ## p_curr (an argument to the function) is the likelihood of all trees plus the old tree: P(t,ts_i|alpha)
        condp = p_curr-p_i

        ## Conditional probability of new tree P(t_prime|ts_i,alpha) = P(t_prime,ts_i|alpha)/P(ts_i|alpha)
        condp_prime = p_prime-p_i

        ## Full acceptance function from above
        A = min(1, math.exp((condp_prime+logp)-(condp+logpprime)))

        if A == 1:
            p_curr = p_prime
            #print("returned t_prime")
            return t_prime, p_curr

        else:
            x = random.random()
            if x < math.exp((condp_prime+logp)-(condp+logpprime)):
                p_curr = p_prime
                #print("returned t_prime")
                return t_prime, p_curr
            else:
                #print("t")
                return t, p_curr

# Conducts one iteration of MH sampling for a single chain
def tree_sampler(dirichlets, hs, alpha, data, sampled_ts, probs, temp, iteration):

    ts = sampled_ts[iteration]
    sampled_ts.append([])

    p_curr = probs[iteration]

    for j in range(len(data)):
        t = ts[j]
        new_ts = sampled_ts[iteration+1] + ts[j+1:]

        ## Set theta to expected value given current trees for all strings excluding j
        ## using maximum likelihood estimate, with add-one smoothing to account for accidental gaps
        rewrite_counts, parent_counts = count_ss_rewrites(hs.ss_rewrites, new_ts)
        nonterms = [rule[0] for rule in list(rewrite_counts.keys())]

        nonterms_counts = Counter(nonterms) 

        rules = {rule:(float(count+1))/float(parent_counts.get(rule[0])+nonterms.count(rule[0])) for (rule, count) in rewrite_counts.items()}
        means = list(rules.values())
        counter = 0
        new_probs_complete = []
        for key in nonterms_counts:
            num_rewrites = nonterms_counts[key]
            if num_rewrites == 1:
                new_probs = [1]
            else:
                cov = 0.25 * (np.identity(num_rewrites))
                mean = means[counter:counter+num_rewrites]
                counter = counter+num_rewrites
                new_probs = np.random.multivariate_normal(mean, cov)
                while any(((element > 1) or (element < 0)) for element in new_probs):
                    new_probs = np.random.multivariate_normal(mean, cov)
                new_probs = new_probs.tolist()
            new_probs_complete = new_probs_complete + new_probs
            #print(new_probs_complete)

        new_rules = rules.copy()
        counter = 0
        for key in new_rules:
            new_rules[key] = new_probs_complete[counter]
            counter+=1

        ## Sample new s-structure tree for string at position j using Inside algorithm

        #theta_s = defaultdict(lambda: 0, rules) #comment out line below and use this line for original implementation
        theta_s = defaultdict(lambda: 0, new_rules) #use this line for the new implementation where we sample thetas
        proposal = sample_tree(hs, tuple(data[j]), theta_s)

        ## Accept proposed new tree using acceptance function
        t_prime, p_curr = accept(dirichlets, hs, p_curr, t, proposal, new_ts, alpha, theta_s, temp)

        sampled_ts[iteration+1].append(t_prime)

    probs.append(p_curr)

    return (sampled_ts, probs)

## Version of helper function using parallel tempering to improve mixing
## Following method described here: 
## https://darrenjw.wordpress.com/2013/09/29/parallel-tempering-and-metropolis-coupled-mcmc/
## and https://academic.oup.com/gji/article/196/1/357/585739
def multichain_sampler(dirichlets, hs, alpha, data, iterations, chains, chatty=True):

    ## Randomly initialize a s-structure tree for each string, from trees allowable under alpha
    ## Doing this by first initializing a d-structure tree for each string, then flattening
    ts = None
    while ts is None:
        initial_rules = initialize_rules(hs, alpha)
        try:
            ds_ts = [sample_tree(hs, tuple(w), initial_rules) for w in data]
            ts = list(map(hs.convert_ds_to_ss, ds_ts))
        except UnparseableException:
            print("Exception: cannot parse tree, trying a new theta vector")
            pass

    sampled_ts = [[ts] for c in range(chains)]

    ## Create a temperature ladder for each chain between 0 and 1
    ## If only one chain, the default temperature is 1
    temps = np.arange(1.0, 0.0, -1/chains)

    ## Current probability of trees at each temperature
    probs = [[temp*total_ll(dirichlets,hs,ts,alpha)] for temp in temps]

    for i in range(iterations):

        if chatty:
            print('hastings iteration ', i) ## for trace

        unzip = lambda x: list(zip(*x))
        samples = unzip(map(lambda t, p, k: tree_sampler(dirichlets, hs, alpha, data, t, p, k, i), sampled_ts, probs, temps))
        sampled_ts = list(samples[0])
        probs = list(samples[1])

        ## If more than 1 chain, pick 2 random chains to propose a state swap
        if chains > 1:
            c1, c2 = random.sample(range(chains), 2)

            ## k1 and k2 are temperatures of these chains
            k1 = temps[c1]
            k2 = temps[c2]

            ## Let f(x) be target posterior of chain 1 and g(y) be target posterior of chain 2
            ## State swap: propose move from chain 1's sampled trees t to chain 2's sampled trees t', and vice versa
            ## Accept proposal with probability min(1,A), where A = f(t')g(t)/f(t)g(t')

            t = sampled_ts[c1][-1]
            t_prime = sampled_ts[c2][-1]

            f_t = probs[c1][-1]
            g_tprime = probs[c2][-1]

            ## Because each chain uses the same posterior raised to a different power (different temperature),
            ## we take the kth root of the other chain's posterior and raise to the power of k-prime
            f_tprime = g_tprime * (k1/k2)
            g_t = f_t * (k2/k1)

            A = min(1, math.exp((f_tprime+g_t)-(f_t+g_tprime)))
            x = random.random()

            if (A == 1) or (x < A):
                sampled_ts[c1][-1] = t_prime
                sampled_ts[c2][-1] = t
                probs[c1][-1] = f_tprime
                probs[c2][-1] = g_t
                #print('swapped states')

    return sampled_ts

## Function for sampling s-structure trees using Hastings proposal, assuming only one chain
def sample_ts(dirichlets, hs, data, alpha, iterations, chatty=True):

    chains = 1
    sampled_ts = multichain_sampler(dirichlets, hs, alpha, data, iterations, chains, chatty)[0]

    return sampled_ts[-1]

## Version of standalone sampler able to use parallel tempering
## The chains parameter corresponds to the number of chains to run in parallel (an integer value)
## For previous standalone version, pass 1 as this argument
## The ideal number for good mixing is 10 chains
def sample_ts_standalone(hs, alpha, data, iterations, chains, tag):

    dirichlets = {}
    data_shuffled = data
    random.shuffle(data_shuffled)

    sampled_ts = multichain_sampler(dirichlets, hs, alpha, data_shuffled, iterations, chains)[0]

    # Convert sampled_ts to a list of lists of strings (rather than list of lists of trees), so that numpy.asarray 
    # doesn't get misled by the fact that our trees are tuples (caused problems if the trees were the same `length')
    sampled_ts_as_strings = [[str(t) for t in tlist] for tlist in sampled_ts]
    np.savetxt('results/%s_ts.txt' % tag, np.asarray(sampled_ts_as_strings, dtype=str), fmt='%s')

    with open("results/%s_ss_rewrites.txt" % tag, 'w') as output:
        for i in list(hs.ss_rewrites):
            output.write(str(i) + '\n')

    return sampled_ts[-1], hs.ss_rewrites

