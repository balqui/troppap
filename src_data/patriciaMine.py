

Dprime = ["BADFGH","BL","BADFLH","BADFLG","BLGH","BADF"]
IL = "BADFLGH"
count = {"B":6,"A":4,"D":4,"F":4,"L":4,"G":3,"H":3}
supp = {"B":6,"A":4,"D":4,"F":4,"L":4,"G":3,"H":3}
X,h,l = ["" for i in IL],0,0
min_supp = 3

def select(D,X):
    out = []
    for tran in D:
        if set([j for j in X]).issubset(set([j for j in tran])):
            out.append(tran)
    return out

while l<len(IL):
    print("X = %s, h = %s, l= %s"%("".join(X),h,l))
    input()
    if count[IL[l]] < min_supp:
        l += 1
    else:
        if h>0 and IL[l]==X[h-1]:
            print("if True")
            l += 1
            h -= 1
        else:
            X[h] = IL[l]
            h += 1
            print("if False, Generate","".join(X[:h]))
            if l:
                DX = select(Dprime,X[:h])
                print("    D'%s = %s\n"%("".join(X[:h]),DX))
            for i in range(l-1,-1,-1):
                
                print("    make %s.ptr point to head of threaded list for item %s w.r.t. D'%s"%(IL[i],IL[i],"".join(X[:h])))
                print("    %s.count =  support of %s item in D'%s"%(IL[i],IL[i],"".join(X[:h])))
                # Commenting the next line generates all the tree, not just frequent itemsets
                count[IL[i]] = sum([1 for elem in DX if IL[i] in elem])
                print("    new support for ",IL[i],"is",count[IL[i]],"\n")
            l=0

