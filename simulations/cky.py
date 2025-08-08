
import random
from collections import defaultdict
from collections import Counter
from functools import reduce

import trees

###############################################################################################

class UnparseableException(Exception):
    pass

rules0 = defaultdict(lambda: 0, {("VP", ("V","NP")):   0.4, 
                                 ("VP", ("VP","PP")):  0.3, 
                                 ("VP", "watches"):    0.2, 
                                 ("VP", "spies"):      0.1, 
                                 ("NP", ("NP","PP")):  0.2, 
                                 ("NP", "watches"):    0.3, 
                                 ("NP", "spies"):      0.2, 
                                 ("NP", "telescopes"): 0.3, 
                                 ("PP", ("P","NP")):   1.0, 
                                 ("V",  "watches"):    1.0, 
                                 ("P",  "with"):       1.0, 
                                })

rules1 = defaultdict(lambda: 0, {("S", ("S-",)):       0.1, 
                                 ("S", ("S+",)):       0.9, 
                                 ("S+", ("VP","NP")):  0.4, 
                                 ("S+", ("NP","VP")):  0.4, 
                                 ("S+", ("VP",)):      0.2, 
                                 ("S-", ("VP","NP")):  0.3, 
                                 ("S-", ("NP","VP")):  0.3, 
                                 ("S-", ("VP",)):      0.4, 
                                 ("VP", ("VP-",)):     0.8, 
                                 ("VP", ("VP+",)):     0.2, 
                                 ("VP+", ("V","NP")):  0.4, 
                                 ("VP+", ("NP","V")):  0.4, 
                                 ("VP+", ("V",)):      0.2, 
                                 ("VP-", ("V","NP")):  0.3, 
                                 ("VP-", ("NP","V")):  0.3, 
                                 ("VP-", ("V",)):      0.4, 
                                 ("NP", "np"):         1.0, 
                                 ("V", "v"):           1.0, 
                                })

rules2 = defaultdict(lambda: 0, {("S", ("NP","VP")):   0.4, 
                                 ("S", ("VP","NP")):   0.4,
                                 ("S", ("VP")):        0.2, 
                                 ("VP", ("V","NP")):   0.4, 
                                 ("VP", ("NP","V")):   0.4, 
                                 ("VP", ("V",)):       0.2, 
                                 ("NP", "np"):         1.0, 
                                 ("V", "v"):           1.0, 
                                })

# graph is a list of pairs where (x,y) represents an edge from x to y
# Kahn's algorithm: https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm
def topological_sort(graph):

    list_of_edges = graph
    nodes = set([n for edge in list_of_edges for n in edge])
    result = []

    s = nodes - set([y for (x,y) in list_of_edges])
    while len(s) > 0:
        n = s.pop()
        result.append(n)
        after_n = [y for (x,y) in list_of_edges if x == n]
        for m in after_n:
            list_of_edges.remove((n,m))
            before_m = [x for (x,y) in list_of_edges if y == m]
            if before_m == []:
                s.add(m)

    if list_of_edges != []:
        assert False, "Graph has a cycle"
    else:
        return result

# ruleprob is a dictionary mapping rules to probabilities (possibly zero)
def inside_chart(ruleprob, string):

    chart = defaultdict(lambda: [])
    nonterms = list(set([lhs for (lhs,rhs) in ruleprob.keys()]))
    seen_substrings = set([])

    # Set up an ordered list of unary rules that respects the topological ordering 
    # amongst nonterminals. The topological_sort function will throw an exception if 
    # the unary rules create cycles.
    unary_rules = [(lhs,rhs) for (lhs,rhs) in ruleprob.keys() if type(rhs) is tuple and len(rhs) == 1]
    nonterms_ordered_by_unaries = topological_sort([(daughter,parent) for (parent,(daughter,)) in unary_rules])
    def rule_sort_key(rule):
        (lhs, rhs) = rule
        try:
            return nonterms_ordered_by_unaries.index(lhs)
        except ValueError:
            return len(nonterms_ordered_by_unaries)
    sorted_unary_rules = [(r, ruleprob[r]) for r in sorted(unary_rules, key=rule_sort_key)]

    # For each diagonal of the CKY chart
    for length in range(1, len(string)+1):

        # For each cell on this diagonal
        for startpos in range(0, len(string)-length+1):

            # This is the substring/infix represented by this cell
            xs = tuple(string[startpos:startpos+length])

            if xs in seen_substrings:
                continue
            seen_substrings.add(xs)

            # First deal with CNF rules
            for ((lhs,rhs),prob) in ruleprob.items():
                if type(rhs) is str and xs == (rhs,):
                    chart[(xs,lhs)].append((None,prob))
                elif type(rhs) is tuple and len(rhs) == 2:
                    (l,r) = rhs
                    for i in range(1,length):
                        daughters_prob = inside_prob(chart, xs[:i], l) * inside_prob(chart, xs[i:], r)
                        if daughters_prob != 0:
                            chart[(xs,lhs)].append(((i,l,r), prob*daughters_prob))

            # Now deal with unary rules (as long as there are no loops)
            for ((lhs,rhs),prob) in sorted_unary_rules:
                (d,) = rhs
                total_prob = prob * inside_prob(chart, xs, d)
                ptr = (length,d)
                if total_prob != 0:
                    chart[(xs,lhs)].append((ptr,total_prob))

    return chart

