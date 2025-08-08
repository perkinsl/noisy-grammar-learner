#!/usr/bin/env python3

import sys
import re
import argparse
import itertools
from collections import Counter, defaultdict

import trees

class LangInfo:
    pass

langinfodict = {}

######################################################################
### English

ENG = "eng"
langinfodict[ENG] = LangInfo()

langinfodict[ENG].initial_tagger = {
    "you"            : "prn",           #   21482    you               Counter({'pro:per': 21481, '0pro:per': 1})
    "be&3S"          : "fun",           #   16064    be&3S             Counter({'cop': 13848, 'aux': 2216})
    "what"           : "fun",           #   11708    what              Counter({'pro:int': 11708})
    "the"            : "det",           #   10780    the               Counter({'det:art': 10780})
    "it"             : "prn",           #   10485    it                Counter({'pro:per': 10485})
    "that"           : "fun",           #    9616    that              Counter({'pro:dem': 6562, 'comp': 1071, 'det:dem': 744, 'pro:rel': 680, 'adv': 559})
    "-s"             : "nsuf",          #    9233    -s                Counter({None: 9233})
    "a"              : "det",           #    9114    a                 Counter({'det:art': 8944, 'n:let': 170})
    "not"            : "neg",           #    8932    not               Counter({'neg': 8932})
    "do"             : "aux",           #    8028    do     ?          Counter({'mod': 5845, 'v': 2183})
    "I"              : "prn",           #    7301    I                 Counter({'pro:sub': 7300, 'meta': 1})
    "to"             : "fun",           #    7138    to                Counter({'inf': 5291, 'prep': 1847})
    "be&PRES"        : "fun",           #    5210    be&PRES           Counter({'aux': 2660, 'cop': 2550})
    "-ing"           : "vsuf",          #    5026    -ing              Counter({None: 5026})
    "no"             : "fun",           #    3969    no                Counter({'co': 3450, 'qn': 518, 'meta': 1})
    "and"            : "fun",           #    3869    and               Counter({'coord': 3869})
    "oh"             : "fun",           #    3748    oh                Counter({'co': 3747, 'meta': 1})
    "your"           : "det",           #    3719    your              Counter({'det:poss': 3719})
    "in"             : "fun",           #    3512    in                Counter({'prep': 3082, 'adv': 430})
    "have"           : None,            #    3317    have              Counter({'v': 2074, 'aux': 630, 'mod': 613})
    "on"             : "fun",           #    3138    on                Counter({'prep': 2351, 'adv': 787})
    "do&PAST"        : "aux",           #    3071    do&PAST           Counter({'mod': 2564, 'v': 507})
    "he"             : "prn",           #    2659    he                Counter({'pro:sub': 2659})
    "yeah"           : "fun",           #    2532    yeah              Counter({'co': 2532})
    "there"          : "fun",           #    2518    there             Counter({'adv': 1226, 'n': 789, 'pro:exist': 503})
    "will"           : "aux",           #    2480    will              Counter({'mod': 2480})
    "this"           : "fun",           #    2478    this              Counter({'pro:dem': 1504, 'det:dem': 974})
    "can"            : "aux",           #    2427    can               Counter({'mod': 2362, 'n': 65})
    "one"            : "fun",           #    2384    one               Counter({'pro:indef': 1571, 'det:num': 810, 'qn': 3})
    "she"            : "prn",           #    2303    she               Counter({'pro:sub': 2303})
    "go-PRESP"       : None,            #    2171    go-PRESP          Counter({'part': 2161, 'n:gerund': 10})
    "like"           : None,            #    2104    like              Counter({'v': 828, 'prep': 665, 'conj': 322, 'co': 289})
    "here"           : "fun",           #    2090    here              Counter({'adv': 1225, 'n': 592, 'pro:exist': 273})
    "see"            : None,            #    2062    see               Counter({'v': 1924, 'co': 138})
    "yes"            : "fun",           #    2007    yes               Counter({'co': 2006, 'meta': 1})
    "-ed"            : "vsuf",          #    2006    -ed               Counter({None: 2006})
    "where"          : "fun",           #    1916    where             Counter({'pro:int': 1392, 'pro:rel': 524})
    "know"           : None,            #    1898    know              Counter({'v': 1898})
    "of"             : "fun",           #    1744    of                Counter({'prep': 1744})
    "me"             : "prn",           #    1708    me                Counter({'pro:obj': 1708})
    "for"            : "fun",           #    1693    for               Counter({'prep': 1683, 'conj': 10})
    "we"             : "prn",           #    1671    we                Counter({'pro:sub': 1671})
    "want"           : None,            #    1645    want              Counter({'v': 1645})
    "go"             : None,            #    1639    go                Counter({'v': 1639})
    "put&ZERO"       : None,            #    1634    put&ZERO          Counter({'v': 1634})
    "with"           : "fun",           #    1612    with              Counter({'prep': 1612})
    "think"          : None,            #    1566    think             Counter({'v': 1566})
    "they"           : "prn",           #    1474    they              Counter({'pro:sub': 1474})
    "get"            : None,            #    1449    get               Counter({'v': 1349, 'aux': 100})
    "right"          : "fun",           #    1438    right             Counter({'co': 741, 'adv': 515, 'adj': 139, 'n': 43})
    "up"             : "fun",           #    1403    up                Counter({'adv': 1135, 'prep': 261, 'n|+v|make+prep': 5, 'n|+v|check+prep': 1, 'n|+v|push+prep': 1})
    "how"            : "fun",           #    1393    how               Counter({'pro:int': 1205, 'pro:rel': 188})
    "well"           : "fun",           #    1393    well              Counter({'co': 1253, 'adv': 94, 'n': 46})
    "do&3S"          : "aux",           #    1384    do&3S             Counter({'mod': 1120, 'v': 264})
    "Sarah"          : "nam",           #    1329    Sarah             Counter({'n:prop': 1328, 'meta': 1})
    "now"            : "fun",           #    1292    now               Counter({'adv': 1292})
    "Adam"           : "nam",           #    1291    Adam              Counter({'n:prop': 1290, 'meta': 1})
    "why"            : "fun",           #    1281    why               Counter({'pro:int': 906, 'pro:rel': 375})
    "huh"            : "fun",           #    1261    huh               Counter({'co': 1261})
    "who"            : "fun",           #    1259    who               Counter({'pro:int': 787, 'pro:rel': 472})
    "be&PAST&13S"    : "fun",           #    1242    be&PAST&13S       Counter({'cop': 960, 'aux': 282})
    "all"            : "fun",           #    1240    all               Counter({'adv': 498, 'qn': 456, 'post': 148, 'pro:indef': 138})
    "out"            : "fun",           #    1089    out               Counter({'adv': 852, 'prep': 227, 'n': 4, 'n|+v|blow+prep': 3, 'n|+v|cook+prep': 3})
    "her"            : "fun",           #    1087    her               Counter({'pro:obj': 561, 'det:poss': 526})
    "alright"        : "fun",           #    1078    alright           Counter({'co': 914, 'adj': 164})
    "be"             : "fun",           #    1076    be                Counter({'cop': 875, 'aux': 191, 'v': 10})
    "down"           : "fun",           #    1057    down              Counter({'adv': 799, 'prep': 233, 'n': 19, 'v': 3, 'adv|+n|upside+prep': 3})
    "them"           : "prn",           #    1048    them              Counter({'pro:obj': 1048})
    "just"           : "fun",           #    1027    just              Counter({'adv': 891, 'adj': 136})
    "come"           : None,            #    1011    come              Counter({'v': 1011})
    "look"           : None,            #     901    look              Counter({'v': 804, 'co': 95, 'cop': 2})
    "little"         : None,            #     895    little            Counter({'adj': 895})
    "at"             : "fun",           #     882    at                Counter({'prep': 882})
    "do-PRESP"       : None,            #     871    do-PRESP          Counter({'part': 855, 'n:gerund': 16})
    "some"           : "det",           #     856    some              Counter({'qn': 810, 'pro:indef': 46})
    "good"           : None,            #     843    good              Counter({'adj': 843})
    "so"             : "fun",           #     836    so                Counter({'adv': 399, 'co': 327, 'conj': 110})
    "okay"           : "fun",           #     830    okay              Counter({'co': 768, 'adj': 62})
    "be&1S"          : "fun",           #     803    be&1S             Counter({'cop': 402, 'aux': 401})
    "hm"             : "fun",           #     800    hm                Counter({'co': 800})
    "if"             : "fun",           #     797    if                Counter({'conj': 690, 'comp': 107})
    "say"            : None,            #     795    say               Counter({'v': 730, 'co': 65})
    "when"           : "fun",           #     765    when              Counter({'conj': 685, 'pro:rel': 54, 'pro:int': 26})
    "will&COND"      : "aux",           #     763    will&COND         Counter({'mod': 763})
    "about"          : None,            #     762    about             Counter({'prep': 497, 'adv': 265})
    "my"             : "det",           #     753    my                Counter({'det:poss': 724, 'co': 29})
    "mhm=yes"        : "fun",           #     749    mhm=yes           Counter({'co': 749})
    "over"           : None,            #     747    over              Counter({'prep': 421, 'adv': 326})
    "take"           : None,            #     741    take              Counter({'v': 740, 'meta': 1})
    "too"            : "fun",           #     729    too               Counter({'adv': 600, 'post': 129})
    "two"            : "fun",           #     727    two               Counter({'det:num': 726, 'meta': 1})
    "his"            : "det",           #     712    his               Counter({'det:poss': 709, 'pro:poss': 3})
    "tell"           : None,            #     711    tell              Counter({'v': 711})
    "big"            : None,            #     694    big               Counter({'adj': 694})
    "make"           : None,            #     678    make              Counter({'v': 678})
    "get&PAST"       : None,            #     666    get&PAST          Counter({'v': 640, 'aux': 26})
    "back"           : None,            #     651    back              Counter({'adv': 472, 'n': 124, 'adj': 51, 'v': 4})
    "him"            : "prn",           #     610    him               Counter({'pro:obj': 610})
    "because"        : None,            #     601    because           Counter({'conj': 601})
    "Eve"            : "nam",           #     596    Eve               Counter({'n:prop': 596})
}

