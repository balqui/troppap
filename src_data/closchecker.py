"""
Checks a file of closures for a dataset and minimum support against
a precomputed reference file. Assumes nothing about the order.
"""

from collections import defaultdict # Counter

from dataset import Dataset
from hyperparam import HyperParam

class OurDDict(defaultdict):
    "Just to tune how it is written out"

    def __init__(self):
        super().__init__(set)
        self.mxsuppref = 0
        self.mnsuppref = float("inf")

    def __str__(self):
        r = str()
        for s in reversed(range(self.mnsuppref, self.mxsuppref + 1)):
            r += '\n' + str(s) + ' '
            r += '\n  '.join(('{ ' + 
                (', '.join(it for it in sorted(itst))) + ' }') 
                for itst in refdict[s])
        return r

if __name__ == "__main__":

    # ~ fnm = "markbask"
    # ~ fnm = "supermarket"
    # ~ fnm = "adultrain"
    # ~ fnm = "cmc-full"
    # ~ fnm = "chess.td"
    # ~ fnm = "connect.td"
    # ~ fnm = "mushroomTr" 
    # ~ fnm = "votesTr" 
    # ~ fnm = "NOW" 
    # ~ fnm = "papersTr"

    # ~ fnm = "e13"

    fnm = input("Data file? ")
    support = input("Support bound? (integer number of transactions) ")
    ref_file_name = f"ref_{fnm}_{support}.txt"

    # ~ if fnm.endswith('.td') or fnm.endswith('.txt'):
        # ~ filenamefull = fnm
        # ~ filename, _ = fnm.rsplit('.',1)
    # ~ else:
        # ~ filename = fnm
        # ~ filenamefull = fnm + ".txt" # of ".td" one day...

    try:
        rf = open(ref_file_name)
        assert rf._checkReadable()
        print("File is now open.")
    except (IOError, OSError, AssertionError):
        print(f"Nonexistent or unreadable reference file {ref_file_name}.")
        exit(1)

    checkfnm = input("Closures file to check? ")

    # ~ checkfnm = "ref_e13_0_incomplete.txt"
    # ~ checkfnm = "ref_e13_0_.txt"

    try:
        cf = open(checkfnm)
        assert cf._checkReadable()
        print("File is now open.")
    except (IOError, OSError, AssertionError):
        print(f"Nonexistent or unreadable closures file {checkfnm}.")
        exit(1)

    refdict = OurDDict()
    # ~ with open(ref_file_name) as rf:
    for line in rf:
        if line.strip():
            itst, spp = line.split('/')
            spp = int(spp)
            refdict.mxsuppref = max(refdict.mxsuppref, spp)
            refdict.mnsuppref = min(refdict.mnsuppref, spp)
            refdict[spp].add((frozenset(itst.split(',')), spp))
    rf.close()

    # ~ print(refdict)

    clodict = OurDDict()
    for line in cf:
        if line.strip():
            itst, spp = line.split('/')
            spp = int(spp)
            clodict.mxsuppref = max(clodict.mxsuppref, spp)
            clodict.mnsuppref = min(clodict.mnsuppref, spp)
            clodict[spp].add((frozenset(itst.split(',')), spp))
    cf.close()

    # ~ print(clodict)

    if clodict.mnsuppref == refdict.mnsuppref and \
       clodict.mxsuppref == refdict.mxsuppref:
        print("Support limits match.")
        mnsuppref = clodict.mnsuppref
        mxsuppref = refdict.mxsuppref
        limmatch = '.'
    else:
        mnsuppref = max(clodict.mnsuppref, refdict.mnsuppref)
        mxsuppref = min(clodict.mxsuppref, refdict.mxsuppref)
        print("Support limits don't match.")
        print(f"Testing on common supports, {mnsuppref} to {mxsuppref}.")
        limmatch = ' in the common supports.'

    diff = set()
    for s in reversed(range(mnsuppref, mxsuppref + 1)):
        diff.update(refdict[s].symmetric_difference(clodict[s]))
    if not diff:
        print("Closures coincide" + limmatch)
    else:
        print("Closures don't coincide.")
        print(f"There are {len(diff)} differences.")
        if input("Show all differences? (Y/n) ") != 'n':
            cnt = 0
            for e in sorted(diff, key = lambda it: it[1]):
                cnt += 1
                print(f"{cnt}: {{ {', '.join(sorted(e[0]))} }} /{e[1]}")
