"""
Current date: early Fructidor 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Closure miner based on the Troppus algorithm: simpler version
with Store but no memory checks nor halving the size of the
list of pending closures. Nonclosed sets keep being added to 
the dict as in the immediately previous version.
"""


from itset import ItSet
from dataset import Dataset
from store import Store

class ClMiner(dict):
    """
    Troppus-based miner. It is a dict from (frozen)sets of items 
    (closed or not) to their closing ItSet's. Has a mine_closures 
    generator of course to be called from Lattice.
    """

    def __init__(self, dataset, hpar, supp=-1):
        super().__init__()
        self.dataset = dataset
        self.hpar = hpar
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = IFace.hpar.genabsupp
        self.card = 0
        self.totlen = 0
        self.pend_clos = Store(use_heap = False)


    def supp_adding(self, itst, nitt):
        """
        Find support of the result of adding nitt (new item) to itst.
        If necessary, compute supporting set for that. Store on self 
        if not there yet. (THEN dict order is NOT yield order anymore.)
        Leave sets and closures in the dict even if their support is 
        zero.
        They are not that useful but wanted to avoid testing them again,
        grab a lot of memory though since closure is all the items.
        """
        exact = False # matches maybe a transaction
        itst = frozenset(itst)
        itstadd = frozenset(itst.union(nitt))
        if itstadd in self:
            "supp of union is supp of its closure"
            return self[itstadd].supp
        if itst in self:
            "itstadd not in self but itst is, intersect support sets"
            supp = set(self[itst].supportset) & nitt.supportset
            clos = self.dataset.inters(supp)
        else:
            "need to compute support set on data"
            supp, exact = self.dataset.slow_supp(itstadd)
            if exact:
                "matched a transaction hence it is closed"
                clos = itstadd
            else:
                "intersect support sets"
                clos = self.dataset.inters(supp)
        clos = ItSet(clos, supp)
        self[itstadd] = clos
        self.totlen += len(supp)
        return clos.supp


    def mine_closures(self):
        "As per the Troppus algorithm"

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
            if frozenset(pclos) not in self:
                self[frozenset(pclos)] = clos
            self.card += 1
            yield clos

            mxsupp = 0
            for itt in sorteditems:
                (i,) = itt # extract the item in the singleton ItSet
                if i in pclos:
                    "remove this i as required for all future i's"
                    pclos.remove(i)
                else:
                    nst = pclos.copy() # copy to modify
                    sp = self.supp_adding(nst, itt)
                    if sp > mxsupp:
                        ncl = self[frozenset(nst.union(itt))]
                        for j in ncl:
                            jtt = ItSet({j}, self.dataset.occurncs[j])
                            if (j not in clos and itt < jtt):
                                "I should recheck out these conditions once more one day"
                                break
                        else:
                            if sp > clos.supp:
                                break
                            elif sp > self.intsupp:
                                self.pend_clos.spush(ncl)
                                mxsupp = sp

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
    fnm = "NOW" 
    # ~ fnm = "papersTr"

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
    miner = ClMiner(d, hpar, 0.0043)
    lcl = list()
    t0 = time.time()
    for cl in miner.mine_closures():
        lcl.append(cl)
        # ~ if len(lcl) == 2000:
            # ~ break
        # ~ print(cl)
    t1 = time.time()
    print("Mining time:", t1 - t0)
    print(f"Number of closures: {len(lcl)} of " + 
          f"support {cl.supp} of more; total lengths {miner.totlen}, {miner.card}.") # or miner.card


