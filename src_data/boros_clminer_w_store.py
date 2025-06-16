"""
Current date: early Germinal 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Closure miner based on the algorithm implicit in the Boros et al. paper.
"""

from itset import ItSet
from dataset import Dataset

from store import Store

# ~ from heapq import heapify, heappush, heappop

# ~ from psutil import virtual_memory as vmem

from collections import defaultdict # Counter # consider removing this

# ~ from itertools import combinations

# ~ class Test_Memory:

    # ~ def __init__(self, nrits):
        # ~ self.cuts = 0
        # ~ self.nrits = nrits
        # ~ self.nrits_thr = 1000
        # ~ self.first_thr = 50
        # ~ self.secnd_thr = 65
        # ~ self.third_thr = 80

    # ~ def too_much_mem(self):
        # ~ if self.nrits < self.nrits_thr or self.cuts == 0:
            # ~ return vmem().percent > self.first_thr
        # ~ elif self.cuts == 1:
            # ~ return vmem().percent > self.secnd_thr
        # ~ else:
            # ~ "CAVEAT: third threshold or second?"
            # ~ return vmem().percent > self.third_thr

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
        # ~ self.mem_tester = Test_Memory(hpar.nrits)

        # ~ self.ctr = Counter()


    # ~ def close(self, st):
        # ~ "find (and store if new) closure of set st"
        # ~ fst = frozenset(st)
        # ~ if fst in self:
            # ~ "self expected to contain already the whole closure space"
            # ~ return self[fst]
        # ~ supp, exact = self.dataset.slow_supp(fst)
        # ~ if exact:
            # ~ "matched a transaction hence it is closed"
            # ~ clos = fst
        # ~ else:
            # ~ "intersect support sets"
            # ~ clos = self.dataset.inters(supp)
        # ~ clos = ItSet(clos, supp)
        # ~ # if clos.supp > 0:
        # ~ self[fst] = clos
        # ~ self.totlen += len(supp)
        # ~ return clos


    def max_exts(self, st, sorteditems):
        "find items to add s.t. the resulting support set is maximal"
        # ~ print(" --- going to extend", st)
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
        # ~ print(" --- mutual inclusions:")
        # ~ for p in mut_incl:
            # ~ print(" ----- ", p, mut_incl[p])
        for j in ext_supp:
            valid_clos[j].add(j)
            for k in ext_supp:
                if mut_incl[j, k] and not mut_incl[k, j]:
                    "j does not lead to a maximal support set"
                    # ~ print(" --- discard", j, "covered by", k)
                    valid.discard(j) # can be repeatedly discarded
                if mut_incl[j, k] and mut_incl[k, j] and j < k:
                    valid_clos[j].add(k)
                    # ~ print(" --- discard", k, "mutual cov with", j)
                    valid.discard(k) # avoid repetition, keep only j
        # ~ print(" --- closures:", valid_clos)
        # ~ print(" --- valid extensions:", valid)
        for j in ext_supp:
            if j in valid_clos and j not in valid:
                del valid_clos[j]
        # ~ print(" --- valid closures:", valid_clos.values())
        return valid_clos.values(), ext_supp
        



    def test_size(self):
        # ~ """
        # ~ Similar to test_size in yaflheap, with the so-called ugly hack, 
        # ~ but now for a standard heap kept in a standard list; other
        # ~ than that, very close to version 1.*.
        # ~ DOES NOTHING RIGHT NOW because depends on whether store is a heap
        # ~ """
        intsupp = 0 # return 0 if supp unchanged o/w return new supp
        # ~ # if ((count := len(self.pend_clos)) > IFace.hpar.pend_len_limit
          # ~ # or self.totlen > IFace.hpar.tot_len_limit):
            # ~ # """
            # ~ # Too many closures pending expansion: raise
            # ~ # the support bound so that about half of the
            # ~ # heap becomes discarded. Careful that support-tied
            # ~ # ItSet's are either all kept or all discarded.
            # ~ # Trying to control as well tot_len_limit.
            # ~ # THIS TEST FULLY REMOVED FOR NOW.
            # ~ # """
        # ~ incr_supp = False
        # ~ if self.mem_tester.too_much_mem():
            # ~ print("Too high memory usage: " + 
                # ~ "increasing support threshold.")
            # ~ incr_supp = True
        # ~ if len(self.pend_clos) > self.hpar.pend_len_limit:
            # ~ print("Too many pending closures: " + 
                # ~ "increasing support threshold.")
            # ~ incr_supp = True
        # ~ if incr_supp:
            # ~ """
            # ~ Lowish amount of system's memory remains available. 
            # ~ Often, however, most memory is not employed by the heap
            # ~ (e.g. the closures dict instead): maybe, cutting away 
            # ~ half the heap does not free much. But the new support 
            # ~ may allow the computation to complete anyway.
            # ~ """
            # ~ self.mem_tester.cuts += 1
            # ~ lim = len(self.pend_clos) // 2
            # ~ current_supp = self.pend_clos[0].supp
            # ~ current_supp_clos = []
            # ~ new_pend_clos = []
            # ~ new_count = 0
            # ~ popped_count = 0
            # ~ while self.pend_clos:
                # ~ itst = heappop(self.pend_clos)
                # ~ popped_count += 1
                # ~ if popped_count > lim: break
                # ~ if itst.supp == current_supp:
                    # ~ current_supp_clos.append(itst)
                # ~ else:
                    # ~ intsupp = current_supp
                    # ~ new_pend_clos.extend(current_supp_clos)
                    # ~ current_supp = itst.supp
                    # ~ current_supp_clos = [itst]
            # ~ self.pend_clos = new_pend_clos
        return intsupp


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
        # ~ self.pend_clos = [ closempty ]
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

            if self.card % self.hpar.check_size_often == 0:
                "Consider raising support - NEVER HAPPENS IN THIS VERSION."
                new_supp = self.test_size()
                if new_supp > self.intsupp:
                    "support bound grew, heap halved, report"
                    print(
                      f"Increased minimum support from {self.intsupp} "
                      + f"({self.intsupp*100/self.dataset.nrtr:5.3f}%) "
                      + f"up to {new_supp} " 
                      + f"({new_supp*100/self.dataset.nrtr:5.3f}%).")
                    self.intsupp = new_supp
                    report_it = True
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
                if xtitst not in self.pend_clos and xtitst.supp > self.intsupp:
                    self.pend_clos.spush(xtitst)


            # ~ first_level = False  # unless we find otherwise later on
            # ~ mxsupp = 0
            # ~ for itt in sorteditems:
                # ~ (i,) = itt # extract the item in the singleton ItSet
                # ~ # if first_level:
                    # ~ # """
                    # ~ # set at previous loop: no further i can clear mxsupp
                    # ~ # CAVEAT: I don't fully understand these conditions
                    # ~ # """
                    # ~ # break
                # ~ if i in pclos:
                    # ~ "remove this i as required for all future i's"
                    # ~ pclos.remove(i)
                # ~ else:
                    # ~ nst = pclos.copy() # copy to modify
                    # ~ sp = self.supp_adding(nst, itt)
                    # ~ if not pclos:
                        # ~ """
                        # ~ nst a singleton: back down to singletons level
                        # ~ CAVEAT: I don't fully understand these conditions
                        # ~ """
                        # ~ first_level = True
                    # ~ if sp > mxsupp:
                        # ~ ncl = self[frozenset(nst.union(itt))]
                        # ~ for j in ncl:
                            # ~ jtt = ItSet({j}, self.dataset.occurncs[j])
                            # ~ # if (j not in clos and
                               # ~ # (itt.supp > jtt.supp or
                               # ~ # (itt.supp == jtt.supp and i > j))):
                            # ~ if (j not in clos and itt < jtt):
                                # ~ "CAVEAT: I don't fully understand these conditions"
                                # ~ # print(" --- discard as:", jtt, ">", itt)
                                # ~ break
                        # ~ else:
                            # ~ if sp > clos.supp:
                                # ~ break
                            # ~ elif sp > self.intsupp:
                                # ~ heappush(self.pend_clos, ncl)
                                # ~ mxsupp = sp

