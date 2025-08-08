# Key to numbering of simulation output files

These files contain outputs of 10 runs of each simulation. For example, Eng1.1-1.10 are 10 runs of the simulation described as Eng1 below. For space, we did not save files containing sampled trees, but instead saved the processed estimates of theta values created by running `analyze_thetas()` within `postprocessing.py`.

----------------------------------------------------------------

Eng1, Fr1, JapNoCase1

	Fully-flexible, unbiased: flat prior over theta (v14hs)
	50,000 iteration chain with a Gaussian Hastings proposal, sigma=0.25
	Using parallel tempering with 10 chains, temperatures evenly distributed between 0 and 1.0
	Analyzing every 10th sample in last quarter of chain
	Datasets: data_brown_final, data_lyon_final, data_miipro_nocase

----------------------------------------------------------------

Eng2, Fr2, JapNoCase2

	Fully-flexible, biased: skewed prior (alphas = 0.0001) (v12hs)
	50,000 iteration chain with a Gaussian Hastings proposal, sigma=0.25
	Using parallel tempering with 10 chains, temperatures evenly distributed between 0 and 1.0
	Analyzing every 10th sample in last quarter of chain
	Datasets: data_brown_final, data_lyon_final, data_miipro_nocase	

----------------------------------------------------------------

Eng5, Fr5, JapNoCase5

	8 grammars plus noise (word_order_8grammars_hs)
	50,000 iteration chain 
	Analyzing every 10th sample in last quarter of chain
	Datasets: data_brown_final, data_lyon_final, data_miipro_nocase

----------------------------------------------------------------

Eng6, Fr6, JapNoCase6

	9 grammars plus noise (word_order_9grammars_hs)
	50,000 iteration chain 
	Analyzing every 10th sample in last quarter of chain
	Datasets: data_brown_final, data_lyon_final, data_miipro_nocase

----------------------------------------------------------------

Eng7, Fr7, JapNoCase7

	9 grammars plus noise, not requiring subjects in canonical clauses (word_order_subjdrop_hs)
	50,000 iteration chain 
	Analyzing every 10th sample in last quarter of chain
	Datasets: data_brown_final, data_lyon_final, data_miipro_nocase

----------------------------------------------------------------

Eng9-11, Fr9-11, JapNoCase9-11

	8 grammars plus noise (word_order_8grammars_hs), on smaller datasets of varying sizes
	50,000 iteration chain 
	Analyzing every 10th sample in last quarter of chain
	Datasets: 

	9. data_brown_10, data_lyon_10, data_miipro_10
	10. data_brown_30, data_lyon_30, data_miipro_30
	11. data_brown_20, data_lyon_20, data_miipro_20

----------------------------------------------------------------

Eng12-14, Fr12-14, J12-14

	Fully-flexible, biased: skewed prior (alphas = 0.0001) (v12hs), on smaller datasets of varying sizes
	50,000 iteration chain with a Gaussian Hastings proposal, sigma=0.25
	Using parallel tempering with 10 chains, temperatures evenly distributed between 0 and 1.0
	Analyzing every 10th sample in last quarter of chain
	Datasets: 

	12. data_brown_10, data_lyon_10, data_miipro_10
	13. data_brown_20, data_lyon_20, data_miipro_20
	14. data_brown_30, data_lyon_30, data_miipro_30

----------------------------------------------------------------

JapNomAcc

	case-marking of nominative & accusative only, plus noise

	1. Fully-flexible, unbiased: flat prior over theta (v15hs)
	2. Fully-flexible, biased: skewed prior (alphas = 0.0001) (v13hs)
	6. Eight restrictive grammars (word_order_case_hs)
	7. Fully-flexible, unbiased: flat prior over theta, only SOV word order options (v18hs)
	8. Fully-flexible, biased: skewed prior (alphas = 0.0001), only SOV word order options (v19hs)
	9. Two restrictive SOV grammars (case_SOV_hs)

	50,000 iteration chain 
	Analyzing every 10th sample in last quarter of chain
	Dataset: data_miipro_nomacc