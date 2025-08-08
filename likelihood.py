## Calculates likelihood of data and a set of trees under alpha, P(ts, w|alpha)

import math
import numpy as np
import itertools
from operator import add
from functools import reduce
from trees import *
from grammars import *
from data import *
from numba import njit

## Function for pre-populating Dirichlet constant dictionary before chain runs
def create_ddict(hs, data):

    flatten = lambda l: [item for sublist in l for item in sublist]
    all_alphas = flatten([list(a.values()) for a in hs.alphas])
    alpha_keys = []
    for a in all_alphas:
        if a not in alpha_keys:
            alpha_keys.append(a)

    n_max = max(len(a) for a in alpha_keys)
    k_max = len(data)
    multichoose_dict = create_multichoose_dict(n_max, k_max)

    d = {}
    for a in alpha_keys:
        n = len(a)
        for k in range(k_max + 1):
            for x in multichoose_dict[(n,k)]:
                v = handle_zeros(a,x)
                d[(tuple(a),tuple(x))] = v
    return d

## Creates a dictionary where d[(n,k)] is a list of ways to choose 
## positions for k balls in n boxes
def create_multichoose_dict(n_max, k_max):
    d = {}
    for n_plus_k in range(n_max + k_max + 1):
        for n in range(n_plus_k + 1):
            k = n_plus_k - n
            if n > n_max or k > k_max:
                continue
            if k == 0:
                result = [[0]*n]
            elif n == 0:
                result = []
            elif n == 1:
                result = [[k]]
            else:
                result = [[0]+val for val in d[(n-1,k)]] + [[val[0]+1]+val[1:] for val in d[(n,k-1)]]
            d[(n,k)] = result
    return d

## Function calculating Dirichlet combinations term in log space
## for any vector a encoding rule pseudo-counts for expansions of the same nonterminal
## All pseudo-counts must be positive (non-zero)
## @njit doesn't work with assertion
## use @jit to allow falling back to normal mode without throwing an error
@njit(cache=True)
def dirichlet_c(a):
    # assert all([i > 0 for i in a])
    num = 0
    for i in a:
        num += math.lgamma(i)
    denom = math.lgamma(sum(a))
    return num - denom


## Function computing multinomial coefficient in log space
## For any vector of counts of rule expansions for a given nonterminal
def multinom(counts):
    num = math.lgamma(sum(counts)+1)
    denom = sum(map(lambda n: math.lgamma(n+1), counts))
    return num - denom


## Work out a likelihood given an alpha vector and a corresponding vector of counts,
## where the alpha vector might include any number 0s indicating that an outcome is
## outright disallowed.
def handle_zeros(alpha_vector, counts_vector):

    assert len(alpha_vector) == len(counts_vector)
    pairs = zip(alpha_vector, counts_vector)

    # Remove all (0,0) pairs, for disallowed things that correctly didn't happen
    pairs = list(filter(lambda x: x != (0,0), pairs))

    if pairs == []:
        # This was the only way things were allowed to be, so probability 1
        result = 0
    elif any(p[0] == 0 for p in pairs):
        # We have some non-zero count for something with an alpha value of zero
        result = float('-inf')
    elif any(p[0] == None for p in pairs):
        # This indicates a theta that we're not integrating over, but rather setting to be a uniform distribution
        assert all(p[0] == None for p in pairs)
        theta_r = np.log(1/(len(pairs)))
        result = sum([theta_r * y for (x,y) in pairs]) + multinom(counts_vector)
        # Probability is multinomial with theta_r as its parameter
    else:
        result = dirichlet_c(tuple(x+y for (x,y) in pairs)) - dirichlet_c(tuple(x for (x,y) in pairs))

    return result

## Function counting relevant treelet types in ss trees
def count_ss_rewrites(ss_rewrites, trees):

    ## Count instances of each relevant ss_rewrite in trees
    rewrite_list = reduce(lambda x,y: x+y , map(rewrites, trees))
    rewrite_counts = dict([(i, rewrite_list.count(i)) for i in ss_rewrites])

    ## Add together rewrites with same parent nonterminal (e.g., S, VP)
    parent_counts = {}
    for key in rewrite_counts.keys():
        if key[0] in parent_counts:
            parent_counts[(key[0])] += rewrite_counts.get(key)
        else:
            parent_counts[(key[0])] = rewrite_counts.get(key)

    return rewrite_counts, parent_counts


## For each nonterminal count n_a ... n_z, calculate log likelihood in parallel


