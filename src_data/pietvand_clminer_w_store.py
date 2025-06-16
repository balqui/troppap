# -*- coding: cp1252 -*-
'''
To Do immediately:
  - change direct use of heap into detour compatible with store.py
  - end up with a PV implementation "w_store"
  - keep checking it out at each step wrt the reference files
  - is "japanese+heap" = "italian" ? Must start by understanding LCM v1 (v2, v3...)
'''

import heapq
import time

from itset import ItSet # overrides comparison so that standard heapq works
from store import Store

from collections import defaultdict
class TopK:
    '''This class implements an iterator for getting the first K closed sets'''
    def __init__(self, nameFile,K=2):
        '''Initialize the attributes
        - transactions: a list of all transactions in the
        dataset (a transaction is a set of items),
        - items: a list of all items,
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
                d[item]+=1
        self.items=[x for x,y in sorted(list(d.items()),key=lambda x: x[1],reverse=True)] #all the items in descdending oreder of support
        self.l=len(self.transactions) # number of transactions
        self.l_items=len(self.items) #number of items

        
    def __iter__(self):
        '''
        This method is necessary to initialize the
        iterator.
        No it isn't, we could use generators. I leave it as is though. -JLB
        '''
        # ~ self.q=[]
        # ~ heapq.heapify(self.q) # Unnecessary, it is empty
        self.q = Store(use_heap = False)
        self.generatedK=0
        clos_empty = self.intersect(self.transactions)
        self.q.spush(ItSet(clos_empty, self.transactions, 0))
        return self
    
    def jth_prefix(self,itemset,j):
        '''
        This method returns the jth prefix of an itemset
        (Assume the alphabet is indexed from 1 to n)
        '''
        result=set([])
        #################  TO DO #######################
        result = itemset.intersection(set(self.items[:j]))
        ################################################
        return result
    
    def extract_trans(self,it,trans_list):
        '''
        This method receives as parameters an item it
        and a list of transactions (each being a set of items)
        and filters the list of transactions, returning only
        those that contain the item it
        '''
        result=[set()]
        #################  TO DO #######################
        result=[trans for trans in trans_list if it in trans]
        ################################################
        return result
    
    def intersect(self,trans_list):
        '''
        This method returns the set of items that are included
        in all transactions in trans_list. If trans_list is empty,
        it returns the set of all items
        '''
        result=set(self.items)
        #################  TO DO #######################
        if trans_list:
            result=trans_list[0]
            for elem in trans_list[1:]:
                result=result.intersection(elem)
        ################################################
        return result
    

    def __next__(self):
        '''
        This method is the main function of the class. It throws
        StopIteration if more elements than necessary are generated
        or if there is no other closed set in the priority queue.
        
        '''
        if self.generatedK>self.K or not self.q:
            raise StopIteration
        # ~ Ysupp,(Yitems,Ytrans_list,Ycore)=heapq.heappop(self.q)
        Yy = self.q.spop()
        Ysupp, Yitems, Ytrans_list, Ycore = Yy.supp, set(Yy), Yy.supportset, Yy.core
        #################  TO DO #######################
        #You will have to compute the next possible succesors
        #and push them to the priority queue q. For each of
        #them you should compute:
        #  next_items = the next closed itemset
        #  next_supp = the support of the next closed itemset
        #  next_trans_list = the list of all transactions
        #                   containing the items in next_items
        #  next_core = the core of next_items
        #The command for adding this element to the priority queue is:
        #heapq.heappush(self.q,(self.l-next_supp,(next_items,next_trans_list,next_core)))
        for j in range(Ycore+1,self.l_items+1):
            aj=self.items[j-1]
            if aj not in Yitems:
                next_trans_list=self.extract_trans(aj,Ytrans_list)
                next_items = self.intersect(next_trans_list)
                if self.jth_prefix(next_items,j-1)==self.jth_prefix(Yitems,j-1):
                    next_supp=len(next_trans_list)
                    next_core=j
                    self.q.spush(ItSet(next_items, next_trans_list, next_core))
        ################################################                   
        self.generatedK=self.generatedK+1
        return Yitems


if __name__=='__main__':
    n = 12
    tic = time.time()
    # ~ a=TopK('ect24.td',n)
    a=TopK('ejemploPV.txt',n)
    x = list(a)
    toc = time.time()
    print("Tiempo",toc-tic,"para",n,"cerrados")
    for x in a: print(' '.join(e for e in sorted(x)))
    
##    for num,e in enumerate(a):
##        print(" Valor del programa:",sorted(e))

# VARIOUS ALTERNATIVE MAINS

# ~ if __name__=='__main__':
    # ~ print("hola")
    # ~ a=TopK('ex7data.txt',10)
    # ~ i=0
    # ~ for e in a:
        # ~ print(i)
        # ~ i+=1
        
##if __name__=='__main__':
##    print("hola")
##    a=TopK('ex6data.txt',60)
##    nota=0
##    cond=True
##    itemset=set(['dairy', 'freshmeat', 'confectionery', 'Female', 'cannedveg'])
##    if a.jth_prefix(itemset,0)!=set([]):
##        cond=False
##    if a.jth_prefix(itemset,4)!=set(['dairy', 'confectionery', 'freshmeat']):
##        cond=False
##    if a.jth_prefix(itemset,5)!=set(['dairy', 'confectionery', 'freshmeat']):
##        cond=False
##    if a.jth_prefix(itemset,10)!= set(['dairy', 'cannedveg', 'confectionery', 'freshmeat', 'Female']):
##        cond=False
##    if cond:
##        nota+=20
##        print('jth_prefix=ok')
##    else:
##        print('jth_prefix=not ok')
##
##    lista=[set(['freshmeat', 'Female', 'DoNotOwnHome']), set(['beer', 'Male', 'freshmeat', 'DoNotOwnHome']), set(['cannedmeat', 'fruitveg', 'Female', 'DoNotOwnHome']), set(['fish', 'Male', 'DoNotOwnHome']), set(['Male', 'frozenmeal', 'Homeowner']), set(['softdrink', 'wine', 'freshmeat', 'Female', 'DoNotOwnHome']), set(['Male', 'wine', 'Homeowner']), set(['confectionery', 'fish', 'wine', 'Female', 'Homeowner']), set(['confectionery', 'cannedveg', 'cannedmeat', 'softdrink', 'Male', 'Homeowner']), set(['dairy', 'Male', 'fruitveg', 'confectionery', 'DoNotOwnHome']), set(['beer', 'Male', 'Homeowner']), set(['confectionery', 'fruitveg', 'Homeowner', 'dairy', 'Female', 'freshmeat', 'wine']), set(['confectionery', 'fruitveg', 'beer', 'Female', 'DoNotOwnHome', 'wine']), set(['Male', 'frozenmeal', 'DoNotOwnHome']), set(['beer', 'cannedveg', 'Male', 'frozenmeal', 'Homeowner']), set(['fish', 'fruitveg', 'Female', 'DoNotOwnHome']), set(['fish', 'Male', 'freshmeat', 'frozenmeal', 'DoNotOwnHome']), set(['Female', 'Homeowner']), set(['Female', 'Homeowner']), set(['freshmeat', 'fruitveg', 'Female', 'Homeowner']), set(['beer', 'cannedveg', 'Male', 'frozenmeal', 'Homeowner']), set(['confectionery', 'fruitveg', 'cannedmeat', 'Homeowner', 'beer', 'Female']), set(['cannedmeat', 'Male', 'dairy', 'Homeowner']), set(['freshmeat', 'confectionery', 'fruitveg', 'Female', 'Homeowner']), set(['softdrink', 'cannedmeat', 'Female', 'DoNotOwnHome']), set(['fruitveg', 'cannedveg', 'cannedmeat', 'beer', 'frozenmeal', 'wine', 'Male', 'fish', 'DoNotOwnHome']), set(['softdrink', 'Male', 'freshmeat', 'fish', 'Homeowner']), set(['confectionery', 'beer', 'Male', 'dairy', 'Homeowner']), set(['beer', 'fruitveg', 'fish', 'Female', 'DoNotOwnHome']), set(['cannedveg', 'Homeowner', 'beer', 'frozenmeal', 'Male', 'wine'])]
##    cond=True
##    if a.extract_trans('freshmeat',lista)!=[set(['freshmeat', 'Female', 'DoNotOwnHome']), set(['beer', 'Male', 'freshmeat', 'DoNotOwnHome']), set(['DoNotOwnHome', 'wine', 'freshmeat', 'Female', 'softdrink']), set(['confectionery', 'fruitveg', 'Homeowner', 'dairy', 'Female', 'freshmeat', 'wine']), set(['fish', 'Male', 'freshmeat', 'frozenmeal', 'DoNotOwnHome']), set(['fruitveg', 'freshmeat', 'Female', 'Homeowner']), set(['fruitveg', 'confectionery', 'freshmeat', 'Female', 'Homeowner']), set(['Homeowner', 'fish', 'Male', 'freshmeat', 'softdrink'])]:
##        cond=False
##    if a.extract_trans('freshmeat',[])!=[]:
##        cond=False
##    if cond:
##        nota+=20
##        print('extract_trans=ok')
##    else:
##        print('extract_trans=not ok')
##    lista=[set(['fruitveg', 'cannedveg', 'dairy', 'Female', 'wine', 'freshmeat', 'fish', 'DoNotOwnHome']), set(['fruitveg', 'cannedveg', 'cannedmeat', 'Homeowner', 'beer', 'dairy', 'frozenmeal', 'Male', 'freshmeat', 'wine']), set(['confectionery', 'cannedveg', 'Homeowner', 'dairy', 'frozenmeal', 'Male', 'freshmeat', 'fish']), set(['confectionery', 'cannedveg', 'Homeowner', 'dairy', 'Female', 'freshmeat', 'wine']), set(['fruitveg', 'cannedveg', 'softdrink', 'dairy', 'Female', 'wine', 'freshmeat', 'fish', 'DoNotOwnHome']), set(['confectionery', 'fruitveg', 'cannedveg', 'softdrink', 'dairy', 'Male', 'freshmeat', 'DoNotOwnHome']), set(['cannedveg', 'cannedmeat', 'Homeowner', 'beer', 'dairy', 'frozenmeal', 'softdrink', 'Male', 'freshmeat', 'wine']), set(['fruitveg', 'cannedveg', 'cannedmeat', 'softdrink', 'dairy', 'Female', 'freshmeat', 'DoNotOwnHome']), set(['cannedveg', 'beer', 'dairy', 'frozenmeal', 'Male', 'freshmeat', 'DoNotOwnHome']), set(['confectionery', 'cannedveg', 'beer', 'dairy', 'frozenmeal', 'Male', 'freshmeat', 'fish', 'DoNotOwnHome']), set(['confectionery', 'cannedveg', 'beer', 'dairy', 'frozenmeal', 'Male', 'freshmeat', 'DoNotOwnHome']), set(['cannedveg', 'dairy', 'Female', 'DoNotOwnHome', 'freshmeat', 'fish', 'wine'])]
##    cond=True
##    if a.closure(lista)!=set(['dairy', 'cannedveg', 'freshmeat']):
##        cond=False
##    if cond:
##        nota+=20
##        print('closure=ok')
##    else:
##        print('closure=not ok')
##    acerted=0
##    i=0
##
##    for e in a:
##        i+=1
##        if i==13:
##            if e==set(['Female', 'Homeowner']):
##                acerted+=1
##            else:
##                print('el elemento decimotercero deberia ser set([\'Female\', \'Homeowner\'] y es ',e)
##        if i==18:
##            if e==set(['cannedmeat']):
##                acerted+=1
##            else:
##                print('el elemento decimoctavo deberia ser set([\'cannedmeat\'] y es ',e)
##        if i==27:
##            if e==set(['dairy']):
##                acerted+=1
##            else:
##                print('el elemento vigesimo septimo deberia ser set([\'dairy\'] y es ',e)
##        if i==53:
##            if e==set(['confectionery', 'Female', 'wine']):
##                acerted+=1
##            else:
##                print('el elemento quincuagesimo tercero deberia ser set([\'confectionery\', \'Female\', \'wine\']) y es ',e)
##    if acerted==4:
##        print("next=ok")
##    else:
##        if acerted>1:
##            print("next=partially ok")
##        else:
##            print("next=not ok")
##    print(nota+acerted*10)