# Build a CKY chart for the given string, using just a list of (lhs,rhs) pairs, no probabilities.
def nonprob_inside_chart(rulelist, string):

    chart = defaultdict(lambda: [])
    seen_substrings = set([])

    # Set up an ordered list of unary rules that respects the topological ordering 
    # amongst nonterminals. The topological_sort function will throw an exception if 
    # the unary rules create cycles.
    unary_rules = [(lhs,rhs) for (lhs,rhs) in rulelist if type(rhs) is tuple and len(rhs) == 1]
    nonterms_ordered_by_unaries = topological_sort([(daughter,parent) for (parent,(daughter,)) in unary_rules])
    def rule_sort_key(rule):
        (lhs, rhs) = rule
        try:
            return nonterms_ordered_by_unaries.index(lhs)
        except ValueError:
            return len(nonterms_ordered_by_unaries)
    sorted_unary_rules = sorted(unary_rules, key=rule_sort_key)

    # For each diagonal of the CKY chart
    for length in range(1, len(string)+1):

        # For each cell on this diagonal
        for startpos in range(0, len(string)-length+1):

            # This is the substring/infix represented by this cell
            xs = tuple(string[startpos:startpos+length])

            if xs in seen_substrings:
                continue
            seen_substrings.add(xs)

            # First deal with CNF rules
            for (lhs,rhs) in rulelist:
                if type(rhs) is str and xs == (rhs,):
                    chart[(xs,lhs)].append(None)
                elif type(rhs) is tuple and len(rhs) == 2:
                    (l,r) = rhs
                    for i in range(1,length):
                        if chart[(xs[:i],l)] != [] and chart[(xs[i:],r)] != []:
                            chart[(xs,lhs)].append((i,l,r))

            # Now deal with unary rules (as long as there are no loops)
            for (lhs,rhs) in sorted_unary_rules:
                (d,) = rhs
                if chart[(xs,d)] != []:
                    chart[(xs,lhs)].append((length,d))

    return chart

# Enrich a non-probabilistic chart to a probabilistic chart, on the basis of a particular 
# assignment of probabilities to grammar rules.
def add_probs_to_chart(nchart, ruleprob, string):

    pchart = defaultdict(lambda: [])
    nonterms = list(set([lhs for (lhs,rhs) in ruleprob.keys()]))

    unary_rules = [(lhs,rhs) for (lhs,rhs) in ruleprob.keys() if type(rhs) is tuple and len(rhs) == 1]
    nonterms_ordered_by_unaries = topological_sort([(daughter,parent) for (parent,(daughter,)) in unary_rules])
    def nonterm_position(n):
        try:
            return nonterms_ordered_by_unaries.index(n)
        except ValueError:
            return len(nonterms_ordered_by_unaries)
    sorted_all_nonterms = sorted(nonterms, key=nonterm_position)

    # For each diagonal of the CKY chart
    for length in range(1, len(string)+1):

        # For each cell on this diagonal
        for startpos in range(0, len(string)-length+1):

            # This is the substring/infix represented by this cell
            xs = tuple(string[startpos:startpos+length])

            for n in sorted_all_nonterms:
                # print("Working on cell (%s,%s):" % (xs,n))
                for option in nchart[(xs,n)]:
                    if option is None:
                        assert len(xs) == 1
                        (x,) = xs
                        prob = ruleprob[(n,x)]
                    elif len(option) == 3:
                        (i,l,r) = option
                        prob = ruleprob[(n,(l,r))] * inside_prob(pchart, xs[:i], l) * inside_prob(pchart, xs[i:], r)
                    elif len(option) == 2:
                        (i,d) = option
                        prob = ruleprob[(n,(d,))] * inside_prob(pchart, xs, d)
                    else:
                        assert False
                    # print("    For option %s, got probability %f" % (option,prob))
                    if prob != 0:
                        pchart[(xs,n)].append((option,prob))

    return pchart

