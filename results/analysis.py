## Analyses on outputs of Gibbs and Hastings samplers: sampled alphas (grammars) and sampled trees

import math
import numpy as np
from grammars import *
from baselines import *
from likelihood import *
import pandas as pd
import ast
from trees import *
from cky import *
from data import *

## Analyze grammars (alphas) by reading in samples from .txt file
## Requires paths to two files that are output of Gibbs sampler:
## alpha_path: file containing sampled alpha vectors
## legend_path: saved 'legend' mapping alpha vectors to particular grammars
def analyze_alphas(alpha_path, legend_path):

    with open(alpha_path) as alpha_f:
          alpha_data = alpha_f.read().splitlines()

    ## Analyze every 10th sample from last quarter of chain
    thinned_alphas = alpha_dicts[-round(len(alpha_data)/4)::10]

    ## Create a dataframe with columns corresponding to grammar and parameter value at each sample
    ## Need to use saved alpha legend in order to interpret sampled alpha vectors
    with open(legend_path) as legend_f:
        legend_data = legend_f.read().splitlines()

    alpha_legend = [ast.literal_eval(s) for s in legend_data]
    hs_ivd = {str(v): k for k, v in alpha_legend}

    a_samples = pd.DataFrame.from_dict(thinned_alphas)
    g_samples = list(map(lambda x: hs_ivd.get(str(x)), thinned_alphas))
    g_summary = pd.get_dummies(g_samples, dtype=float)

    a_samples = pd.concat([a_samples, g_summary], axis = 1)

    ## Dataframe showing means for each grammar and each parameter setting for this set of samples
    ## Along with other less useful descriptive stats
    a_summary = a_samples[list(g_summary.keys())].describe().round(4)

    ## Examining convergence: split second half of chain into third and forth quarters
    a_Q3 = a_samples.loc[0:int(len(a_samples)/2-1)]
    a_Q4 = a_samples.loc[int(len(a_samples)/2):]
    Q3_summary = a_Q3[list(g_summary.keys())].describe().round(4)
    Q4_summary = a_Q4[list(g_summary.keys())].describe().round(4)

    return(a_summary, Q3_summary, Q4_summary)


## Analyze ML estimates of thetas from trees by reading in samples from .txt file
## Requires paths to two files that are output of Hastings sampler:
## t_path: file containing sampled trees
## rewrite_path: file containing list of rewrites in trees
def analyze_thetas(t_path, rewrite_path, output_path):

    pd.options.display.max_columns = None
    
    with open(t_path) as t_f:
          t_data = t_f.read().splitlines()

    ## Analyze every 10th sample from last quarter of chain
    thinned_tdata = t_data[-round(len(t_data)/4)::10]

    with open(rewrite_path) as rewrite_f:
        rewrite_data = rewrite_f.read().splitlines()
    ss_rewrites = [ast.literal_eval(s) for s in rewrite_data]

    ts = [list(ast.literal_eval(l.replace(') (', '), ('))) for l in thinned_tdata]
    t_counts = [count_ss_rewrites(ss_rewrites, l) for l in ts]

    ## ML estimate of theta from these (s-structure) rule counts
    def estimate_theta(rewrite_counts, parent_counts):
      nonterms = [rule[0] for rule in list(rewrite_counts.keys())]
      theta = {}
      for (rule, count) in rewrite_counts.items():
        if parent_counts.get(rule[0]) != 0:
          theta[rule] = (float(count))/float(parent_counts.get(rule[0]))
        else:
          theta[rule] = 0.0
      return theta

    ## Create a dataframe with columns corresponding to theta estimates at each sample
    t_samples = pd.DataFrame.from_dict([r for (r,p) in t_counts])
    theta_list = [estimate_theta(r,p) for (r,p) in t_counts]
    theta_samples = pd.DataFrame.from_dict(theta_list)
    theta_samples.to_csv(output_path)

    ## Summarize mean along with other less useful descriptive stats
    theta_summary = theta_samples.describe().round(4)

    ## Examining convergence: split sample into first and second half
    theta_Q3 = theta_samples.loc[0:int(len(theta_samples)/2-1)]
    theta_Q4 = theta_samples.loc[int(len(theta_samples)/2):]
    Q3_summary = theta_Q3.describe().round(4)
    Q4_summary = theta_Q4.describe().round(4)

    return(theta_summary, Q3_summary, Q4_summary, t_samples)


## Analyze bottom-up probabilities of case-markers by reading in samples from .txt file
## Requires original dataset as argument, as well as path to output file of Hastings sampler:
## t_path: file containing sampled trees
def analyze_case(t_path, dataset, output_path):

    pd.options.display.max_columns = None
    
    with open(t_path) as t_f:
          t_data = t_f.read().splitlines()

    ## Analyze every 10th sample from last quarter of chain
    thinned_tdata = t_data[-round(len(t_data)/4)::10]

    ## Count rewrites of only the terminal np rules
    nps = ['np','np1','np2']
    nonterms = ['NPS','NPO','NPA']
    ss_rewrites = [('NPS', 'np'), ('NPS', 'np1'), ('NPS', 'np2'),
                   ('NPO', 'np'), ('NPO', 'np1'), ('NPO', 'np2'),
                   ('NPA', 'np'), ('NPA', 'np1'), ('NPA', 'np2')]
    ts = [list(ast.literal_eval(l.replace(') (', '), ('))) for l in thinned_tdata]
    t_counts = [count_ss_rewrites(ss_rewrites, l) for l in ts]
    np_counts = {np:sum([s.count(np) for s in dataset]) for np in nps}

    ## ML estimate of bottom-up probabilities from these rule counts
    def estimate_npprobs(rewrite_counts, np_counts):
      return {rule:(float(count)/float(np_counts.get(rule[1]))) for (rule, count) in rewrite_counts.items()}

    ## Create a dataframe with columns corresponding to np prob estimates at each sample
    t_samples = pd.DataFrame.from_dict([r for (r,p) in t_counts])
    pr_list = [estimate_npprobs(r,np_counts) for (r,p) in t_counts]
    pr_samples = pd.DataFrame.from_dict(pr_list)
    pr_samples.to_csv(output_path)

    ## Summarize mean along with other less useful descriptive stats
    pr_summary = pr_samples.describe().round(4)

    ## Examining convergence: split sample into first and second half
    pr_Q3 = pr_samples.loc[0:int(len(pr_samples)/2-1)]
    pr_Q4 = pr_samples.loc[int(len(pr_samples)/2):]
    Q3_summary = pr_Q3.describe().round(4)
    Q4_summary = pr_Q4.describe().round(4)

    return(pr_summary, Q3_summary, Q4_summary, t_samples)