def eng_add_tags_from_cues(x):

    for i in range(len(x)):

        if x[i].guess_tag is None:

            # Choose a candidate tag, candidate1, based on what precedes x[i]
            if i >= 1 and x[i-1].guess_tag == "det":
                candidate1 = "noun"
            elif i >= 1 and x[i-1].guess_tag == "aux":
                candidate1 = "verb"
            elif i >= 2 and x[i-2].guess_tag == "aux" and x[i-1].guess_tag == "neg":
                candidate1 = "verb"
            else:
                candidate1 = None

            # Choose a candidate tag, candidate2, based on what follows x[i]
            if i+1 < len(x) and x[i+1].guess_tag == "nsuf":
                candidate2 = "noun"
            elif i+1 < len(x) and x[i+1].guess_tag == "vsuf":
                candidate2 = "verb"
            else:
                candidate2 = None

            candidates = set([c for c in [candidate1,candidate2] if c is not None])
            if len(candidates) == 1:
                x[i].guess_tag = candidates.pop()

langinfodict[ENG].add_tags_from_cues = eng_add_tags_from_cues

def eng_try_split_suffixes(plain_w, pos, gloss):
    m = re.match(r'(.*)(-[0-9A-Z]+)', gloss)
    if m is not None:
        if plain_w[-1] == "s":
            tw1 = TaggedWord(gloss, pos)
            tw2 = TaggedWord("-s")
            return [tw1, tw2]
        elif plain_w[-2:] == "ed":
            tw1 = TaggedWord(gloss, pos)
            tw2 = TaggedWord("-ed")
            return [tw1, tw2]
        elif plain_w[-3:] == "ing":
            tw1 = TaggedWord(gloss, pos)
            tw2 = TaggedWord("-ing")
            return [tw1, tw2]
    else:
        return None

langinfodict[ENG].try_split_suffixes = eng_try_split_suffixes

######################################################################

######################################################################
### French

FRE = "fre"
langinfodict[FRE] = LangInfo()

