## Outermost function: Gibbs sampler that alternates between sampling alphas and sampling trees

import math
import numpy as np
import random
from likelihood import *
from hastings_sampler import *
import timeit
import pandas as pd
from grammars import *
from data import *

## For testing
# random.seed(0)
# np.random.seed(0)  # sets seed for hastings_sampler

## Function for sampling alpha from P(alpha|w,ts)
def sample_alpha(dirichlets, hs, ts):

    ## Staying in log space here to avoid overflow issues
    ## Compute log likelihood of ts under each value of alpha
    likelihoods = [total_ll(dirichlets, hs, ts, alpha) for alpha in hs.alphas]

    ## Compute log posterior probability of each value of alpha given ts
    numerators = sorted([x+y for x,y in zip(np.log(hs.priors), likelihoods)], reverse=True)

    ## Trick for computing the log of a summation without stack overflow:
    ## You can subtract the largest log value from all other values without exponentiating it
    ##      log(sum of a_i from i=0 to N) =
    ##          = log(a_0) + log(1 + (sum of (a_i)/(a_0) from i=1 to N))
    ##          = log(a_0) + log(1 + (sum of exp(log(a_i) - log(a_0)) from i=1 to N))
    ##      for a_0 > a_1 > ... > a_N

    ## If largest log probability in list is -inf, result of subtraction for rest of list is also -inf
    ## Otherwise, perform subtraction for the result of the list, and exponentiate result
    if numerators[0] == float('-inf'):
        sub = numerators
    else:
        sub = map(lambda x: x-numerators[0], numerators)
    exp = map(lambda x: math.exp(x), sub)

    ## Add to 1, re-log, and add to first log probability in list
    ## np.log1p() calculates log(1 + x) for each element x of input array
    denominators = numerators[0] + np.log1p(sum(itertools.islice(exp,1,None)))

    # Calculate log posterior and re-exponentiate
    posteriors = list(map(lambda x: math.exp(x), [n-denominators for n in numerators]))
    #print("current posteriors: ", posteriors)

    ## Flip coin weighted by posteriors over alpha in order to sample a new alpha
    sampled_alpha = random.choices(hs.alphas, posteriors)[0]

    return sampled_alpha

## Gibbs sampler: jointly samples alphas and trees over specified number of iterations
## hs: hypothesis space
## data: dataset (list)
## iterations: number of iterations (integer)
## tag: descriptor of run (string)
## chatty: optional, for trace
def joint_inference(hs, data, iterations, tag, chatty=True):

    #saving current dataset
    with open('results/%s_dataset.txt' % tag, 'w') as output:
        for i in data:
            output.write(str(i) + ', ')

    starttime = timeit.default_timer()
    ## Randomly initialize a value for alpha
    alpha_0 = random.choice(hs.alphas)

    sampled_alphas = [alpha_0]
    sampled_ts = []
    dirichlets = {}

    for i in range(iterations):
        #starttime_it = timeit.default_timer() #-- for timer
        if chatty:
            print('gibbs iteration ', i)
            print('current alpha ', sampled_alphas[i])
        else:
            print(".", end="", flush=True)

        ## Sample new trees from pdf on t using Hastings proposal
        ## Changed to just a single iteration of Hastings sampling, because we're updating this component-wise
        data_shuffled = data.copy()
        random.shuffle(data_shuffled)
        sampled_ts.append(sample_ts(dirichlets, hs, data_shuffled, sampled_alphas[i], 1, chatty))

        ## print('current trees ', sampled_ts[i]) -- for tree trace

        ## Sample new alpha from pdf on alpha
        sampled_alphas.append(sample_alpha(dirichlets, hs, sampled_ts[i]))

        #print('iteration time: ', timeit.default_timer() - starttime_it) #-- for timer trace

    if not chatty:
        print()

    np.savetxt('results/%s_sampled_alphas.txt' % tag, np.asarray(sampled_alphas), fmt='%s')
    # Convert sampled_ts to a list of lists of strings (rather than list of lists of trees), so that numpy.asarray 
    # doesn't get misled by the fact that our trees are tuples (caused problems if the trees were the same `length')
    sampled_ts_as_strings = [[str(t) for t in tlist] for tlist in sampled_ts]
    np.savetxt('results/%s_sampled_ts.txt' % tag, np.asarray(sampled_ts_as_strings, dtype=str), fmt='%s')

    #print('total time: ', timeit.default_timer() - starttime)

    #saving current alpha legend, to preserve sorting key:
    with open("results/%s_alphalegend.txt" % tag, 'w') as output:
        for i in list(hs.alpha_legend.items()):
            output.write(str(i) + '\n')

    return sampled_alphas, sampled_ts, list(hs.alpha_legend.items())

## Create a table of counts of sampled alphas for a specified number of samples
def count_alphas(hs, sampled_alphas, iterations, skip_rate):

    ## Use every nth value from the last half of iterations as samples
    samples = sampled_alphas[round(iterations/2 + 1)::skip_rate]
    alpha_counts = [[key, samples.count(value)] for key, value in hs.alpha_legend.items()]
    alpha_table = np.asarray(alpha_counts)
    np.savetxt('alpha_table', alpha_table, delimiter=",", fmt='%s')

    return alpha_table

def print_data(d):
    print()
    for (x,freq) in Counter(map(tuple,d)).most_common():
        print("\t%5d\t%s" % (freq, " ".join(x)))
    print()

## For real-time trace visualization
def ji_wrapper(hs, data, num_iterations, tag):

    print_data(data)

    sampled_alphas, _, _ = joint_inference(hs, data, num_iterations, tag, chatty=False)

    print()
    denom = len(sampled_alphas)
    for (label,a) in hs.alpha_legend.items():
        num = sampled_alphas.count(a)
        worm_line = "".join(("*" if x == a else " ") for x in sampled_alphas)
        print("\t%16s\t%5d\t%.3f\t%s" % (label, num, num/denom, worm_line))
    print()


