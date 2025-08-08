# noisy-grammar-learner

This repository contains data and code for (authors blinded) "Modeling Regularization in Language Acquisition as Noise-Tolerant Grammar Selection", under review. It contains the following:

- datasets: corpora of child-directed speech used as data for the model, with the CHILDES morphological ('mor') tier extracted, and code for tagging np's and v's within these corpora based on recognizable functional elements. This code was written in Python3.

- simulations: code for running model and baseline simulations. This code was written in Python3.

- results: output and analysis scripts for reported model and baseline simulations. This code was written in Python3 and R.

Code was written by (name) and (name). We thank (names) for their assistance with testing these scripts.

----------------------------------------------------------------
INSTRUCTIONS FOR PERFORMING SIMULATIONS

Note: runtime for these scripts is quite long over the 50-sentence datasets (several hours to several days depending on processor).

For the noisy grammar learners:

- Make sure all simulation scripts are located in the same directory. Open a Python interactive shell and import all modules from `gibbs_sampler.py`.
- Call `joint_inference()` on the specific hypothesis space (located in `grammars.py`), the specific dataset (located in `data.py`), and the specific number of iterations. Additional arguments to this function include a descriptor of the run and an optional switch for a trace. The reported simulations used 50,000 iterations.
- For example, the command for one run of the English learner on the 50-sentence Brown dataset would be `joint_inference(word_order_8grammars_hs(), data_brown_final, 50000, "Eng-50")`

For the fully-flexible learners:

- Make sure all simulation scripts are located in the same directory. Open a Python interactive shell and import all modules from `hastings_sampler.py`.
- Call `sample_ts_standalone()` on the specific baseline hypothesis space (locatated in `baselines.py`), the vector of alpha values for the sole grammar in this hypothesis space, the specific dataset (located in `data.py`), the specific number of iterations, and the specific number of chains for parallel tempering. The final argument is a descriptor of the run. The reported simulations used 50,000 iterations and 10 chains of parallel tempering.
- For example, the command for one run of the biased English fully-flexible learner on the 50-sentence Brown dataset would be `sample_ts_standalone(v12hs(), v12hs().alphas[0], data_brown_final, 50000, 10, "Eng-fullyflexible-biased")`