langinfodict[FRE].initial_tagger = {
    "tu"             : "prn",           #       18387    tu                      Counter({'pro:sub': 18387})
    "être&PRES&3s"   : "fun",           #       17865    être&PRES&3s            Counter({'v:aux': 15226, 'v:exist': 2635, '0v:aux': 3, '0v:exist': 1})
    "ce"             : "fun",           #       15323    ce                      Counter({'pro:dem': 15322, '0pro:dem': 1})
    "que"            : "fun",           #       12534    que                     Counter({'pro:rel': 4422, 'adv': 3477, 'pro:int': 3126, 'prep': 1148, '0adv': 288, 'conj': 58, '0prep': 9, '0pro:int': 3, '0pro:rel': 2, '0conj': 1})
    "ça"             : "prn",           #       11430    ça                      Counter({'pro:dem': 11427, '0pro:dem': 3})
    "le&m&sg"        : "det",           #        8788    le&m&sg                 Counter({'det:art': 8782, '0det:art': 6})
    "-e"             : "vsuf",          #        8728    -e                      Counter({None: 8728})
    "il"             : "prn",           #        8685    il                      Counter({'pro:sub': 8377, '0pro:sub': 300, 'pro': 8})
    "là"             : "fun",           #        8129    là                      Counter({'adv:place': 8127, 'prep': 1, '0adv:place': 1})
    "pas"            : "neg",           #        7419    pas                     Counter({'neg': 7419})
    "je"             : "prn",           #        6485    je                      Counter({'pro:sub': 6482, '0pro:sub': 3})
    "un&m&sg"        : "det",           #        6407    un&m&sg                 Counter({'det:art': 6259, 'pro': 148})
    "on"             : "prn",           #        6381    on                      Counter({'pro:sub': 6374, '0pro:sub': 6, 'L2': 1})
    "cm"             : "fun",           #        6327    cm                      Counter({'cm': 6327})
    "et"             : "fun",           #        6258    et                      Counter({'conj': 6242, '0conj': 16})
    "la&f&sg"        : "fun",           #        6060    la&f&sg                 Counter({'det:art': 6059, '0det:art': 1})
    "de"             : "fun",           #        5863    de                      Counter({'prep': 5673, 'adv': 177, '0prep': 8, 'uni': 5})
    "ah"             : "fun",           #        5591    ah                      Counter({'co': 5591})
    "oui=yes"        : "fun",           #        5275    oui=yes                 Counter({'co': 5275})
    "avoir&PRES&3s"  : "fun",           #        4899    avoir&PRES&3s           Counter({'v:aux': 4651, 'v:poss': 245, '0v:aux': 3})
    "non=no"         : "fun",           #        4882    non=no                  Counter({'co': 4882})
    "le"             : "det",           #        4790    le                      Counter({'det:art': 2429, 'pro:obj': 2352, 'pro': 8, '0pro:obj': 1})
    "hein"           : "fun",           #        4520    hein                    Counter({'co': 4520})
    "y"              : "fun",           #        4204    y                       Counter({'pro:y': 4198, '0pro:y': 3, 'n:let': 2, 'on': 1})
    "les&pl"         : "det",           #        4095    les&pl                  Counter({'det:art': 4094, '0det:art': 1})
    "est–ce"         : "fun",           #        3993    est–ce                  Counter({'v:int': 3993})
    "oh"             : "fun",           #        3579    oh                      Counter({'co': 3579})
    "à"              : "fun",           #        3440    à                       Counter({'prep': 3438, '0prep': 2})
    "vouloir&PRES&12s" : None,          #        3401    vouloir&PRES&12s        Counter({'v:mdl': 3254, 'v:mdllex': 142, 're#v:mdl': 5})
    "aller&PRES&3s"  : "aux",           #        3381    aller&PRES&3s           Counter({'v:mdl': 3365, 'v:mdllex': 15, '0v:mdl': 1})
    "te"             : "fun",           #        3259    te                      Counter({'pro:obj': 3256, '0pro:obj': 3})
    "avoir&PRES&2s"  : "fun",           #        3184    avoir&PRES&2s           Counter({'v:aux': 2607, 'v:poss': 576, '0v:aux': 1})
    "une&f&sg"       : "det",           #        3030    une&f&sg                Counter({'det:art': 2958, 'pro': 72})
    "alors"          : "fun",           #        2989    alors                   Counter({'adv': 2972, 'conj': 17})
    "voilà"          : "fun",           #        2884    voilà                   Counter({'adv:place': 2098, 'co': 786})
    "en"             : "fun",           #        2833    en                      Counter({'pro:y': 1534, 'prep': 1297, '0prep': 1, '0pro:y': 1})
    "elle"           : "prn",           #        2774    elle                    Counter({'pro:sub': 2766, '0pro:sub': 6, 'pro': 2})
    "qui"            : "fun",           #        2539    qui                     Counter({'pro:int': 2180, 'pro:rel': 359})
    "faire-PP&m"     : None,            #        2477    faire-PP&m              Counter({'part': 2445, 're#part': 16, 'dé#part': 16})
    "comme"          : "fun",           #        2367    comme                   Counter({'adv': 1975, 'prep': 382, 'conj': 10})
    "mais"           : "fun",           #        2291    mais                    Counter({'adv': 2279, 'conj': 9, '0adv': 2, 'none': 1})
    "quoi"           : "fun",           #        2248    quoi                    Counter({'pro:int': 1353, 'pro:rel': 895})
    "de&les"         : "det",           #        2236    de&les                  Counter({'prep': 2236})
    "regarder-IMP&2s" : None,           #        2215    regarder-IMP&2s         Counter({'v': 2215})
    "dans"           : "fun",           #        2154    dans                    Counter({'prep': 2153, 'none': 1})
    "faire-INF"      : None,            #        2141    faire-INF               Counter({'v:mdl': 1565, 'v:mdllex': 522, 're#v:mdl': 18, 're#v:mdllex': 17, 'dé#v:mdllex': 12, 'dé#v:mdl': 7})
    "ben"            : "fun",           #        2017    ben                     Counter({'co': 1503, 'adv': 512, 'uni': 2})
    "toi&sg"         : "prn",           #        2005    toi&sg                  Counter({'pro': 2005})
    "moi&sg"         : "prn",           #        1988    moi&sg                  Counter({'pro': 1988})
    "où"             : "fun",           #        1940    où                      Counter({'pro:int': 1788, 'pro:rel': 151, '0pro:int': 1})
    "pour"           : "fun",           #        1810    pour                    Counter({'prep': 1638, 'conj': 172})
    "faire-PRES&12s" : None,            #        1775    faire-PRES&12s          Counter({'v:mdl': 1695, 'v:mdllex': 57, 'dé#v:mdl': 11, 're#v:mdl': 10, 'dé#v:mdllex': 2})
    "bon"            : "fun",           #        1742    bon                     Counter({'co': 1742})
    "me"             : "fun",           #        1732    me                      Counter({'pro:obj': 1728, '0pro:obj': 4})
    "tenir-IMP&2s"   : None,            #        1698    tenir-IMP&2s            Counter({'v': 1695, 're#v': 3})
    "allez"          : "fun",           #        1650    allez                   Counter({'co': 1650})
    "avec"           : None,            #        1648    avec                    Counter({'prep': 1648})
    "bien"           : None,            #        1625    bien                    Counter({'adv': 1408, 'adj': 217})
    "la"             : "fun",           #        1611    la                      Counter({'co': 1314, 'pro:obj': 296, 'pro': 1})
    "ouais=yes"      : "fun",           #        1591    ouais=yes               Counter({'co': 1591})
    "encore"         : None,            #        1543    encore                  Counter({'adv': 1543})
    "falloir&PRES&3s" : "aux",          #        1543    falloir&PRES&3s         Counter({'v:mdl': 1543})
    "de&le"          : "det",           #        1538    de&le                   Counter({'prep': 1538})
    "se"             : "fun",           #        1535    se                      Counter({'pro:refl': 1534, '0pro:refl': 1})
    "hop"            : "fun",           #        1481    hop                     Counter({'co': 1481})
    "petit&m"        : None,            #        1463    petit&m                 Counter({'adj': 1463})
    "plus"           : None,            #        1427    plus                    Counter({'qn': 757, 'prep': 385, 'adv': 278, 'conj': 7})
    "mettre-INF"     : None,            #        1412    mettre-INF              Counter({'v': 1312, 're#v': 100})
    "aller&PRES&2s"  : "aux",           #        1300    aller&PRES&2s           Counter({'v:mdl': 1294, 'v:mdllex': 5, '0v:mdl': 1})
    "sur"            : "fun",           #        1294    sur                     Counter({'prep': 1292, 'vpfx': 2})
    "si"             : "fun",           #        1147    si                      Counter({'adv': 681, 'co': 262, 'conj': 204})
    "mh"             : "fun",           #        1144    mh                      Counter({'co': 1144})
    "aussi"          : None,            #        1132    aussi                   Counter({'adv': 1110, 'conj': 22})
    "être&PRES&2s"   : "fun",           #        1120    être&PRES&2s            Counter({'v:aux': 1019, 'v:exist': 100, '0v:aux': 1})
    "venir-IMP&2s"   : None,            #        1117    venir-IMP&2s            Counter({'v': 1072, 're#v': 42, 'pré#v': 3})
    "savoir&PRES&12s" : None,           #        1114    savoir&PRES&12s         Counter({'v:mdl': 1100, 'v:mdllex': 13, '0v:mdl': 1})
    "bah"            : "fun",           #        1080    bah                     Counter({'co': 1080})
    "voir&IMP&PRES&12s" : None,         #        1067    voir&IMP&PRES&12s       Counter({'v': 1067})
    "attendre-IMP&2s" : None,           #        1057    attendre-IMP&2s         Counter({'v': 1057})
    "mhm"            : "fun",           #        1021    mhm                     Counter({'co': 1021})
    "autre&sg"       : None,            #        1007    autre&sg                Counter({'pro': 1003, 'det:gen': 4})
    "ne"             : "fun",           #         963    ne                      Counter({'neg': 661, '0neg': 302})
    "avoir&PRES&1s"  : "aux",           #         961    avoir&PRES&1s           Counter({'v:aux': 756, 'v:poss': 205})
    "d'accord"       : "fun",           #         956    d'accord                Counter({'adv': 956})
    "voir&INF"       : None,            #         955    voir&INF                Counter({'v': 939, 're#v': 15, 'pré#v': 1})
    "ils"            : "prn",           #         934    ils                     Counter({'pro:sub': 930, '0pro:sub': 4})
    "regarder-PRES&SUB&13s" : None,     #         918    regarder-PRES&SUB&13s   Counter({'v': 918})
    "peu&m"          : None,            #         915    peu&m                   Counter({'n': 915})
    "très"           : None,            #         911    très                    Counter({'adv': 911})
    "maman&f"        : "nam",           #         898    maman&f                 Counter({'n': 898})
    "ton&m&sg"       : "det",           #         877    ton&m&sg                Counter({'det:poss': 877})
    "être&PRES&3p"   : "fun",           #         831    être&PRES&3p            Counter({'v:aux': 815, 'v:exist': 16})
    "Nanou"          : "nam",           #         814    Nanou                   Counter({'n:prop': 814})
    "aller&PRES&1s"  : "aux",           #         769    aller&PRES&1s           Counter({'v:mdl': 762, 'v:mdllex': 6, '0v:mdl': 1})
    "tout&m"         : None,            #         761    tout&m                  Counter({'n': 761})
    "à&le"           : "fun",           #         748    à&le                    Counter({'prep': 748})
    "mets&m"         : None,            #         747    mets&m                  Counter({'n': 747})
    "luire&PP&m"     : "prn",           #         731    luire&PP&m              Counter({'part': 731})     # NB: this is a mis-tagging of 'lui'!
    "euh"            : "fun",           #         712    euh                     Counter({'co': 712})
    "oui&m"          : "fun",           #         710    oui&m                   Counter({'n': 710})
}

