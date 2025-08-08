import trees
import re
from collections import Counter
import random

# tiny tester treeset
tester_trees =  [trees.make_tree("S", 
                    trees.make_tree("NP","np"), 
                    trees.make_tree("VP",
                        trees.make_tree("V","v"), 
                        trees.make_tree("NP","np")
                    )
                ),
                trees.make_tree("S", 
                    trees.make_tree("NP","np"), 
                    trees.make_tree("VP",
                        trees.make_tree("NP","np"), 
                        trees.make_tree("V","v")
                    )
                ),
                trees.make_tree("S", 
                    trees.make_tree("NP","np"), 
                    trees.make_tree("VP",
                        trees.make_tree("V","v")
                    )
                ),
                trees.make_tree("S", 
                    trees.make_tree("VP",
                        trees.make_tree("V","v"), 
                        trees.make_tree("NP","np")
                    ),
                    trees.make_tree("NP","np") 
                )] 


##################################################################################################
## ENGLISH
## 50-sentence version
data_brown_final =  [["np","v"]]*17 + [["np","v","np"]]*14 + [["v"]]*5 + [["v","np"]]*4 + [["np","v","np","np"]]*3 +   \
                    [["np","np","v"]]*2 + [["np","np","v","np"]]*1 + [["v","np","np"]]*1 + [["np","v","np","np","np"]]*1 + \
                    [["np","np","np","v"]]*1 + [["np","np","np","v","np"]]*1

## 30-sentence version
data_brown_30 =     [["np","v"]]*10 + [["np","v","np"]]*8 + [["v"]]*3 + [["v","np"]]*3 + [["np","v","np","np"]]*2 +   \
                    [["np","np","v"]]*1 + [["np","np","v","np"]]*1 + [["v","np","np"]]*1 + [["np","v","np","np","np"]]*1

## 20-sentence version
data_brown_20 =     [["np","v"]]*7 + [["np","v","np"]]*6 + [["v"]]*2 + [["v","np"]]*2 + [["np","v","np","np"]]*1 +   \
                    [["np","np","v"]]*1 + [["np","np","v","np"]]*1

## 10-sentence version
data_brown_10 =     [["np","v"]]*3 + [["np","v","np"]]*3 + [["v"]]*1 + [["v","np"]]*1 + [["np","v","np","np"]]*1 +   \
                    [["np","np","v"]]*1


##################################################################################################
## FRENCH: 
## 50-sentence version
data_lyon_final = [["np","v"]]*22 + [["np","v","np"]]*10 + [["v"]]*6 + [["np","np","v"]]*4 + [["v","np"]]*2 + \
                  [["np","np","v","np"]]*2 + [["np","v","np","np"]]*2 + [["np","np","np","v"]]*1 + [["v","np","np"]]*1

## 30-sentence version
data_lyon_30 =  [["np","v"]]*13 + [["np","v","np"]]*6 + [["v"]]*4 + [["np","np","v"]]*3 + [["v","np"]]*1 + \
                [["np","np","v","np"]]*1 + [["np","v","np","np"]]*1 + [["np","np","np","v"]]*1

## 20-sentence version
data_lyon_20 =  [["np","v"]]*9 + [["np","v","np"]]*4 + [["v"]]*2 + [["np","np","v"]]*2 + [["v","np"]]*1 + \
                [["np","np","v","np"]]*1 + [["np","v","np","np"]]*1

## 10-sentence version
data_lyon_10 =  [["np","v"]]*4 + [["np","v","np"]]*2 + [["v"]]*1 + [["np","np","v"]]*1 + [["v","np"]]*1 + \
                [["np","np","v","np"]]*1


##################################################################################################

## JAPANESE:
## 50-sentence version
data_miipro_nocase = [["v"]]*32 + [["np","v"]]*11 + [["v","np"]]*3 + [["np","np","v"]]*3 + [["np","v","np"]]*1

## 30-sentence version
data_miipro_30 = [["v"]]*19 + [["np","v"]]*7 + [["v","np"]]*2 + [["np","np","v"]]*1 + [["np","v","np"]]*1

## 20-sentence version
data_miipro_20 = [["v"]]*13 + [["np","v"]]*5 + [["v","np"]]*1 + [["np","np","v"]]*1

## 10-sentence version
data_miipro_10 = [["v"]]*6 + [["np","v"]]*2 + [["v","np"]]*1 + [["np","np","v"]]*1


## case-marked dataset
data_miipro_nomacc = [["np1","v"]]*22 + [["np","np1","v"]]*7 + [["np2","v"]]*7 + [["v","np1"]]*3 + [["np","np2","v"]]*3 + \
                     [["np1","v","np"]]*2 + [["np","np","np1","v"]]*2 + [["np1","np","v"]]*1 + [["np","v","np1"]]*1 + \
                     [["v","np","np1"]]*1 + [["v","np2"]]*1
                     