# Boros et all naive implementation

a=[[1,1,1,1,1],
   [0,1,1,1,1],
   [0,1,1,1,1],
   [1,1,0,0,1],
   [0,0,1,1,1],
   [0,1,0,0,1],
   [1,0,0,0,1],
   [1,0,0,0,1],
   [1,0,0,0,1],
   [1,1,0,0,0],
   [1,1,0,0,0],
   [1,1,0,0,0],
   [1,1,0,0,0],
   [0,0,1,1,0],
   [0,0,1,1,0],
   [0,0,1,1,0],
   [0,0,1,1,0],
   [0,0,1,1,0],
   [0,0,1,1,0],
   [0,1,0,0,0],
   [0,1,0,0,0],
   [1,0,0,0,0],
   [1,0,0,0,0],
   [1,0,0,0,0]]

##a=[[1,1,1,1,1],
##   [1,1,1,1,1],
##   [1,1,1,1,1],
##   [1,1,0,0,1],
##   [1,0,1,1,1],
##   [1,1,0,0,1],
##   [1,0,0,0,1],
##   [1,0,0,0,1],
##   [1,0,0,0,1],
##   [1,1,0,0,0],
##   [1,1,0,0,0],
##   [1,1,0,0,0],
##   [1,1,0,0,0],
##   [1,0,1,1,0],
##   [1,0,1,1,0],
##   [1,0,1,1,0],
##   [1,0,1,1,0],
##   [1,0,1,1,0],
##   [1,0,1,1,0],
##   [1,1,0,0,0],
##   [1,1,0,0,0],
##   [1,0,0,0,0],
##   [1,0,0,0,0],
##   [1,0,0,0,0]]

# a is a list of lists of 0's and 1's - i.e., an array
# l is a list of indices
def computeH(a,l):
    result=[]
    for j in range(len(a)):
        output=True
        for i in l:
            if a[j][i]==0:
                output=False
        if output:
            result.append(j)
    return result

def computeMaximal(l):
    newl=[]
    for i in range(len(l)-1):
        toadd=True
        for j in range(i+1,len(l)):
            if set(l[i][1])==set(l[j][1]):
                l[i]=(list(set(l[j][0]+l[i][0])),l[i][1])
                l[j]=l[i]
            else:
                if len(set(l[i][1]).difference(set(l[j][1])))==0: #if l[i] is strictly included in l[j]
                    toadd=False
        if toadd:
            if l[i] not in newl:
                newl.append(l[i])
                
    return newl
                                            
t=len(a)
k=1
alph=[0,1,2,3,4]
closureempty=[]
for x in alph:
    if len(computeH(a,[x]))==len(a):
        closureempty.append(x)

d=[closureempty] # put in d the closure of the emptyset

print(d)

while t>=k:
    listallH=[]
    print("Compute D"+str(t))
    for c in d:
        for x in set(alph).difference(set(c)):
            listallH.append((c+[x],computeH(a,c+[x])))
    d=[closureempty]
    for s,h in computeMaximal(sorted(listallH,key=len,reverse=True)):                           
        if len(h)>=t:
            d.append(s)
    print(d)
    t=t-1
    




