from random import *
from math import comb

## Regularization simulation
## samples numbers of 'ka' and 'bo' at a particular forgetting rate
def sample_austindata(rate, observed_k, observed_b):
    k_total = 0
    b_total = 0

    for i in range(0,observed_k):
        x = random()
        if x > rate:
            k_total += 1

    for i in range(0,observed_b):
        x = random()
        if x > rate:
            b_total += 1

    return (k_total, b_total)

## generates samples for a number of simulated learners
def generate_samples(runs, rate, observed_k, observed_b):
    k_totals = []
    b_totals = []

    for i in range(0,runs):
        (ka,bo) = sample_austindata(rate,observed_k,observed_b)
        k_totals.append(ka)
        b_totals.append(bo)

    return(k_totals,b_totals)

## Noisy hypotheses simulations
## Likelihood of particular numbers of `ka' and `po' observations under a particular hypothesis
## with a particular decision about how much is signal
def likelihood_prime(h, surface_counts, real_counts):
    (surface_ka, surface_po) = surface_counts
    (real_ka, real_po) = real_counts
    total = surface_ka + surface_po
    if h == "Hka":
        if real_po != 0:
            likelihood = 0
        else:
            likelihood = (1.0 / ((total + 1.0) * (total + 1.0 - real_ka)))
    elif h == "Hpo":
        if real_ka != 0:
            likelihood = 0
        else:
            likelihood = (1.0 / ((total + 1.0) * (total + 1.0 - real_po)))
    else:
        print("Unknown hypothesis")
    return likelihood

## Likelihood of particular numbers of `ka' and `po' observations under a particular hypothesis
def likelihood(h, surface_counts):
    (surface_ka, surface_po) = surface_counts
    totallikelihood = 0
    for k in range(0,surface_ka+1):
        for p in range(0,surface_po+1):
            totallikelihood += likelihood_prime(h, surface_counts, (k,p))
    return totallikelihood

## Posterior of Hka and Hpo given particular numbers of `ka' and `po' observations
## Assuming equal priors
def posterior_kapo(surface_counts):
    (surface_ka, surface_po) = surface_counts
    (lka, lpo) = (likelihood("Hka",surface_counts),likelihood("Hpo",surface_counts))
    denominator = lka + lpo
    pka = lka / denominator
    ppo = lpo / denominator
    return (pka, ppo)






