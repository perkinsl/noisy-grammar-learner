import re
from collections import defaultdict
from collections import Counter

import trees
import cky

class HypothesisSpace:

    # We represent a grammar with a triple: (label, non-noise rules, noise rules).
    # The argument to this constructor is a list of these triples.
    def __init__(self, grammar_list):

        # For each nonterminal, find all the RHS it can be rewritten to, across all grammars, 
        # including noise and non-noise rules.
        # We'll build up a dictionary mapping each nonterminal to a set of RHSs.
        rhss = defaultdict(set)
        for (label, nonnoise_rules, noise_rules) in grammar_list:
            for (lhs,rhs) in (nonnoise_rules + noise_rules):
                rhss[lhs].add(rhs)

        # Now freeze each collection of RHSs in some order
        for nt in rhss.keys():
            rhss[nt] = sorted(rhss[nt], key=hash)
        # And get rid of the defaulting to empty set
        rhss = dict(rhss)

        ds_rules = []
        for nt in rhss.keys():
            ds_rules.append((nt,(self.nonnoise_version(nt),)))
            ds_rules.append((nt,(self.noise_version(nt),)))
            for rhs in rhss[nt]:
                ds_rules.append((self.nonnoise_version(nt),rhs))
            for rhs in rhss[nt]:
                ds_rules.append((self.noise_version(nt),rhs))

        def make_alpha_dict(nonnoise_rules, noise_rules):
            d = {}
            for nt in rhss.keys():
                nonnoise_alphas = [(1 if (nt,rhs) in nonnoise_rules else 0) for rhs in rhss[nt]]
                noise_alphas = [(1 if (nt,rhs) in noise_rules else 0) for rhs in rhss[nt]]
                indicator = lambda b: 1 if b else 0
                d[nt] = [indicator(any(nonnoise_alphas)), indicator(any(noise_alphas))]
                d[self.nonnoise_version(nt)] = nonnoise_alphas
                d[self.noise_version(nt)] = noise_alphas
            return d

        self.ds_rules = ds_rules
        self.alphas = [make_alpha_dict(nnr,nr) for (label,nnr,nr) in grammar_list]
        self.set_legend([label for (label,nnr,nr) in grammar_list])
        self.set_uniform_priors()
        self.ss_rewrites = [(nt,rhs) for nt in rhss.keys() for rhs in rhss[nt]]

        # For memoization: a dictionary whose keys are (alpha,string) pairs, and whose 
        # values are non-probabilistic charts. See sample_tree in cky.py for more details.
        self.chart_dict = {}

    def set_legend(self, labels):
        assert self.alphas is not None
        assert len(self.alphas) == len(labels)
        self.alpha_legend = {label:alpha for (label,alpha) in zip(labels,self.alphas)}

    def set_uniform_priors(self):
        assert self.alphas is not None
        n = len(self.alphas)
        self.priors = [1/n] * n

    def set_nonnoise_alpha(self, glabel, rule, alpha):
        (lhs,rhs) = rule
        rhss = [x for (nt,x) in self.ss_rewrites if nt==lhs]
        assert rhs in rhss
        i = rhss.index(rhs)
        self.alpha_legend[glabel][self.nonnoise_version(lhs)][i] = alpha

    def fix_flat_nonnoise_thetas(self, glabel, nt):
        alpha_vector = self.alpha_legend[glabel][self.nonnoise_version(nt)]
        for i in range(len(alpha_vector)):
            # If this RHS is not completely disallowed, set it the None to indicate flat theta values
            if alpha_vector[i] != 0:
                alpha_vector[i] = None

    def fix_flat_noise_thetas(self, glabel, nt):
        alpha_vector = self.alpha_legend[glabel][self.noise_version(nt)]
        for i in range(len(alpha_vector)):
            # If this RHS is not completely disallowed, set it the None to indicate flat theta values
            if alpha_vector[i] != 0:
                alpha_vector[i] = None

    def convert_ds_to_ss(self, ds_tree):
        remove_plus_minus = lambda x: re.sub(r'(\+|\-)$', '', x)
        return trees.remove_trivial_unaries(trees.map_nonleaf_labels(remove_plus_minus, ds_tree))

    def nonnoise_version(self, nt):
        assert not (nt.endswith("+") or nt.endswith("-"))
        return (nt + "+")

    def noise_version(self, nt):
        assert not (nt.endswith("+") or nt.endswith("-"))
        return (nt + "-")

    def is_nonnoise_nt(self, nt):
        return nt.endswith("+")

    def is_noise_nt(self, nt):
        return nt.endswith("-")

    def lookup_alpha_dict(self, x):
        result = None
        for (label, alpha_dict) in self.alpha_legend.items():
            if alpha_dict == x:
                assert result is None
                result = label
        return result

    def show_trees(self, string, grammar_labels=None):

        if grammar_labels is None:
            grammar_labels = self.alpha_legend.keys()
        else:
            assert all(l in self.alpha_legend for l in grammar_labels)

        tpl = tuple(string.split())

        # dictionary mapping a grammar label to a list of trees
        trees_dict = {}

        for label in grammar_labels:
            alphadict = self.alpha_legend[label]
            rulelist = []  # list of non-probabilistic rules
            for (nonterm, alphavect) in alphadict.items():
                rhss = [rhs for (lhs,rhs) in self.ds_rules if lhs == nonterm]
                assert len(alphavect) == len(rhss)
                for (rhs, alphaval) in zip(rhss, alphavect):
                    if alphaval != 0:
                        rulelist.append((nonterm,rhs))
            chart = cky.nonprob_inside_chart(rulelist, tpl)
            trees_dict[label] = cky.extract_trees(chart, tpl, "S")

        shared_trees = None
        for ts in trees_dict.values():
            if shared_trees is None:
                shared_trees = set(ts)
            else:
                shared_trees.intersection_update(ts)

        def rewrite_breakdown(t):
            rewrites = trees.rewrites(t)
            nonnoise = [lhs for (lhs,rhs) in rewrites if self.is_nonnoise_nt(lhs)]
            noise = [lhs for (lhs,rhs) in rewrites if self.is_noise_nt(lhs)]
            return (nonnoise, noise)

        def keyfn(pair):
            (t, (nonnoise_list,noise_list)) = pair
            nonnoise_count = len(nonnoise_list)
            noise_count = len(noise_list)
            return (nonnoise_count + noise_count, noise_count, noise_list, nonnoise_list, trees.to_string(t))

        def print_trees(label, ts):
            with_counts = [(t, rewrite_breakdown(t)) for t in ts]
            for (i,(t,breakdown)) in enumerate(sorted(with_counts, key=keyfn)):
                (nonnoise, noise) = breakdown
                print("%s %2d\t%2d rewrites\t%-24s\t%-16s\t%s" % (label, i+1, len(nonnoise+noise), ",".join(noise), ",".join(nonnoise), trees.to_string(t)))

        print()
        print_trees("shared", shared_trees)
        print()
        for (label, ts) in trees_dict.items():
            print_trees(label, [t for t in ts if t not in shared_trees])
            print()

