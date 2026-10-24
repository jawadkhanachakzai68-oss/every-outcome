import sys; sys.path.insert(0,'/home/claude/v9')
from sym import *
import numpy as np, itertools, math, json
# all valid twist vectors, flip vectors, slice sets
TW=[t for t in itertools.product(range(3),repeat=8) if sum(t)%3==0]
FL=[f for f in itertools.product(range(2),repeat=12) if sum(f)%2==0]
ES=[e for e in itertools.combinations(range(12),4)]
print('twist',len(TW),'flip',len(FL),'slice',len(ES),'product',len(TW)*len(FL)*len(ES))
TWa=np.array(TW,dtype=np.int8); FLa=np.array(FL,dtype=np.int8)
ESa=np.zeros((len(ES),12),dtype=np.int8)
for k,e in enumerate(ES): ESa[k,list(e)]=1
total=0; rows=[]
for M in S16:
    ct=corner_tab(M); et=edge_tab(M)
    # twist fixed points
    cj=np.zeros((8,3),dtype=int); ct_t=np.zeros((8,3),dtype=int)
    for (i,t),(j,t2) in ct.items(): cj[i,t]=j; ct_t[i,t]=t2
    new=np.zeros_like(TWa)
    for i in range(8):
        # new[:,cj[i,t]] = t2 for t=TWa[:,i]
        j=cj[i,TWa[:,i]]; t2=ct_t[i,TWa[:,i]]
        new[np.arange(len(TWa)),j]=t2
    fixT=int((new==TWa).all(axis=1).sum())
    # flip+slice fixed points
    fixFE=0
    ej=np.zeros((12,2,2),dtype=int); ef=np.zeros((12,2,2),dtype=int)
    for (i,f,e),(j,f2) in et.items(): ej[i,f,e]=j; ef[i,f,e]=f2
    for k in range(len(ES)):
        e_old=ESa[k]
        # image of slice set
        e_new=np.zeros(12,dtype=np.int8)
        for i in range(12): e_new[ej[i,0,e_old[i]]]=e_old[i]
        if not (e_new==e_old).all(): continue
        newF=np.zeros_like(FLa)
        for i in range(12):
            j=ej[i,0,e_old[i]]
            newF[:,j]=ef[i,FLa[:,i],e_old[i]]
        fixFE+=int((newF==FLa).all(axis=1).sum())
    fx=fixT*fixFE; total+=fx; rows.append((fixT,fixFE,fx))
orbits=total//16
print('sum fixed',total,'orbits',orbits,'remainder',total%16)
json.dump({'twist':len(TW),'flip':len(FL),'slice':len(ES),'cosets':len(TW)*len(FL)*len(ES),'orbits':orbits,'rows':rows},open('burnside.json','w'))
