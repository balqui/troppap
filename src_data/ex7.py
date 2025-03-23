from practica7 import TopK
import time

if __name__=='__main__':
    n = 12
    tic = time.time()
    a=TopK('../ect24.td',n)
    x = list(a)
    toc = time.time()
    print("Tiempo",toc-tic,"para",n,"cerrados")
    # ~ for x in a: print(' '.join(e for e in sorted(x)))
    
##    for num,e in enumerate(a):
##        print(" Valor del programa:",sorted(e))
