from grammars import HypothesisSpace


#########################################################################################################
# (12) flexible biased grammar
def v12hs():
    gALT = ("ALT_sparse_noise",
            # non-noise rules
            [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("S",("NP","S")), ("S",("S","NP")), 
             ("VP",("NP","V")), ("VP",("V","NP")), ("VP",("V",)), ("VP",("NP","VP")), ("VP",("VP","NP")),
             ("NP",("NP","NP")), ("NP","np"), ("V","v")],
            # noise rules
            []
          )
    hs = HypothesisSpace([gALT])
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("NP","VP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("VP","NP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("VP",)), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("NP","S")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("S","NP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("NP","V")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("V","NP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("V",)), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("NP","VP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("VP","NP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NP",("NP","NP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NP","np"), 0.0001)
    return hs

# (13) flexible biased case-marking grammar
def v13hs():
    gALT = ("ALT_sparse_noise",
            # non-noise rules
            [("S",("NPS","VP")), ("S",("VP","NPS")), ("S",("VP",)), ("S",("NPA","S")), ("S",("S","NPA")), 
             ("VP",("NPO","V")), ("VP",("V","NPO")), ("VP",("V",)), ("VP",("NPA","VP")), ("VP",("VP","NPA")), 
             ("NPS",("NPA","NPS")), ("NPS",("NPS","NPA")), ("NPO",("NPA","NPO")), ("NPO",("NPO","NPA")),
             ("NPA",("NPA","NPA")),
             ("NPS","np1"), ("NPO","np2"), ("NPS","np2"), ("NPO","np1"),
             ("NPS","np"), ("NPO","np"),
             ("NPA","np1"), ("NPA","np2"), ("NPA","np"), ("V","v")],
            # noise rules
            []
          )
    hs = HypothesisSpace([gALT])
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("NPS","VP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("VP","NPS")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("VP",)), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("NPA","S")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("S","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("NPO","V")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("V","NPO")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("V",)), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("NPA","VP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("VP","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS",("NPA","NPS")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS",("NPS","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO",("NPA","NPO")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO",("NPO","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA",("NPA","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS","np1"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO","np2"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS","np2"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO","np1"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS","np"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO","np"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA","np1"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA","np2"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA","np"), 0.0001)
    return hs


# (14) flexible unbiased grammar
def v14hs():
    gALT = ("ALT",
            # non-noise rules
            [("S",("NP","VP")), ("S",("VP","NP")), ("S",("VP",)), ("S",("NP","S")), ("S",("S","NP")), 
             ("VP",("NP","V")), ("VP",("V","NP")), ("VP",("V",)), ("VP",("NP","VP")), ("VP",("VP","NP")),
             ("NP",("NP","NP")), ("NP","np"), ("V","v")],
            # noise rules
            []
          )
    return HypothesisSpace([gALT])


# (15) flexible unbiased case-marking grammar
def v15hs():
    gALT = ("ALT",
            # non-noise rules
            [("S",("NPS","VP")), ("S",("VP","NPS")), ("S",("VP",)), ("S",("NPA","S")), ("S",("S","NPA")), 
             ("VP",("NPO","V")), ("VP",("V","NPO")), ("VP",("V",)), ("VP",("NPA","VP")), ("VP",("VP","NPA")), 
             ("NPS",("NPA","NPS")), ("NPS",("NPS","NPA")), ("NPO",("NPA","NPO")), ("NPO",("NPO","NPA")),
             ("NPA",("NPA","NPA")),
             ("NPS","np1"), ("NPO","np2"), ("NPS","np2"), ("NPO","np1"),
             ("NPS","np"), ("NPO","np"),
             ("NPA","np1"), ("NPA","np2"), ("NPA","np"), ("V","v")],
            # noise rules
            []
          )
    return HypothesisSpace([gALT])


    return HypothesisSpace([gALT])

# (18) flexible unbiased case-marking grammar with SOV word order options only
def v18hs():
    gALT = ("ALT_SOV",
            # non-noise rules
            [("S",("NPS","VP")), ("S",("VP",)), ("S",("NPA","S")), ("S",("S","NPA")), 
             ("VP",("NPO","V")), ("VP",("V",)), ("VP",("NPA","VP")), ("VP",("VP","NPA")), 
             ("NPS",("NPA","NPS")), ("NPS",("NPS","NPA")), ("NPO",("NPA","NPO")), ("NPO",("NPO","NPA")),
             ("NPA",("NPA","NPA")),
             ("NPS","np1"), ("NPO","np2"), ("NPS","np2"), ("NPO","np1"),
             ("NPS","np"), ("NPO","np"),
             ("NPA","np1"), ("NPA","np2"), ("NPA","np"), ("V","v")],
            # noise rules
            []
          )
    return HypothesisSpace([gALT])

# (19) flexible biased case-marking grammar with SOV word order options only
def v19hs():
    gALT = ("ALT_sparse_noise",
            # non-noise rules
            [("S",("NPS","VP")), ("S",("VP",)), ("S",("NPA","S")), ("S",("S","NPA")), 
             ("VP",("NPO","V")), ("VP",("V",)), ("VP",("NPA","VP")), ("VP",("VP","NPA")), 
             ("NPS",("NPA","NPS")), ("NPS",("NPS","NPA")), ("NPO",("NPA","NPO")), ("NPO",("NPO","NPA")),
             ("NPA",("NPA","NPA")),
             ("NPS","np1"), ("NPO","np2"), ("NPS","np2"), ("NPO","np1"),
             ("NPS","np"), ("NPO","np"),
             ("NPA","np1"), ("NPA","np2"), ("NPA","np"), ("V","v")],
            # noise rules
            []
          )
    hs = HypothesisSpace([gALT])
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("NPS","VP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("VP",)), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("NPA","S")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("S",("S","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("NPO","V")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("V",)), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("NPA","VP")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("VP",("VP","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS",("NPA","NPS")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS",("NPS","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO",("NPA","NPO")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO",("NPO","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA",("NPA","NPA")), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS","np1"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO","np2"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS","np2"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO","np1"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPS","np"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPO","np"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA","np1"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA","np2"), 0.0001)
    hs.set_nonnoise_alpha("ALT_sparse_noise", ("NPA","np"), 0.0001)
    return hs

