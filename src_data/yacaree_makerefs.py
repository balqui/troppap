"""
Project: yacaree
Programmers: JLB

Its main method is the iterator that provides, one by one,
 in order of decreasing support, all the closures for a given
 dataset and support bound.
This version is to be used to create reference files containing 
 closed sets for comparison with other algorithms.
"""

from dataset import Dataset
from heapq import heappush, heappop

from itset import ItSet



class ClMiner:

    def __init__(self, dataset, hpar, supp = -1):
        "Some inherited fields are likely to be unnecessary here"
        self.dataset = dataset
        self.card = 0
        if supp > -1:
            self.intsupp = int(supp * dataset.nrtr)
        else:
            self.intsupp = hpar.genabsupp
        self.supp_rep_often = 2000
        # ~ self.hpar = hpar
        # ~ self.negbordsize = 0
        # ~ self.maxnonsupp = 0
        # ~ self.maxitemnonsupp = 0
        # ~ self.minsupp = 0
        # ~ self.intsupp = 0

        sorteduniv = set() # autoremove duplicates
        for item in self.dataset.univ:
            cl= ItSet(dataset.inters(dataset.occurncs[item]), dataset.occurncs[item])
            sorteduniv.add(cl)
            # ~ if len(cl) > 1:
                # ~ print("closure of", item, "is", cl)
            
        self.clos_singl = sorted(sorteduniv)
        self.maxitemsupp = self.clos_singl[0].supp

    # ~ def test_size(self, pend_clos):
        # ~ return 0 

    def mine_closures(self):

        if self.maxitemsupp < self.dataset.nrtr:
            "empty set is closed, yield it"
            self.card += 1
            yield ItSet([], self.dataset.nrtr)

        pend_clos = self.clos_singl.copy() # already sorted
        self.minsupp = self.dataset.nrtr
        while pend_clos:
            """
            extract largest-support closure and find subsequent ones,
            possibly after halving the heap through test_size(),
            in which case we got a higher value for the intsupp bound
            """
            # ~ new_supp = self.test_size(pend_clos) # wrong right now
            # ~ if new_supp > self.intsupp:
                # ~ "support bound grows, heap halved, report"
                # ~ print("Increasing min support from " +
                             # ~ str(self.intsupp) +
                             # ~ (" (%2.3f%%) up to " %
                              # ~ self.to_percent(self.intsupp)) +
                             # ~ str(new_supp) +
                             # ~ (" (%2.3f%%)" %
                              # ~ self.to_percent(new_supp)) + 
                            # ~ ".")
                # ~ self.intsupp = new_supp
            cl = heappop(pend_clos)
            spp = cl.supp
            if spp < self.intsupp:
                "maybe intsupp has grown in the meantime, can stop"
                break
            if spp < self.minsupp:
                self.minsupp = spp
            self.card += 1
            yield (cl)
            if self.card % self.supp_rep_often == 0:
                print(str(self.card) +
                            " closures traversed, " +
                               str(pend_clos.count) + 
                            " further closures found so far; current support " +
                            str(spp) + ".")
            for ext in self.clos_singl:
                "try extending with freq closures of singletons"
                if not set(ext) <= cl:
                    supportset = cl.supportset & ext.supportset
                    spp = len(supportset)
                    if spp == 0:
                        "what about outcomes of support zero?"
                        # ~ print("support zero for", cl, ext)
                        pass
                    elif spp <= self.intsupp:
                        pass
                        # ~ self.negbordsize += 1
                        # ~ if spp > self.maxnonsupp:
                            # ~ self.maxnonsupp = spp
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
    # ~ fnm = "e13"
    # ~ supp = 0
    # ~ supp = 1.0/14

    fnm = input("Data file? (.txt assumed) ")
    if fnm.endswith('.td') or fnm.endswith('.txt'):
        filenamefull = fnm
        filename, _ = fnm.rsplit('.',1)
    else:
        filename = fnm
        filenamefull = fnm + ".txt" # of ".td" one day...

    try:
        datafile = open(filenamefull)
        assert datafile._checkReadable()
        # ~ print("File is now open.")
    except (IOError, OSError, AssertionError):
        print("Nonexistent or unreadable file.")
        exit(1)

    supp = float(input("Support bound? (in [0, 1]) "))

    hpar = HyperParam()
    print("Reading in dataset from file", filenamefull)
    d = Dataset(datafile, hpar)

    miner = ClMiner(d, hpar, supp)

    cnt = 0
    lst = list()
    for e in miner.mine_closures():
        cnt += 1
        lst.append(e)

    if lst:
        outfnm = "ref_" + filename + "_" + str(lst[-1].supp) + ".txt"
        with open(outfnm, 'w') as g:
            for e in lst:
                print(e, file = g)
        print("Wrote reference file", outfnm)
    else:
        print("No closures found, no reference file created.")