def fre_add_tags_from_cues(x):

    for i in range(len(x)):

        if x[i].guess_tag is None:

            # Choose a candidate tag, candidate1, based on what precedes x[i]
            if i >= 1 and x[i-1].guess_tag == "det":
                candidate1 = "noun"
            elif i >= 1 and x[i-1].guess_tag == "aux":
                candidate1 = "verb"
            elif i >= 2 and x[i-2].guess_tag == "aux" and x[i-1].guess_tag == "neg":
                candidate1 = "verb"
            else:
                candidate1 = None

            # Choose a candidate tag, candidate2, based on what follows x[i]
            if i+1 < len(x) and x[i+1].guess_tag == "nsuf":
                candidate2 = "noun"
            elif i+1 < len(x) and x[i+1].guess_tag == "vsuf":
                candidate2 = "verb"
            else:
                candidate2 = None

            candidates = set([c for c in [candidate1,candidate2] if c is not None])
            if len(candidates) == 1:
                x[i].guess_tag = candidates.pop()

langinfodict[FRE].add_tags_from_cues = fre_add_tags_from_cues

def fre_try_split_suffixes(plain_w, pos, gloss):
    m = re.match(r'(.*)(-[0-9A-Za-z&]+)', gloss)
    if m is not None:
        if plain_w[-1:] in ["é"] or plain_w[-2:] in ["ée","és","er"] or plain_w[-3:] in ["ées"]:
            tw1 = TaggedWord(gloss, pos)
            tw2 = TaggedWord("-e")
            return [tw1, tw2]
        elif plain_w[-3:] == "ons":
            tw1 = TaggedWord(gloss, pos)
            tw2 = TaggedWord("-ons")
            return [tw1, tw2]
    return None

