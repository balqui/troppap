"""
Based on yacaree, tuned for Pietracaprina/Vandin by adding the core item

Current revision: late Prairial 2025

Author: Jose Luis Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Careful: 
(1) A hash is defined to use ItSet's as set members and 
dict keys; ItSet should be handled always as immutable 
even though the program does not control that instances 
don't change.
(2) Comparison < redefined to be support-based instead 
of set inclusion.
"""

class ItSet(set):

    cnt = 0 # counts created ItSet's to set up the tie-breaking label


    def __init__(self, contents = set(), infosupp = -1, core = 0):
        """
        Current closure miner puts in heap pending closures with
        their supporting set of transactions. Maybe one day I can
        bet rid of that list and store only the support but, as of
        today, I keep it.
        """
        super().__init__(contents)
        self._hash = hash(frozenset(contents))
        self.core = core
        if type(infosupp) == int:
            self.supp = infosupp
            self.supportset = None
        else:
            "assumed something with a length"
            self.supp = len(infosupp)
            self.supportset = infosupp
        self.suppratio = float("inf") # default
        ItSet.cnt += 1
        self.label = ItSet.cnt
        self.is_closed = False


    def _break_tie(self, other):
        "We end up needing that singletons compare the items."
        if len(self) == 1 == len(other):
            "cannot compare directly as sets but avoid extracting items"
            return list(self) < list(other)
        else:
            return self.label < other.label


    def __lt__(self, other):
        """
        For heap purposes, ItSet-smaller itemsets will come out first,
        hence these must be the ones with larger supports. Support ties
        are broken arbitrarily by creation time order except singletons.
        Rest of order comparisons are set-theoretic on the contents BUT
        be careful as set comparison is not total.
        """
        return (self.supp > other.supp or
                self.supp == other.supp and self._break_tie(other))


    def __hash__(self):
        """
        Make it hashable so that they can be in set's and
        index dict's exactly as the frozenset of the contents.
        """
        return self._hash


    # ~ def __str__(self):
        # ~ return ('{ ' + ', '.join(sorted(str(e) for e in self)) +
                       # ~ ' } [' +  str(self.supp) + ']')

    def __str__(self):
        "TEMPORARY WHILE TESTING makerefs AND closchecker"
        return (','.join(sorted(str(e) for e in self)) +
                       '/' +  str(self.supp))

    # ~ def fullstr(self):
        # ~ s = '[X]' if self.supportset is None else str(sorted(self.supportset))
        # ~ return str(self) + ' / ' + s


if __name__ == "__main__":

    # ~ PENDING: test printing and all the comparisons with all cases, also difference

    print(ItSet([], range(100, 120)))
    s0 = ItSet([], range(100, 120))
    print(s0)
    s1 = ItSet([], range(150, 175))
    print(s1)
    print(ItSet(range(5), range(200, 210)))
    s2 = ItSet(range(5), range(200, 210))
    print(s2)

    print("s0 == s1", s0 == s1)
    print("s0 == s2", s0 == s2)
    print("s2 == s1", s2 == s1)

    a = ItSet(range(5), range(30))
    print("s1", s1)
    print("s2", s2)
    print("a", a)
    print("s2 < a", s2 < a)
    print("a < s2", a < s2)
    print("s2 > a", s2 > a)
    print("set(s2) == set(a)", set(s2) == set(a))
    print("s2 == a", s2 == a)
    print("set(s2) < set(a)", set(s2) < set(a))
    print("set(s2) <= set(a)", set(s2) <= set(a))
    print("s2 << a", s2 << a)
    print("a << s2", a << s2)

    print("s0 found in [s1, s2]?", s0 in [s1, s2])

    b = a.difference([2, 3])
    print(b, type(b))

    print(set([s0, s1, s2, a]))