## Log likelihood for a single nonterminal count, e.g. logP(n|alpha):
def calculate_likelihood(dirichlets, hs, nonterm, alpha, rewrite_counts, parent_counts):

    n = parent_counts.get(nonterm)
    #rewrite_list = { key:value for (key, value) in rewrite_counts.items() if key[0] == nonterm }
    #ns = list(rewrite_list.values())

    right_hand_sides_in_order = [rhs for (lhs,rhs) in hs.ss_rewrites if lhs == nonterm]
    ns = [rewrite_counts[(nonterm,rhs)] for rhs in right_hand_sides_in_order]

    ## Helper functions for calculating each term of likelihood eqn

    ## Calculate logP(n+|n,alpha): probability of certain number of signal ns given total ns
    def calculate_nterm(nplus, n, alpha):
        if nplus <= n:              ## double-check we're not out of range
            alpha_n = alpha.get(nonterm)

            try:
                nterm = dirichlets[(tuple(alpha_n), (nplus, n-nplus))]
            except KeyError:
                #print('Dirichlet key error ', (tuple(alpha_n), (nplus, n-nplus)))
                nterm = handle_zeros(alpha_n, [nplus, n-nplus])
                dirichlets[(tuple(alpha_n), (nplus, n-nplus))] = nterm
        else:
            nterm = float('-inf')
        return nterm


    ## Calculate logP(n_1+ ... n_m+|n+, alpha):
    ## probability of total signal ns distributing among the various rule expansions
    def calculate_nplusterm(npluses, nplus, ns, alpha):

        if sum(npluses) == nplus and all([npluses[i] <= ns[i] for i in range(len(npluses))]): ## double-check we're not out of range
            #alpha_nplus = alpha.get(hs.nonnoise_version(nonterm))

            try:
                nplusterm = dirichlets[(tuple(alpha_nplus), tuple(npluses))]
            except KeyError:
                #print('Dirichlet key error ', (tuple(alpha_nplus), tuple(npluses)))
                nplusterm = handle_zeros(alpha_nplus, npluses)
                dirichlets[(tuple(alpha_nplus), tuple(npluses))] = nplusterm

        else:
            nplusterm = float('-inf')

        return nplusterm

    ## Calculate logP(n_1- ... n_m-|n-,alpha):
    ## probability of total noise ns distributing among the various rule expansions
    def calculate_nminterm(npluses, nplus, ns, alpha):
        nmin = n - nplus
        nmins = [ns[i]-npluses[i] for i in range(len(npluses))]
        if sum(nmins) == nmin:          ## double-check we're not out of range
            #alpha_nmin = alpha.get(hs.noise_version(nonterm))

            try:
                nminterm = dirichlets[(tuple(alpha_nmin), tuple(nmins))]
            except:
                #print('Dirichlet key error ', (tuple(alpha_nmin), tuple(nmins)))
                nminterm = handle_zeros(alpha_nmin, nmins)
                dirichlets[(tuple(alpha_nmin), tuple(nmins))] = nminterm

        else:
            nminterm = float('-inf')

        return nminterm

    alpha_nplus = alpha.get(hs.nonnoise_version(nonterm))
    alpha_nmin = alpha.get(hs.noise_version(nonterm))

    # list of ranges, where each inner element is the possible niplus
    # avoiding extra sums where there are zeros either in non-noise or noise alpha vectors
    niplus_range = [ [ni] if alpha_nmin[i] == 0 else [0] if alpha_nplus[i] == 0 else range(ni+1) for (i, ni) in enumerate(ns) ]

    # possible nplus
    # nplus = range(n+1)
    # permutations of nipluses
    # e.g. [(0, 0, 0), (0, 1, 0), (0, 1, 1), ..., (2, 1, 3)]
    nipluses_combos = itertools.product(*niplus_range)
    # nipluses_combos = itertools.product(*niplus_range)
    # 4-tuple input arguments for calculate_nplusterm and calculate_nminterm
    # only keep nplus if it is a sum of nipluses
    nplusgroup = [(nipluses_combo, sum(nipluses_combo), ns, alpha) for nipluses_combo in nipluses_combos]
    #nplusgroup = [result for result in itertools.product(nipluses_combos, nplus, [ns], [alpha]) if sum(result[0]) == result[1]]
    nplusgroup = sorted(nplusgroup, key = lambda x: x[1])


    ## Calculate P(n_1+ ... n_m+|n+, alpha) * P(n_1- ... n_m-|n-,alpha) * P(n+|n, alpha)
    ##      itertools.starmap() applies given function using all elements from the tuple as arguments
    ##      E.g., it applies calculate_nplusterm to the (n+, (n_1+ ... n_m+)) tuples in the given list of tuples


    # 3-tuple input argument for calculate_nterm
    ngroup = [ (tup[1], n, alpha) for tup in nplusgroup ]


    nterm = itertools.starmap(calculate_nterm, ngroup)
    nplusterm = itertools.starmap(calculate_nplusterm, nplusgroup)
    nminterm = itertools.starmap(calculate_nminterm, nplusgroup)
    product = sorted(map(add, nterm, map(add, nplusterm, nminterm)), reverse=True) ## Sort results from large to small


    ## Calculate summation over these probabilities
    ## Trick for computing the log of a summation without stack overflow:
    ## You can subtract the largest log value from all other values without exponentiating it
    ##      log(sum of a_i from i=0 to N) =
    ##          = log(a_0) + log(1 + (sum of (a_i)/(a_0) from i=1 to N))
    ##          = log(a_0) + log(1 + (sum of exp(log(a_i) - log(a_0)) from i=1 to N))
    ##      for a_0 > a_1 > ... > a_N

    ## If largest log probability in list is -inf, result of subtraction for rest of list is also -inf
    ## Otherwise, perform subtraction for the result of the list, and exponentiate result
    if product[0] == float('-inf'):
        sub = product
    else:
        sub = map(lambda x: x-product[0], product)
    exp = map(lambda x: math.exp(x), sub)

    ## Add to 1, re-log, and add to first log probability in list
    ## np.log1p() calculates log(1 + x) for each element x of input array
    likelihood = product[0] + np.log1p(sum(itertools.islice(exp,1,None)))

    return likelihood

## Total log likelihood: product of log likelihoods for all nonterminals
## This is assuming that these trees are all valid trees for the strings in data
def total_ll(dirichlets, hs, trees, alpha):
    (rewrite_counts, parent_counts) = count_ss_rewrites(hs.ss_rewrites, trees)
    nonterms = parent_counts.keys()

    lls = map(lambda n: calculate_likelihood(dirichlets, hs, n, alpha,rewrite_counts, parent_counts), nonterms)
    return sum(lls)