langinfodict[FRE].try_split_suffixes = fre_try_split_suffixes

######################################################################

######################################################################
### Japanese

JPN = "jpn"
langinfodict[JPN] = LangInfo()

langinfodict[JPN].initial_tagger = {
    "-te"                    : "vsuf",           #        9263    -te                     Counter({None: 9263})
    "ne=TAG"                 : "sfp",           #        8749    ne=TAG                  Counter({'ptl:fina': 8749})
    "no=QUD"                 : "fun",           #        8729    no=QUD                  Counter({'n:fml': 8729})
    "un=yes"                 : None,           #        8438    un=yes                  Counter({'co:i': 8438})
    "yo=ASSERT"              : "sfp",           #        7947    yo=ASSERT               Counter({'ptl:fina': 7947})
    "disloc"                 : None,           #        6902    disloc                  Counter({'tag': 6902})
    "da&PRES=be"             : "fun",           #        6467    da&PRES=be              Counter({'v:cop': 6467})
    "wa=TOP"                 : "cm",           #        6341    wa=TOP                  Counter({'ptl:top': 6341})
    "no=GEN"                 : "cm",           #        5292    no=GEN                  Counter({'ptl:attr': 5291, 'ptl:case': 1})
    "kore=this"              : "prn",           #        5074    kore=this               Counter({'n:deic:dem': 5074})
    "-nai"                   : "neg",           #        4839    -nai                    Counter({None: 4839})
    "hai=yes"                : None,           #        4742    hai=yes                 Counter({'co:i': 4742})
    "ga=NOM"                 : "cm1",           #        4669    ga=NOM                  Counter({'ptl:case': 4669})
    "aq=ah"                  : None,           #        4253    aq=ah                   Counter({'co:i': 4253})
    "nani=what"              : "fun",           #        3881    nani=what               Counter({'n:deic:wh': 3881})
    "voc"                    : None,           #        3838    voc                     Counter({'tag': 3838})
    "tte=QUOT"               : "fun",           #        3402    tte=QUOT                Counter({'ptl:quot': 3402})
    "ni=DAT"                 : "cm",           #        3200    ni=DAT                  Counter({'ptl:post': 3200})
    "ka=Q"                   : "sfp",           #        2748    ka=Q                    Counter({'ptl:fina': 2748})
    "n=yes"                  : None,           #        2653    n=yes                   Counter({'co:i': 2653})
    "Asato-kun_MFAM=Asato"   : "nam",           #        2306    Asato-kun_MFAM=Asato    Counter({'n:prop': 2306})
    "i-PRES=good"            : None,           #        2267    i-PRES=good             Counter({'adj': 2267})
    "mo=ADD"                 : "cm",           #        2174    mo=ADD                  Counter({'ptl:foc': 2174})
    "hora=look"              : None,           #        2148    hora=look               Counter({'co:i': 2148})
    "ni&ADV=be"              : "fun",           #        2098    ni&ADV=be               Counter({'v:cop': 2098})
    "ja=well"                : None,           #        2095    ja=well                 Counter({'conj': 2095})
    "kanaa=DOUBT"            : "sfp",           #        1948    kanaa=DOUBT             Counter({'ptl:fina': 1948})
    "kara=because"           : "fun",           #        1780    kara=because            Counter({'ptl:conj': 1780})
    "koko=here"              : "prn",           #        1679    koko=here               Counter({'n:deic:dem': 1679})
    "sore=this"              : "prn",           #        1575    sore=this               Counter({'n:deic:dem': 1575})
    "da&PRES:na=be"          : "fun",           #        1508    da&PRES:na=be           Counter({'v:cop': 1508})
    "Natchan=Natchan"        : "nam",           #        1325    Natchan=Natchan         Counter({'n:prop': 1325})
    "doko=where"             : "fun",           #        1247    doko=where              Counter({'n:deic:wh': 1247})
    "naa=TAG"                : "sfp",           #        1244    naa=TAG                 Counter({'ptl:fina': 1244})
    "su-PRES=do"             : None,           #        1219    su-PRES=do              Counter({'v:ir': 712, 'v:ir:sub': 507})
    "Nanami=Nanami"          : "nam",           #        1214    Nanami=Nanami           Counter({'n:prop': 1214})
    "de=LOC"                 : "cm",           #        1202    de=LOC                  Counter({'ptl:post': 1202})
    "kotchi=here"            : "prn",           #        1167    kotchi=here             Counter({'n:deic:dem': 1167})
    "moo=already"            : None,           #        1130    moo=already             Counter({'adv': 1130})
    "ar-PRES=be"             : None,           #        1130    ar-PRES=be              Counter({'v:ir': 1076, 'v:ir:sub': 54})
    "ar&NEG-PRES=be"         : None,           #        1109    ar&NEG-PRES=be          Counter({'v:ir': 870, 'v:ir:sub': 239})
    "o=ACC"                  : "cm2",           #        1068    o=ACC                   Counter({'ptl:case': 1068})
    "Kakka=Mum"              : "nam",           #        1025    Kakka=Mum               Counter({'n:prop': 1025})
    "no=RLV"                 : None,           #        1012    no=RLV                  Counter({'n:fml': 1012})
    "chotto=a_bit"           : None,           #        1009    chotto=a_bit            Counter({'adv': 1009})
    "de&wa-NEG-PRES=be"      : "fun",           #         941    de&wa-NEG-PRES=be       Counter({'v:cop': 941})
    "Okaasan=HON_Mother_HON" : "nam",           #         852    Okaasan=HON_Mother_HON  Counter({'n:prop': 852})
    "da&POL-PRES=be"         : "fun",           #         834    da&POL-PRES=be          Counter({'v:cop': 834})
    "soo=like_that"          : "fun",           #         818    soo=like_that           Counter({'adv:deic:dem': 818})
    "su-CONN=do"             : None,           #         816    su-CONN=do              Counter({'v:ir:sub': 428, 'v:ir': 388})
    "ara=oh_dear"            : None,           #         814    ara=oh_dear             Counter({'co:i': 814})
    "koo=like_this"          : "fun",           #         791    koo=like_this           Counter({'adv:deic:dem': 791})
    "de&CONN=be"             : "fun",           #         774    de&CONN=be              Counter({'v:cop': 774})
    "to=and"                 : "fun",           #         750    to=and                  Counter({'ptl:coo': 750})
    "ar-PAST=be"             : None,           #         733    ar-PAST=be              Counter({'v:ir': 730, 'v:ir:sub': 3})
    "hontoo=in_fact"         : None,           #         726    hontoo=in_fact          Counter({'n': 726})
    "ne=APPEAL"              : "fun",           #         696    ne=APPEAL               Counter({'co:i': 696})
    "to=COMT"                : "cm",           #         685    to=COMT                 Counter({'ptl:post': 685})
    "ik-PRES=go"             : None,           #         662    ik-PRES=go              Counter({'v:c': 567, 'v:c:sub': 95})
    "daroo&POL=INFR"         : "fun",           #         647    daroo&POL=INFR          Counter({'smod': 647})
    "Juri-chan_FAM=Juri"     : "nam",           #         619    Juri-chan_FAM=Juri      Counter({'n:prop': 619})
    "sa=FINA"                : "sfp",           #         611    sa=FINA                 Counter({'ptl:fina': 611})
    "su-HORT=do"             : None,           #         602    su-HORT=do              Counter({'v:ir': 340, 'v:ir:sub': 262})
    "sugo-PRES=terrific"     : None,           #         602    sugo-PRES=terrific      Counter({'adj': 602})
    "-de"                    : "vsuf",           #         600    -de                     Counter({None: 600})
    "dore=which"             : "fun",           #         597    dore=which              Counter({'n:deic:wh': 597})
    "Natchi"                 : "nam",           #         592    Natchi                  Counter({'n:prop': 592})
    "-ba"                    : "vsuf",           #         589    -ba                     Counter({None: 589})
    "da&POL-HORT=be"         : "fun",           #         588    da&POL-HORT=be          Counter({'v:cop': 588})
    "deki-PAST=can/make"     : None,           #         558    deki-PAST=can/make      Counter({'v:v': 558})
    "ippai=plenty"           : None,           #         552    ippai=plenty            Counter({'quant': 552})
    "tokoro=place"           : None,           #         546    tokoro=place            Counter({'n': 546})
    "ku-PAST=come"           : None,           #         528    ku-PAST=come            Counter({'v:ir:sub': 313, 'v:ir': 215})
    "arigatoo-thank_you"     : None,           #         524    arigatoo-thank_you      Counter({'co:g': 524})
    "iya=disgusting"         : None,           #         524    iya=disgusting          Counter({'n:an': 520, 'co:i': 4})
    "dare=who"               : "fun",           #         523    dare=who                Counter({'n:deic:wh': 523})
    "jan=TAG"                : "sfp",           #         520    jan=TAG                 Counter({'ptl:fina': 520})
    "kondo=this_time"        : None,           #         518    kondo=this_time         Counter({'n': 518})
    "mata=again"             : None,           #         510    mata=again              Counter({'adv': 510})
    "mot-CONN=hold"          : None,           #         510    mot-CONN=hold           Counter({'v:c': 510})
    "nande=why"              : "fun",           #         506    nande=why               Counter({'adv:deic:wh': 506})
    "dame=no_good"           : None,           #         491    dame=no_good            Counter({'n:an': 491})
    "fuun=AMAZED"            : None,           #         490    fuun=AMAZED             Counter({'co:i': 490})
    "areq=AMAZED"            : None,           #         477    areq=AMAZED             Counter({'co:i': 477})
    "su-IMP:te=do"           : None,           #         471    su-IMP:te=do            Counter({'v:ir:sub': 315, 'v:ir': 156})
    "yar-CONN=do"            : None,           #         470    yar-CONN=do             Counter({'v:c': 470})
    "su-PAST=do"             : None,           #         469    su-PAST=do              Counter({'v:ir': 241, 'v:ir:sub': 228})
    "ku-IMP:te=come"         : None,           #         466    ku-IMP:te=come          Counter({'v:ir:sub': 385, 'v:ir': 81})
    "kono=this"              : "fun",           #         466    kono=this               Counter({'adn:deic:dem': 466})
    "kedo=although"          : "fun",           #         461    kedo=although           Counter({'ptl:conj': 461})
    "doo=how"                : "fun",           #         453    doo=how                 Counter({'adv:deic:wh': 453})
    "yan=TAG"                : "sfp",           #         452    yan=TAG                 Counter({'ptl:fina': 452})
    "mon=ASSERT"             : "sfp",           #         449    mon=ASSERT              Counter({'ptl:fina': 449})
    "yoisho=oof"             : None,           #         444    yoisho=oof              Counter({'co:i': 444})
    "issho=together"         : None,           #         434    issho=together          Counter({'n': 434})
    "wa=FINA"                : "cm",           #         431    wa=FINA                 Counter({'ptl:fina': 431})          NB: homophonous with wa=TOP!
    "su-ASP-PRES=do"         : None,           #         430    su-ASP-PRES=do          Counter({'v:ir:sub': 275, 'v:ir': 155})
    "onaji=same"             : None,           #         421    onaji=same              Counter({'adn': 421})
    "ya&PRES=be"             : "fun",           #         419    ya&PRES=be              Counter({'v:cop': 419})
    "oq=oh"                  : None,           #         417    oq=oh                   Counter({'co:i': 417})
}

