"""
Two options for storage of the generated closures with lowish support
that must wait for their turn: traditional heap and dict of sets.

The dict of sets is relevant mainly because it allows for faster 
tests of duplicates.
"""

from heapq import heappush, heappop
from collections import defaultdict

class Store:

    def __init__(self, use_heap = True):
        self.h = list()
        self.d = defaultdict(set)
        self.mxsupp = 0 # keep self.d[mxsupp] nonempty if d nonempty
        self.total = 0  # for len, not really for emptiness test
        self.use_heap = use_heap
        print("Store use_heap:", use_heap)

    def spush(self, iset):
        if self.use_heap:
            heappush(self.h, iset)
        else:
            self.mxsupp = max(self.mxsupp, isupp := iset.supp)
            self.total += 1
            self.d[isupp].add(iset)

    def spop(self):
        if self.use_heap:
            return heappop(self.h)
        else:
            self.total -= 1
            r = self.d[self.mxsupp].pop()
            while self.mxsupp > 0 and not self.d[self.mxsupp]:
                self.mxsupp -= 1
            return r

    def __bool__(self):
        "emptiness test"
        if self.use_heap:
            return bool(self.h)
        else:
            return self.total > 0
            # ~ return self.mxsupp > 0

    def __contains__(self, iset):
        "membership test"
        if self.use_heap:
            return iset in self.h
        else:
            return iset in self.d[iset.supp]

    def __len__(self):
        if self.use_heap:
            return len(self.h)
        else:
            return self.total
