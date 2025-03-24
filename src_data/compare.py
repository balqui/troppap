from practica7 import TopK
from hyperparam import HyperParam
from yacaree_clminer_noprint import ClMiner
from dataset import Dataset
import time

if __name__=='__main__':
    # ~ datafile = 'ect24.td'
    # ~ datafile = 'markbask.txt'
    datafile = 'cmc-full.txt'
    # ~ n = 12
    n = 1000
    tic = time.time()
    a=TopK(datafile, n)
    x = list(a)
    toc = time.time()
    print("Tiempo Pietracaprina", toc - tic, "para", n, "cerrados")
    print(len(x), n, "(off by one due to empty set?)")

    hpar = HyperParam()
    miner = ClMiner(Dataset(open(datafile), hpar), hpar)
    cnt = 0
    lst = list()
    tic = time.time()
    for e in miner.mine_closures():
        cnt += 1
        lst.append(e)
        if cnt == n: break
    toc = time.time()
    print("Tiempo Yacaree", toc - tic, "para", n, "cerrados")
    print(len(lst), n, cnt, "closures")


    # ~ for x in a: print(' '.join(e for e in sorted(x)))
    
##    for num,e in enumerate(a):
##        print(" Valor del programa:",sorted(e))
