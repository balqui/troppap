'''
Read in a transactional dataset from a txt file, one transaction per line.
'''

from collections import defaultdict

class Dataset:

    def __init__(self, datafile, hpar):
        self.nrocc = 0
        self.nrtr = 0
        self.univ = set()
        self.transcns = defaultdict(set)
        self.occurncs = defaultdict(set)
        for line in datafile:
            isempty = True
            for el in line.strip().split():
                if len(el) > 0:
                    isempty = False
                    self.nrocc += 1
                    self.univ.add(el)
                    self.transcns[self.nrtr].add(el)
                    self.occurncs[el].add(self.nrtr)
            if not isempty:
                self.nrtr += 1
        self.nrits = len(self.univ)
        hpar.nrtr = self.nrtr
        hpar.nrits = self.nrits
        datafile.close()
        # ~ print("Dataset read in. Consists of " +
            # ~ str(self.nrtr) + " transactions from among " +
            # ~ str(self.nrits) + " different items, with a total of " +
            # ~ str(self.nrocc) + " item occurrences.")

    def inters(self, lstr):
        "for iterable of transactions lstr, return their intersection"
        items = self.univ.copy()
        for t in lstr:
            items &= self.transcns[t]
        return items

    def slow_supp(self, st):
        """
        Find the supporting set of st in ds by means of a full scan.
        Hopefully it is infrequent to need to resort to this slow way.
        CAVEAT: Consider keeping a count of calls to this method.
        """
        exact = False # did it match exactly some transaction?
        transcontain = list()
        for tr in self.transcns:
            if st <= self.transcns[tr]:
                transcontain.append(tr)
                if self.transcns[tr] <= st:
                    exact = True
        return transcontain, exact


