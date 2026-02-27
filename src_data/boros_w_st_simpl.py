"""
Current date: early Germinal 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Closure miner based on the algorithm implicit in the Boros et al. paper.
"""

from itset import ItSet
from dataset import Dataset

from hyperparam import HyperParam

from store import Store

import time

from collections import defaultdict # Counter # consider removing this


class ClMiner:
    """
    Closure miner as per Boros et al. Has a mine_closures 
    generator as well.
    """

    def __init__(self, dataset, hpar, supp = -1):
        # ~ super().__init__()
        self.dataset = dataset
        self.hpar = hpar
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = hpar.genabsupp
        self.card = 0
        self.totlen = 0
        self.pend_clos = Store(use_heap = False)

        # ~ self.ctr = Counter()


    def max_exts(self, st, sorteditems):
        "find items to add s.t. the resulting support set is maximal"
        trace = False
        # ~ trace = True
        # ~ trace = len(st) == 0
        if trace:
            print(" --- going to extend", st)
        ext_supp = dict() # map item to support of extension with it
        for itt in sorteditems:
            (i,) = itt # extract the item in the singleton ItSet
            if i not in st:
                ext_supp[i] = set()
        mut_incl = dict() # pairwise inclusions between support sets
        for j in ext_supp:
            for k in ext_supp:
                mut_incl[j, k] = True # until proven false
        for tr in st.supportset:
            for j in ext_supp:
                if j in self.dataset.transcns[tr]:
                    ext_supp[j].add(tr)
                    for k in ext_supp:
                        if k not in self.dataset.transcns[tr]:
                            mut_incl[j, k] = False
        valid = set(ext_supp)
        valid_clos = defaultdict(set)
        # ~ if trace:
            # ~ print(" --- mutual inclusions:")
            # ~ for p in mut_incl:
                # ~ print(" ----- ", p, mut_incl[p])
        for j in ext_supp:
            valid_clos[j].add(j)
            for k in ext_supp:
                if mut_incl[j, k] and not mut_incl[k, j]:
                    "j does not lead to a maximal support set"
                    if trace:
                        print(" --- discard", j, "covered by", k)
                    valid.discard(j) # can be repeatedly discarded
                if mut_incl[j, k] and mut_incl[k, j] and j < k:
                    valid_clos[j].add(k)
                    if trace:
                        print(" --- discard", k, "mutual cov with", j)
                    valid.discard(k) # avoid repetition, keep only j
        for j in ext_supp:
            if j in valid_clos and j not in valid:
                del valid_clos[j]
        if trace:
            print(" --- valid extensions:", dict(valid_clos))
        return valid_clos.values(), ext_supp
        


    def mine_closures(self):

        closempty = set()
        sorteditems = list()

        for it in self.dataset.univ:
            if len(self.dataset.occurncs[it]) == self.dataset.nrtr:
                closempty.add(it)
            else:
                sorteditems.append(
                    ItSet([it], self.dataset.occurncs[it])
                )

        sorteditems.sort() # decr supp, item tie-break, see ItSet.__lt__

        closempty = ItSet(closempty, range(self.dataset.nrtr))
        self.pend_clos.spush(closempty)

        report_it = False
        self.minsupp = self.dataset.nrtr
        while self.pend_clos:
            """
            Yield next closure and handle extensions.
            """
            clos = self.pend_clos.spop()
            pclos = set(clos)  # mutable copy of contents
            # ~ if frozenset(pclos) not in self:
                # ~ self[frozenset(pclos)] = clos
            self.card += 1
            yield clos

            if self.card % self.hpar.report_often == 0 or report_it:
                "Just report."
                report_it = False
                print(
                  f"{self.card} closures traversed, " +
                  f"{len(self.pend_clos)} further closures " +
                  f"found so far; current support {clos.supp}.")

            mx_xts, xts_supp = self.max_exts(clos, sorteditems)
            for xt in mx_xts:
                one, *_ = xt
                xtitst = ItSet(clos.union(xt), xts_supp[one])
                # ~ print(" +++++++ ", xtitst, "from", clos)
                if xtitst not in self.pend_clos and xtitst.supp > self.intsupp:
                    self.pend_clos.spush(xtitst)