def jpn_add_tags_from_cues(x):

    for i in range(len(x)):

        if x[i].guess_tag is None:

            if i+1 < len(x) and x[i+1].guess_tag == "neg":
                result = "verb"
            elif i+1 < len(x) and x[i+1].guess_tag == "sfp":
                result = "verb"
            elif i+1 < len(x) and x[i+1].guess_tag == "vsuf":
                result = "verb"
            elif i+1 < len(x) and x[i+1].guess_tag is not None and re.match("cm[0-9]?", x[i+1].guess_tag):
                result = "noun"
            else:
                result = None
            x[i].guess_tag = result

            if i+1 < len(x) and x[i+1].guess_tag is not None:
                m = re.match("cm([0-9])", x[i+1].guess_tag)
                if m is not None:
                    x[i].cls = int(m.group(1))

langinfodict[JPN].add_tags_from_cues = jpn_add_tags_from_cues

def jpn_try_split_suffixes(plain_w, pos, gloss):

    m = re.match(r'(.*)(-[0-9A-Z]+)', gloss)
    if m is not None:
        for suffix in ["nai","nakatta","te","de","ba"]:
            if plain_w.endswith(suffix):
                tw1 = TaggedWord(gloss, pos)
                tw2 = TaggedWord("-" + suffix)
                return [tw1, tw2]

    return None