#################################################################
## Word order learner
## Hypothesis space includes probabilities for 4 additional more flexible word orders,
## Posterior distribution over 4 strict word orders can be found by re-normalizing
def word_order_8grammars_hs():

    shared_nonnoise_rules = [("VP",("V",)), ("NP","np"), ("V","v")]
    shared_noise_rules = [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("S",("NP","S")), ("S",("S","NP")), 
                          ("VP",("NP","V")), ("VP",("V","NP")), ("VP",("V",)), ("VP",("NP","VP")), ("VP",("VP","NP")),
                          ("NP",("NP","NP")), ("NP","np"), ("V","v")]
    gSOV = ("SOV", [("S",("NP","VP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gSVO = ("SVO", [("S",("NP","VP")), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gOVS = ("OVS", [("S",("VP","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVOS = ("VOS", [("S",("VP","NP")), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gSV = ("SV", [("S",("NP","VP")), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVS = ("VS", [("S",("VP","NP")), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gOV = ("OV", [("S",("NP","VP")), ("S",("VP","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVO = ("VO", [("S",("NP","VP")), ("S",("VP","NP")), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)

    return HypothesisSpace([gSOV, gSVO, gOVS, gVOS, gSV, gVS, gOV, gVO])

## Word order learner including the 'FREE' grammar along with other 8
def word_order_9grammars_hs():

    shared_nonnoise_rules = [("VP",("V",)), ("NP","np"), ("V","v")]
    shared_noise_rules = [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("S",("NP","S")), ("S",("S","NP")), 
                          ("VP",("NP","V")), ("VP",("V","NP")), ("VP",("V",)), ("VP",("NP","VP")), ("VP",("VP","NP")),
                          ("NP",("NP","NP")), ("NP","np"), ("V","v")]
    gSOV = ("SOV", [("S",("NP","VP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gSVO = ("SVO", [("S",("NP","VP")), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gOVS = ("OVS", [("S",("VP","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVOS = ("VOS", [("S",("VP","NP")), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gSV = ("SV", [("S",("NP","VP")), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVS = ("VS", [("S",("VP","NP")), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gOV = ("OV", [("S",("NP","VP")), ("S",("VP","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVO = ("VO", [("S",("NP","VP")), ("S",("VP","NP")), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gFREE = ("FREE", [("S",("NP","VP")), ("S",("VP","NP")), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)

    return HypothesisSpace([gSOV, gSVO, gOVS, gVOS, gSV, gVS, gOV, gVO, gFREE])

## Word order learner that does not require subjects in canonical clauses
def word_order_subjdrop_hs():

    shared_nonnoise_rules = [("VP",("V",)), ("NP","np"), ("V","v")]
    shared_noise_rules = [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("S",("NP","S")), ("S",("S","NP")), 
                          ("VP",("NP","V")), ("VP",("V","NP")), ("VP",("V",)), ("VP",("NP","VP")), ("VP",("VP","NP")),
                          ("NP",("NP","NP")), ("NP","np"), ("V","v")]
    gSOV = ("SOV", [("S",("NP","VP")), ("S",("VP",)), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gSVO = ("SVO", [("S",("NP","VP")), ("S",("VP",)), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gOVS = ("OVS", [("S",("VP","NP")), ("S",("VP",)), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVOS = ("VOS", [("S",("VP","NP")), ("S",("VP",)), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gSV = ("SV", [("S",("NP","VP")), ("S",("VP",)), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVS = ("VS", [("S",("VP","NP")), ("S",("VP",)), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gOV = ("OV", [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)
    gVO = ("VO", [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("VP",("V","NP"))] + shared_nonnoise_rules, shared_noise_rules)
    gFREE = ("FREE", [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("VP",("V","NP")), ("VP",("NP","V"))] + shared_nonnoise_rules, shared_noise_rules)

    return HypothesisSpace([gSOV, gSVO, gOVS, gVOS, gSV, gVS, gOV, gVO, gFREE])

## Case-marking learner
def word_order_case_hs():

    shared_nonnoise_rules = [("VP",("V",)), ("V","v"), ("NPA","np")]
    shared_noise_rules = [("S",("NPS","VP")), ("S",("VP","NPS")), ("S",("VP",)), ("S",("NPA","S")), ("S",("S","NPA")), 
                          ("VP",("NPO","V")), ("VP",("V","NPO")), ("VP",("V",)), ("VP",("NPA","VP")), ("VP",("VP","NPA")), 
                          ("NPS",("NPA","NPS")), ("NPS",("NPS","NPA")), ("NPO",("NPA","NPO")), ("NPO",("NPO","NPA")),
                          ("NPA",("NPA","NPA")),
                          ("NPS","np1"), ("NPO","np2"), ("NPS","np2"), ("NPO","np1"),
                          ("NPS","np"), ("NPO","np"),
                          ("NPA","np1"), ("NPA","np2"), ("NPA","np"),
                          ("V","v")]
    gSOV_12 = ("SOV_12", [("S",("NPS","VP")), ("VP",("NPO","V")), ("NPS","np1"), ("NPO","np2")] + shared_nonnoise_rules, shared_noise_rules)
    gSOV_21 = ("SOV_21", [("S",("NPS","VP")), ("VP",("NPO","V")), ("NPS","np2"), ("NPO","np1")] + shared_nonnoise_rules, shared_noise_rules)
    gSVO_12 = ("SVO_12", [("S",("NPS","VP")), ("VP",("V","NPO")), ("NPS","np1"), ("NPO","np2")] + shared_nonnoise_rules, shared_noise_rules)
    gSVO_21 = ("SVO_21", [("S",("NPS","VP")), ("VP",("V","NPO")), ("NPS","np2"), ("NPO","np1")] + shared_nonnoise_rules, shared_noise_rules)
    gOVS_12 = ("OVS_12", [("S",("VP","NPS")), ("VP",("NPO","V")), ("NPS","np1"), ("NPO","np2")] + shared_nonnoise_rules, shared_noise_rules)
    gOVS_21 = ("OVS_21", [("S",("VP","NPS")), ("VP",("NPO","V")), ("NPS","np2"), ("NPO","np1")] + shared_nonnoise_rules, shared_noise_rules)
    gVOS_12 = ("VOS_12", [("S",("VP","NPS")), ("VP",("V","NPO")), ("NPS","np1"), ("NPO","np2")] + shared_nonnoise_rules, shared_noise_rules)
    gVOS_21 = ("VOS_21", [("S",("VP","NPS")), ("VP",("V","NPO")), ("NPS","np2"), ("NPO","np1")] + shared_nonnoise_rules, shared_noise_rules)
 
    return HypothesisSpace([gSOV_12, gSOV_21, gSVO_12, gSVO_21, gOVS_12, gOVS_21, gVOS_12, gVOS_21])

## Version of the same case-marking learner with only 2 SOV word order options
def case_SOV_hs():

    shared_nonnoise_rules = [("VP",("V",)), ("V","v"), ("NPA","np"),("S",("NPS","VP")), ("VP",("NPO","V"))]
    shared_noise_rules = [("S",("NPS","VP")), ("S",("VP",)), ("S",("NPA","S")), ("S",("S","NPA")), 
                          ("VP",("NPO","V")), ("VP",("V",)), ("VP",("NPA","VP")), ("VP",("VP","NPA")), 
                          ("NPS",("NPA","NPS")), ("NPS",("NPS","NPA")), ("NPO",("NPA","NPO")), ("NPO",("NPO","NPA")),
                          ("NPA",("NPA","NPA")),
                          ("NPS","np1"), ("NPO","np2"), ("NPS","np2"), ("NPO","np1"),
                          ("NPS","np"), ("NPO","np"),
                          ("NPA","np1"), ("NPA","np2"), ("NPA","np"),
                          ("V","v")]
    gSOV_12 = ("SOV_12", [("NPS","np1"), ("NPO","np2")] + shared_nonnoise_rules, shared_noise_rules)
    gSOV_21 = ("SOV_21", [("NPS","np2"), ("NPO","np1")] + shared_nonnoise_rules, shared_noise_rules)
 
    return HypothesisSpace([gSOV_12, gSOV_21])
