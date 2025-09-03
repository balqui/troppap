# -*- coding: cp1252 -*-
##from hyperparam import HyperParam
##from dataset import Dataset
import time


import heapq
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
        self.items=[x for x,y in sorted(list(d.items()),key=lambda x: x[1],reverse=True)] #all the items in descdending order of support
        self.l=len(self.transactions) # number of transactions
        self.l_items=len(self.items) #number of items
        self.supplists = defaultdict(lambda:[])
        self.suppsingl = defaultdict(lambda:[])

        
    def __iter__(self):
        '''
        This method is necessary to initialize the
        iterator.
        '''
        self.q=[]
        heapq.heapify(self.q)
        self.generatedK=0
        element=self.closure(self.transactions)
        heapq.heappush(self.q,(0,(element,self.transactions)))
        return self
    
    def jth_prefix(self,itemset,j):
        '''
        This method returns the jth prefix of an itemset
        (Assume the alphabet is indexed from 1 to n)
        '''
##        result=set([])
        #################  TO DO #######################
        result = itemset.intersection(set(self.items[:j]))
        ################################################
        return result

    def jth_suffix(self,itemset,j):
        '''
        This method returns the jth suffix of an itemset
        (Assume the alphabet is indexed from 1 to n)
        '''
##        result=set([])
        #################  TO DO #######################
        result = itemset.intersection(set(self.items[j:]))
        ################################################
        return result
    
    def extract_trans(self,it,trans_list):
        '''
        This method receives as parameters an item it
        and a list of transactions (each being a set of items)
        and filters the list of transactions, returning only
        those that contain the item it
        '''

        #################  TO DO #######################
        result=[trans for trans in trans_list if it in trans]
        ################################################
        return result


    
    def closure(self,trans_list):
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
        if self.generatedK>=self.K or not self.q:
            raise StopIteration
        Ysupp,(Yitems,Ytrans_list)=heapq.heappop(self.q)
       # Ysupp = self.l-Ysupp
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
        m = 0
        for j in range(self.l_items):
            aj=self.items[j]
            if aj not in Yitems:
                X_items = self.jth_suffix(Yitems,j+1)
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
                if next_supp>m and self.jth_suffix(next_items,j+1)==self.jth_suffix(Yitems,j+1):
                    if next_supp>self.l-Ysupp:
                        break
                    else:
                        m = next_supp
                        heapq.heappush(self.q,(self.l-next_supp,(next_items,next_trans_list)))
        ################################################                   
        self.generatedK=self.generatedK+1
        return Yitems

if __name__ == "__main__":
    for iii in range(10):
        with open("times_10_troppus_by_C.txt","a") as f:
            names = ["supermarketTr","NOW","papersTr","votesTr","mushroomTr","connect.td","chess.td","cmc-full","adultrain"]
            for i in range(len(names)):
                fnm = names[i]
                if fnm.endswith('.td') or fnm.endswith('.txt'):
                    filenamefull = fnm
                    filename, _ = fnm.rsplit('.',1)
                else:
                    filename = fnm
                    filenamefull = fnm + ".txt" # of ".td" one day...

                try:
                    datafile = open("datasets/"+filenamefull)
                    assert datafile._checkReadable()
                    print(filenamefull,"File is now open.\n")
                except (IOError, OSError, AssertionError):
                    print(filenamefull,"Nonexistent or unreadable file.")
                    exit(1)
                f.write("Reading in dataset from file %s \n"%filenamefull)
##                l1 = [415,7,22,83,234,63812,2351,5,137]
##                l2 = [4627,1597,721,435,8124,67557,3196,1473,32561]
##                ratio = [0.0897, 0.004, 0.031, 0.191, 0.0289, 0.94457, 0.7357, 0.0034, 0.00423]
                n_of_closures = [11834,1456,3001,11806,23191,1029,14164,19936,33201]
                n_of_closures = [10]*9
                miner = TopK("datasets/"+filenamefull,n_of_closures[i])
                lcl = list()
                t0 = time.time()
                for cl in miner:
                    lcl.append(cl)
                t1 = time.time()

                f.write("Time: %.3f\n"%(t1 - t0))
                f.write(f"Number of closures: {len(lcl)} of " + f"support 0 of more.\n") # the 0 is because I don't have the info of last supp
                g = open("troppus_by_C_%s_iter_%s.txt"%(fnm,iii),"w")            # but I want to keep the same structure of the output
                for elem in lcl:
                    g.write(str(elem)+"\n")
                g.close()
  

