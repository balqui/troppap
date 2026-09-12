# -*- coding: cp1252 -*-
import heapq
from collections import defaultdict

class TroppusRev:
    '''This class implements an iterator for getting the first K closed sets
    Almost as Cristina's code in "compare_reverse.py"
    '''

    def __init__(self, nameFile,K=2):
        '''Initialize the attributes
        - transactions: a list of all transactions in the
        dataset (a transaction is a set of items),
        - items: a list of all items,
              (in order of ascending support, hence later traversal backwards)
        - l: the number of transactions
        - l_items: the number of items
        '''
        self.K=K
        self.transactions=[] #all transactions as a list of sets of items
        d=defaultdict(lambda:0) # all items with their frequencies
        for tran in open(nameFile):
            tran_items=set(tran.strip().split())
            self.transactions.append(tran_items)
            for item in tran_items:
                "changed, it was tran.strip().split()"
                d[item]+=1

        # ~ aaa = [x for x,y in sorted(list(d.items()),key=lambda x: x[1],reverse=True)] #all the items in descending order of support
        # ~ self.items=list(reversed(aaa))                                               # new line
        # ~ self.items = list(x for x in sorted(d, key = lambda x: d[x])) # ascending support

        self.items = list(sorted(d, reverse = True)) # by name, stability then uses it for support tie-breaks 
        self.items.sort(key = lambda x: d[x]) # ascending support
        print(self.items)
        self.l=len(self.transactions) # number of transactions
        self.l_items=len(self.items) #number of items
        self.supplists = defaultdict(lambda:[])
        self.suppsingl = defaultdict(lambda:[])


    def __iter__(self):
        '''
        This method is necessary to initialize the
        iterator.
        Since Python 3.14 there is a max-heap variant in the 
        standard library (but JLB's laptop still is at 3.12).
        '''
        self.q=[]
        # ~ heapq.heapify(self.q) # unnecessary, it is empty
        self.generatedK=0
        element=self.closure(self.transactions)
        heapq.heappush(self.q,(0,(element,self.transactions)))
        return self
    
    def jth_prefix(self,itemset,j):
        '''
        This method returns the jth prefix of an itemset
        (Assume the alphabet is indexed from 1 to n)
        (What does that mean? -JLB)
        '''
        # ~ result = itemset.intersection(set(self.items[:j]))
        result = itemset.intersection(self.items[:j]) # method accepts any iterable, spare type cast
        return result

   
    def closure(self,trans_list):
        '''
        This method returns the set of items that are included
        in all transactions in trans_list. If trans_list is empty,
        it returns the set of all items
        '''
        result=set(self.items)
        if trans_list:
            result=trans_list[0]
            for elem in trans_list[1:]:
                result=result.intersection(elem)
        return result
    

    def __next__(self):
        '''
        This method is the main function of the class. It throws
        StopIteration if more elements than necessary are generated
        or if there is no other closed set in the priority queue.
        '''
        if self.generatedK>=self.K or not self.q:
            raise StopIteration
        Ysupp,(Yitems,Ytrans_list)=heapq.heappop(self.q)
        print(f"yield: {sorted(Yitems)}: {self.l - Ysupp}")
        m = 0
        for j in reversed(range(self.l_items)):
            "not very pythonic... :D"
            aj=self.items[j]
            print(f"    consider: {aj} (already in current set? {aj in Yitems})")
            if aj not in Yitems:
                X_items = self.jth_prefix(Yitems,j)  #new line
                single = not bool(X_items)
                X_items.add(aj)
                X_items=frozenset(X_items)
                if X_items in self.supplists:
                    next_trans_list = self.supplists[X_items]
                else:
                    if single:
                        next_trans_list = [t for t in self.transactions if aj in t]
                    else:
                        next_trans_list = [t for t in self.suppsingl[aj] if X_items.issubset(t)]
                    self.supplists[X_items] = next_trans_list
                next_items=self.closure(next_trans_list)
                if single:
                    self.suppsingl[aj] = next_trans_list
                self.supplists[frozenset(next_items)] = next_trans_list
                next_supp = len(next_trans_list)
                if self.jth_prefix(next_items,j)!=self.jth_prefix(Yitems,j):
                    print(f"      support: {next_supp} (current m: {m})")
                    print(f"      closure fails: adds at wrong side of {self.items[j]} on {sorted(Yitems)} giving {sorted(next_items)}")
                if next_supp <= m:
                        print(f"      fails growing support {sorted(next_items)}: {next_supp} not larger than {m}")
                if next_supp>m and self.jth_prefix(next_items,j)==self.jth_prefix(Yitems,j):    #new line
                    if next_supp>self.l-Ysupp:
                        print(f"  break at {self.items[j]} with {sorted(next_items)}: {next_supp} > {self.l - Ysupp}")
                        break
                    else:
                        m = next_supp
                        heapq.heappush(self.q,(self.l-next_supp,(next_items,next_trans_list)))               
                        print(f"  push: {sorted(next_items)}: {next_supp}")
        self.generatedK=self.generatedK+1
        return Yitems, self.l - Ysupp


if __name__=='__main__':

    # ~ from collections import Counter
    # ~ cnt = Counter()

    print("TroppusRev:")
    print("----------")
    # b = TroppusRev('micromarket.txt',31)
    # b = TroppusRev('minimarket.txt',115)
    # b = TroppusRev('e13alt.txt', 11)
    b = TroppusRev('e13alt2.txt', 11)
    print([(sorted(e[0]), e[1]) for e in b])