langinfodict[JPN].try_split_suffixes = jpn_try_split_suffixes

######################################################################

# ######################################################################
# ### Chinese
# 
# # https://journals.sagepub.com/doi/10.1177/0142723719845175
# 
# CHI = "chi"
# langinfodict[CHI] = LangInfo()
# 
# # 'zhe4=this': 5335 occurrences as 'det', 4411 as 'pro:dem'
# 
# langinfodict[CHI].initial_tags = defaultdict(lambda: None, {"pro:per": "prn", 
#                                                             #"pro:dem": "prn", # including this line creates a clash of tags for 'zhe4=this'
#                                                             "det": "det", 
#                                                             "cl": "cls", 
#                                                             "v:aux": "aux", 
#                                                             "asp": "asp", 
#                                                            })
# 
# def chi_add_tags_from_cues(x):
#     for i in range(len(x)):
#         if x[i].guess_tag is None:
#             if i > 0 and x[i-1].guess_tag == "cls":
#                 x[i].guess_tag = "noun"
#             elif i > 0 and x[i-1].guess_tag == "det":
#                 x[i].guess_tag = "noun"
#             elif i > 0 and x[i-1].guess_tag == "aux":
#                 x[i].guess_tag = "verb"
#             elif i < len(x)-1 and x[i+1].guess_tag == "asp":
#                 x[i].guess_tag = "verb"
# 
# langinfodict[CHI].add_tags_from_cues = chi_add_tags_from_cues
# 
# ######################################################################

######################################################################
### For reading CHILDES files

def utterances(f):

    def add_blank_tags(f):
        last_tag = None
        for line in f:
            line = line.rstrip()
            m = re.match(r'^(.*)\t(.*)$', line)
            if m is not None:
                (tag, contents) = m.groups()
                if tag == "":
                    tag = last_tag
                yield (tag, contents.split())
                last_tag = tag

    # Set up an iterator over (tag,contents) pairs, one per line, where every tag is non-empty
    with_full_tags = add_blank_tags(f)

    # Create an iterator over (tag,i) pairs, where tag is a string like "%mor:" and i is a subiterator
    grouped_by_tag = itertools.groupby(with_full_tags, key=lambda p: p[0])

    # Turn all the subiterators into lists
    grouped_by_tag_with_lists = map(lambda pair: (pair[0], list(pair[1])), grouped_by_tag)

    ignored_count = 0

    # Now group lines together by tag, return to "%mor:" groups
    for ((tag1,it1),(tag2,it2)) in itertools.pairwise(grouped_by_tag_with_lists):
        # it1, it2 = list(it1), list(it2)
        if tag2 == "%mor:" or tag2 == "%xmor:":
            plain_line = list(itertools.chain.from_iterable(contents for (_,contents) in it1))
            plain_line = list(filter(lambda t: t not in ["(.)"], plain_line))
            mor_line = list(itertools.chain.from_iterable(contents for (_,contents) in it2))
            if len(plain_line) == len(mor_line):
                yield zip(plain_line, mor_line)
            else:
                ignored_count += 1
                # print("\nWARNING: line lengths do not match")
                # print("         ", plain_line)
                # print("         ", mor_line)

    if ignored_count != 0:
        print("WARNING: Ignored %d '%%(x)mor:' lines" % ignored_count)

######################################################################

def initial_tagger_check(tagged_sentences, tagger=None):

    tag_counter = defaultdict(lambda: Counter())
    for s in tagged_sentences:
        for tw in s:
            tag_counter[tw.word][tw.true_tag] += 1
    words_ranked = sorted(tag_counter.keys(), key=(lambda w: tag_counter[w].total()), reverse=True)

    frequent_but_absent = []
    print("\nTop 100 most frequent words:")
    for w in words_ranked[:100]:
        print("#    %8d    %-24s%s" % (tag_counter[w].total(), w, tag_counter[w]))
        if tagger is not None and w not in tagger:
            frequent_but_absent.append(w)

    if frequent_but_absent != []:
        print("\nWARNING: Words from the top 100 most frequent not found in initial tagger:", frequent_but_absent)

######################################################################

class TaggedWord:
    def __init__(self, word, true_tag=None, guess_tag=None):
        self.word = word
        self.true_tag = true_tag
        self.guess_tag = guess_tag
        self.cls = None
    def __str__(self):
        return (self.word + "/" + (self.true_tag or "---") + "/" + ((self.guess_tag or "---") + (str(self.cls or ""))))
        # return (self.word + "/" + (self.guess_tag or "---"))

