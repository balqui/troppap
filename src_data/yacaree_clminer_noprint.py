"""
Project: yacaree
Programmers: JLB

Its main method is the iterator that provides, one by one,
 in order of decreasing support, all the closures for a given
 dataset and support bound
 
"""

# ~ from math import floor

from itset import ItSet
from dataset import Dataset
from heapq import heappush, heappop
# ~ from yaflheap import FlHeap

class ClMiner:

    def __init__(self, dataset, hpar):
        "Some inherited fields are likely to be unnecessary here"
        self.dataset = dataset
        self.supp_rep_often = 500
        self.hpar = hpar
        self.card = 0
        self.negbordsize = 0
        self.maxnonsupp = 0
        self.maxitemnonsupp = 0
        self.minsupp = 0
        self.intsupp = 0
        # ~ print("Initializing singletons.")

        "pair up items with their support and sort them"
        sorteduniv = set() # autoremove duplicates
        for item in self.dataset.univ:
            cl= ItSet(dataset.inters(dataset.occurncs[item]), dataset.occurncs[item])
            sorteduniv.add(cl)
            # ~ if len(cl) > 1:
                # ~ print("closure of", item, "is", cl)
            
        self.clos_singl = sorted(sorteduniv)
        self.maxitemsupp = self.clos_singl[0].supp



    def test_size(self, pend_clos):
        return 0 # stub, bring it here from FlHeap

    def mine_closures(self):

        if self.maxitemsupp < self.dataset.nrtr:
            "empty set is closed, yield it"
            self.card += 1
            yield ItSet([], self.dataset.nrtr)

        # ~ pend_clos = FlHeap() 
        # ~ pend_clos = list()
        # ~ pend_clos.mpush(self.clos_singl)

        pend_clos = self.clos_singl.copy() # already sorted
        self.minsupp = self.dataset.nrtr
        while pend_clos:
            """
            extract largest-support closure and find subsequent ones,
            possibly after halving the heap through test_size(),
            in which case we got a higher value for the intsupp bound
            """
            new_supp = self.test_size(pend_clos) # wrong right now
            if new_supp > self.intsupp:
                "support bound grows, heap halved, report"
                # ~ print("Increasing min support from " +
                             # ~ str(self.intsupp) +
                             # ~ (" (%2.3f%%) up to " %
                              # ~ self.to_percent(self.intsupp)) +
                             # ~ str(new_supp) +
                             # ~ (" (%2.3f%%)" %
                              # ~ self.to_percent(new_supp)) + 
                            # ~ ".")
                self.intsupp = new_supp
            cl = heappop(pend_clos)
            spp = cl.supp
            if spp < self.intsupp:
                "maybe intsupp has grown in the meantime (neg border)"
                break
            if spp < self.minsupp:
                self.minsupp = spp
            self.card += 1
            yield (cl)
            # ~ if self.card % self.supp_rep_often == 0:
                # ~ print(str(self.card) +
                            # ~ " closures traversed, " +
                               # ~ str(pend_clos.count) + 
                            # ~ " further closures found so far; current support " +
                            # ~ str(spp) + ".")
            for ext in self.clos_singl:
                "try extending with freq closures of singletons"
                if not set(ext) <= cl:
                    supportset = cl.supportset & ext.supportset
                    spp = len(supportset)
                    if spp <= self.intsupp:
                        self.negbordsize += 1
                        if spp > self.maxnonsupp:
                            self.maxnonsupp = spp
                    else:
                        "find closure and test duplicateness"
                        next_clos = frozenset(self.dataset.inters(supportset))
                        cl_node = ItSet(next_clos, supportset)
                        # ~ print("Generated:", cl_node, "from", cl, "and", ext)
                        if next_clos not in pend_clos:
                            # ~ cl_node = ItSet(next_clos, supportset)
                            heappush(pend_clos, cl_node)
                        # ~ else:
                            # ~ print("Skipped duplicate:", cl_node)

        
if __name__ == "__main__":
    
    from hyperparam import HyperParam

    # ~ fnm = "lenses_recoded"
    fnm = "e13"
    supp = 0
    # ~ supp = 1.0/14

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

    miner = ClMiner(d, hpar)

    cnt = 0
    lst = list()
    for e in miner.clos_singl:
        cnt += 1
        lst.append(e)

    print(len(lst), "singleton closures:")

    for e in lst:
        print("  ", e)

    # ~ print(miner.card, "card")
    # ~ print(miner.negbordsize, "negbordsize")
    # ~ print(miner.maxnonsupp, "maxnonsupp")
    # ~ print(miner.maxitemnonsupp, "maxitemnonsupp")
    # ~ print(miner.minsupp, "minsupp")
    # ~ print(miner.maxitemsupp, "maxitemsupp")

    for e in miner.mine_closures():
        cnt += 1
        lst.append(e)
    print(len(lst), "closures total")


    for e in lst:
        print("  ", e)
