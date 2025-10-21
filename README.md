# noisy-grammar-learner

This repository contains data and code for Perkins & Hunter "Modeling Regularization in Language Acquisition as Noise-Tolerant Grammar Selection", to appear in _Cognition_. It contains code for running simulations, written in Python3, as well as:

- datasets: corpora of child-directed speech used as data for the model, with the CHILDES morphological ('mor') tier extracted.

- results: output and analysis scripts for reported model and baseline simulations. This code was written in Python3 and R.

Code was written by Laurel Perkins and Tim Hunter. We thank Xinyue Cui, Shalinee Maitra, and Hanyu Zhou for their assistance with testing these scripts.

## Instructions for performing simulations

Note: runtime for these scripts is quite long over the 50-sentence datasets (several hours to several days depending on processor).

For the noisy grammar learners:

- Make sure all simulation scripts are located in the same directory. Open a Python interactive shell and import all modules from `gibbs_sampler.py`.
- Call `joint_inference()` on the specific hypothesis space (located in `grammars.py`), the specific dataset (located in `data.py`), and the specific number of iterations. Additional arguments to this function include a descriptor of the run and an optional switch for a trace. The reported simulations used 50,000 iterations.
- For example, the command for one run of the English learner on the 50-sentence Brown dataset would be `joint_inference(word_order_8grammars_hs(), data_brown_final, 50000, "Eng-50")`

For the fully-flexible learners:

- Make sure all simulation scripts are located in the same directory. Open a Python interactive shell and import all modules from `hastings_sampler.py`.
- Call `sample_ts_standalone()` on the specific baseline hypothesis space (locatated in `baselines.py`), the vector of alpha values for the sole grammar in this hypothesis space, the specific dataset (located in `data.py`), the specific number of iterations, and the specific number of chains for parallel tempering. The final argument is a descriptor of the run. The reported simulations used 50,000 iterations and 10 chains of parallel tempering.
- For example, the command for one run of the biased English fully-flexible learner on the 50-sentence Brown dataset would be `sample_ts_standalone(v12hs(), v12hs().alphas[0], data_brown_final, 50000, 10, "Eng-fullyflexible-biased")`

## Instructions for analyzing CHILDES data into strings of `np` and `v`

Running the following commands in the root directory of this repository will produce (for English, French and Japanese respectively) 
the proportions of string types reported in Table 2:
```
cat datasets/english/brown.txt | python3 tag_by_contexts.py --lang eng --childes
cat datasets/french/lyon.txt | python3 tag_by_contexts.py --lang fre --childes
cat datasets/japanese/miipro.txt | python3 tag_by_contexts.py --lang jpn --childes
```

For the case-marking data in Table 3 from Japanese, add the `--cm` flag:
```
cat datasets/japanese/miipro.txt | python3 tag_by_contexts.py --lang jpn --childes --cm
```
The proportions reported in Table 3 are the result of renormalizing after excluding strings that occur less than ten times.