def apply_tagger(tagger, sentences):
    for sent in sentences:
        for tw in sent:
            tw.guess_tag = tagger.get(tw.word, None)

def main(argv):

    p = argparse.ArgumentParser()
    p.add_argument("--lang", type=str, required=True, choices=langinfodict.keys(), help="language")
    p.add_argument("--cm", action="store_true", help="use case-marking")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--ptb", action="store_true", help="input in PTB format")
    g.add_argument("--childes", action="store_true", help="input in CHILDES format")
    args = p.parse_args(sys.argv[1:])

    if args.lang in langinfodict:
        langinfo = langinfodict[args.lang]
    else:
        assert False, "Unknown language '%s'" % args.lang

    if args.ptb:

        ts = trees.get_trees(sys.stdin)
        cleanup = lambda pairs: [TaggedWord(w,t) for (t,w) in pairs if ("-NONE-" not in t) and (t not in [".",","]) and (w != "*null*")]
        tagged_sentences = list(map(cleanup,map(trees.tree_yield_with_tags, ts)))

    elif args.childes:

        tagged_sentences = []
        for u in utterances(sys.stdin):
            tagged_s = []
            for (plain_w, w) in u:
                if w == "part|taire-PP&m":
                    w = "pro:sub|tu"
                if w in [".","?","!","+...","+//.","+/.","beg|beg","end|end"]:
                    continue
                pieces = re.split("\$|\~", w)
                for piece in pieces:
                    m = re.match(r'(.*)\|(.*)', piece)
                    if m is not None:
                        (pos, gloss) = m.group(1,2)
                        if len(pieces) == 1:    # If this token consists of just a single (pos,gloss) pair
                            tws = langinfo.try_split_suffixes(plain_w, pos, gloss)
                            if tws is not None: # Found something!
                                tagged_s.extend(tws)
                            else: # Didn't find a split
                                tw = TaggedWord(gloss, pos)
                                tagged_s.append(tw)
                        else: # This is already one of many (pos,gloss) pairs for this token, so forget about suffixes
                            tw = TaggedWord(gloss, pos)
                            tagged_s.append(tw)
                    else:
                        tw = TaggedWord(piece)
                        tagged_s.append(tw)
            tagged_sentences.append(tagged_s)

    else:

        assert False

    add_our_tags(tagged_sentences, langinfo)

    print("\nSanity-checking of our detected suffixes:")
    # maps a suffix to a counter of true_tags
    d = defaultdict(lambda: Counter())
    for s in tagged_sentences:
        for (tw1,tw2) in zip(s, s[1:]):
            if tw2.word.startswith("-"):
                d[tw2.word][tw1.true_tag] += 1
    for (suffix,counter) in d.items():
        print("\t%-10s      total: %5d       true tags: %s" % (suffix, counter.total(), counter))

    get_usable_strings(tagged_sentences, args.cm)

def add_our_tags(tagged_sentences, langinfo):

    print("Starting with %d raw utterances" % len(tagged_sentences))

    print("\nFirst 30 sentences, raw:")
    for x in tagged_sentences[:30]:
        print("    " + " ".join(map(str,x)))

    initial_tagger = langinfo.initial_tagger

    # Prints out info about the most frequent words that we can use to construct/check/refine 
    # an initial_tagger, and checks these against the provided initial_tagger
    initial_tagger_check(tagged_sentences, initial_tagger)

    # Now do our first-round tagging based on initial_tagger
    apply_tagger(initial_tagger, tagged_sentences)

    print("\nFirst 30 sentences after initial tagging:")
    for x in tagged_sentences[:30]:
        print("    " + " ".join(map(str,x)))

    # Now add more tags based on functional cues
    for x in tagged_sentences:
        langinfo.add_tags_from_cues(x)

    print("\nFirst 30 sentences after tagging based on functional cues:")
    for x in tagged_sentences[:30]:
        print("    " + " ".join(map(str,x)))

    # What is the precision/recall here?

def get_usable_strings(tagged_sentences, use_case_marking=False):

    extracted_strings = [extract_np_v(x) for x in tagged_sentences]

    print("\nCounts of extracted strings:")
    for (tpl,freq) in Counter(extracted_strings).most_common(20):
        print("\t%5d\t%s" % (freq, " ".join(tpl)))

    # The extracted_strings we have so far might include ``case-marked'' NPs, i.e. np1, np2, etc.
    # If use_case_marking is True, we leave the numbers in and only count a string as usable if it 
    # contains at least one case-marked NP. 
    # If use_case_marking is False, we remove the numbers (i.e. "np1" -> "np"). 
    # Either way, a string is only usable if it contains exactly one V.
    if use_case_marking:
        tweak = lambda tpl: tpl
        is_usable = lambda tpl: tpl.count("v") == 1 and any(re.match("np[0-9]", x) for x in tpl)
    else:
        tweak = lambda tpl: tuple(re.sub("np[0-9]", "np", x) for x in tpl)
        is_usable = lambda tpl: tpl.count("v") == 1

    usable_strings = Counter(filter(is_usable, map(tweak, extracted_strings)))
    print("\nCounts and proportions of usable strings (total %d):" % usable_strings.total())
    for (tpl,freq) in usable_strings.most_common():
        print("\t%5d\t%.3f\t%s" % (freq, freq/usable_strings.total(), " ".join(tpl)))

def extract_np_v(tagged_sent):

    d = defaultdict(lambda: None, {"prn" : "np", "nam" : "np", "noun" : "np", "verb" : "v"})
    def replace(guess_tag, cls):
        lookup = d[guess_tag]
        if lookup is not None:
            return (lookup + str(cls or ""))
        else:
            return None
    extracted = tuple(filter(lambda t: t is not None, [replace(tw.guess_tag, tw.cls) for tw in tagged_sent]))

    debug_tpl = None
    if debug_tpl is not None and extracted == debug_tpl:
        print("%s: \t%s" % (" ".join(debug_tpl), " ".join(map(str,tagged_sent))))

    return extracted

if __name__ == "__main__":
    main(sys.argv)