if __name__ == "__main__":

    # ~ from time import time
    from hyperparam import HyperParam

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

    fnm = "ejemploPV"

    if fnm.endswith('.td') or fnm.endswith('.txt'):
        filenamefull = fnm
        filename, _ = fnm.rsplit('.',1)
    else:
        filename = fnm
        filenamefull = fnm + ".txt" # of ".td" one day...

    try:
        datafile = open(filenamefull)
        assert datafile._checkReadable()
        print("File is now open.")
    except (IOError, OSError, AssertionError):
        print("Nonexistent or unreadable file.")
        exit(1)

    hpar = HyperParam()
    print("Reading in dataset from file", filenamefull)
    d = Dataset(datafile, hpar)

    import time
    miner = ClMiner(d, hpar, 0.02)
    lcl = list()
    t0 = time.time()
    for cl in miner.mine_closures():
        lcl.append(cl)
        # ~ if len(lcl) == 2000:
            # ~ break
        # ~ print(cl)
    t1 = time.time()
    print("Time:", t1 - t0)
    mnsupp = cl.supp
    print(f"Number of closures: {len(lcl)} of " + 
          f"support {mnsupp} of more.") # or miner.card
    # ~ print("LAST", str(cl))
    print("ALL", lcl)
    exit(1)

    uh = 'h' if miner.pend_clos.use_heap else 'd'
    if lcl:
        outfnm = "boros_" + uh + "_" + filename + "_" + str(mnsupp) + ".txt"
        with open(outfnm, 'w') as g:
            for e in lcl:
                print(e, file = g)
        print("Wrote closures file", outfnm)
    else:
        print("No closures found, no closures file created.")

# ~ Counter of various classes of closures, uncomment self.ctr in __init__
    # ~ rrr = 0
    # ~ for c in miner.ctr:
        # ~ print(c, miner.ctr[c])
        # ~ rrr += miner.ctr[c]
    # ~ print("%:", miner.ctr["intersected transactions"]*100/rrr)

    # ~ for cl in lcl:
        # ~ print(' '.join(e for e in sorted(cl)))
        # ~ print(cl)