if __name__ == "__main__":
    with open("times_boros_True_simpl.txt","w") as f:
        # ~ names = ["supermarketTr","NOW","papersTr","votesTr","mushroomTr","connect.td","chess.td","cmc-full","adultrain"]
        # ~ l1 = [415,7,22,83,234,63812,2351,5,137]
        # ~ l2 = [4627,1597,721,435,8124,67557,3196,1473,32561]
        names = ["NOW", "papersTr"]
        l1 = [7, 22]
        # ~ l1 = [60, 220]
        l2 = [1597, 721]
        # ~ names = ["toy", "e24t.td"]
        # ~ l1 = [1, 1]
        # ~ l2 = [12, 24]
        # ~ for i in range(1): # 2): # 9):
        for i, fnm in enumerate(names):
            # ~ fnm = names[i]
            print(i)
            if fnm.endswith('.td') or fnm.endswith('.txt'):
                filenamefull = fnm
                filename, _ = fnm.rsplit('.',1)
            else:
                filename = fnm
                filenamefull = fnm + ".txt" # of ".td" one day...

            try:
                # ~ datafile = open("datasets/"+filenamefull)
                datafile = open(filenamefull)
                assert datafile._checkReadable()
                print(filenamefull,"File is now open.\n")
            except (IOError, OSError, AssertionError):
                print(filenamefull,"Nonexistent or unreadable file.")
                exit(1)

            hpar = HyperParam()
            f.write("Reading in dataset from file %s \n"%filenamefull)
            d = Dataset(datafile, hpar)

            thrs = l1[i]/l2[i]
            # ~ thrs = 0.2
            miner = ClMiner(d, hpar, thrs)
            f.write(f"Support quotient {thrs}\n")
            print(f"Support quotient {thrs}\n")
            lcl = list()
            t0 = time.time()
            for cl in miner.mine_closures():
                lcl.append(cl)
                # ~ if len(lcl) == 10:
                    # ~ print("... last, 10th... ", cl)
                    # ~ break
            t1 = time.time()
            # ~ f.write('\n'.join(str(cl) for cl in lcl) + '\n') # write the closures out
            f.write("Time: %.3f\n"%(t1 - t0))
            f.write(f"Number of closures: {len(lcl)} of " + f"support {cl.supp} of more.\n")


# ~ if __name__ == "__main__":

    # ~ from time import time
    # ~ from hyperparam import HyperParam

    # ~ fnm = "lenses_recoded"
    # ~ fnm = "markbask"
    # ~ fnm = "toy"
    # ~ fnm = "ect24.td"
    # ~ fnm = "e24.td"
    # ~ fnm = "e24t.td"
    # ~ fnm = "e13"
    # ~ fnm = "e5b"
    # ~ fnm = "e13a"
    # ~ fnm = "e13b"

    # ~ fnm = "supermarketTr"
    # ~ fnm = "adultrain"
    # ~ fnm = "cmc-full"
    # ~ fnm = "chess.td"
    # ~ fnm = "connect.td"
    # ~ fnm = "mushroomTr" 
    # ~ fnm = "votesTr" 
    # ~ fnm = "NOW" 
    # ~ fnm = "papersTr"

    # ~ fnm = "ejemploPV"

    # ~ uh = 'h' if miner.pend_clos.use_heap else 'd'
    # ~ if lcl:
        # ~ outfnm = "boros_" + uh + "_" + filename + "_" + str(mnsupp) + ".txt"
        # ~ with open(outfnm, 'w') as g:
            # ~ for e in lcl:
                # ~ print(e, file = g)
        # ~ print("Wrote closures file", outfnm)
    # ~ else:
        # ~ print("No closures found, no closures file created.")

# ~ Counter of various classes of closures, uncomment self.ctr in __init__
    # ~ rrr = 0
    # ~ for c in miner.ctr:
        # ~ print(c, miner.ctr[c])
        # ~ rrr += miner.ctr[c]
    # ~ print("%:", miner.ctr["intersected transactions"]*100/rrr)

    # ~ for cl in lcl:
        # ~ print(' '.join(e for e in sorted(cl)))
        # ~ print(cl)