###############################################################################################

def inside_prob(chart, string, nonterm):
    return sum([prob for (ptr,prob) in chart.get((string,nonterm),[])])

###############################################################################################

def sample_tree_from_chart(chart, string, nonterm):

    chart_entries = chart[(string, nonterm)]
    if chart_entries == []:
        raise UnparseableException("No parse available for string %s, nonterminal %s" % (string, nonterm))

    unzip = lambda x: tuple(zip(*x))    # magic hack!
    (options,weights) = unzip(chart[(string, nonterm)])

    [chosen_one] = random.choices(options, weights)
    if chosen_one is None:
        assert len(string) == 1
        (x,) = string
        return trees.make_tree(nonterm, x)     # leaf node
    else:
        if len(chosen_one) == 3:
            (i,l,r) = chosen_one
            left_daughter = sample_tree_from_chart(chart, string[:i], l)
            right_daughter = sample_tree_from_chart(chart, string[i:], r)
            return trees.make_tree(nonterm, left_daughter, right_daughter)       # binary node
        elif len(chosen_one) == 2:
            (i,d) = chosen_one
            daughter = sample_tree_from_chart(chart, string, d)
            return trees.make_tree(nonterm, daughter)                           # unary node
        else:
            assert False

def extract_trees(chart, string, nonterm):

    chart_entries = chart[(string, nonterm)]
    if chart_entries == []:
        raise UnparseableException("No parse available for string %s, nonterminal %s" % (string, nonterm))

    result = []

    for option in chart_entries:
        if option is None:
            assert len(string) == 1
            (x,) = string
            result.append(trees.make_tree(nonterm,x))       # leaf node
        elif len(option) == 3:
            (i,l,r) = option
            left_daughters = extract_trees(chart, string[:i], l)
            right_daughters = extract_trees(chart, string[i:], r)
            result.extend([trees.make_tree(nonterm, ld, rd) for ld in left_daughters for rd in right_daughters])    # binary node
        elif len(option) == 2:
            (i,d) = option
            daughters = extract_trees(chart, string, d)
            result.extend([trees.make_tree(nonterm, d) for d in daughters])     # unary node
        else:
            assert False

    return result

###############################################################################################

def tester0():

    string = tuple(["watches","spies","with","telescopes","with","telescopes"])

    print("*** Here's the chart:")
    chart = inside_chart(rules0, string)
    for (k,v) in chart.items():
        print(k,v)

    counter = Counter()
    for i in range(10000):
        counter[sample_tree_from_chart(chart, string, "VP")] += 1

    print("*** Here are the trees with frequencies:")
    for (tree,freq) in counter.most_common():
        print(freq, tree)

def tester1():

    string = tuple(["np","v","np"])

    print("*** Here's the chart:")
    chart = inside_chart(rules1, string)
    for (k,v) in chart.items():
        print(k,v)

    counter = Counter()
    for i in range(10000):
        counter[sample_tree_from_chart(chart, string, "S")] += 1

    print("*** Here are the trees with frequencies:")
    product = lambda xs: reduce(lambda x,y: x*y, xs, 1)
    for (tree,freq) in counter.most_common():
        print(freq, prob_t(tree,rules1), product(rules1[r] for r in trees.rewrites(tree)), tree)

def sample_tree(hs, string, ruleprobs):
    ruleset = frozenset([r for (r,p) in ruleprobs.items() if p != 0])
    try:
        nchart = hs.chart_dict[(ruleset,string)]
    except KeyError:
        nchart = nonprob_inside_chart(ruleset, string)
        hs.chart_dict[(ruleset,string)] = nchart
    pchart = add_probs_to_chart(nchart, ruleprobs, string)
    tree = sample_tree_from_chart(pchart, string, "S")
    return tree

def prob_t(t, ruleprobs):
    string = trees.tree_yield(t)
    c = inside_chart(ruleprobs, tuple(string))
    product = lambda xs: reduce(lambda x,y: x*y, xs, 1)
    return product(ruleprobs[r] for r in trees.rewrites(t)) / inside_prob(c, tuple(string), trees.root_symbol(t))

