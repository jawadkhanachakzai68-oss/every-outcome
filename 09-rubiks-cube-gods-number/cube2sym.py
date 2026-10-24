import sys; sys.path.insert(0,'/home/claude/v9')
from cube2 import *
import itertools
S=np.load('c2_states.npy'); D=np.load('c2_dist.npy'); N=len(S)
print('states',N)
# symmetry & rotation position maps on the 24 corner stickers
def posmap(M):
    out=np.zeros(24,dtype=np.int64)
    for k,g in enumerate(cidx):
        p,n=FACELETS[g]
        out[k]=loc[FIDX[(apply(M,p),apply(M,n))]]
    return out
mats=[]
for perm in itertools.permutations(range(3)):
    for sg in itertools.product((1,-1),repeat=3):
        M=np.zeros((3,3),dtype=int)
        for i in range(3): M[perm[i],i]=sg[i]
        mats.append(M)
rots=[M for M in mats if round(np.linalg.det(M))==1]
assert len(mats)==48 and len(rots)==24
Sp=[posmap(M) for M in mats]; Rp=[posmap(M) for M in rots]
# DBL corner stickers: slot (-1,-1,-1)
dbl=[loc[FIDX[((-1,-1,-1),n)]] for n in [(-1,0,0),(0,-1,0),(0,0,-1)]]
lut=-np.ones((24,24,24),dtype=np.int64)
for r,R in enumerate(Rp): lut[R[dbl[0]],R[dbl[1]],R[dbl[2]]]=r
Rarr=np.array(Rp)
def inverse(P):
    inv=np.empty_like(P); np.put_along_axis(inv,P.astype(np.int64),np.broadcast_to(np.arange(24),P.shape).astype(P.dtype),axis=1); return inv
def normalize(P):
    # find rotation R with P[R[x]]==x for x in DBL stickers  => R[x]=Pinv[x]
    Pi=inverse(P)
    a=Pi[:,dbl[0]].astype(np.int64); b=Pi[:,dbl[1]].astype(np.int64); c=Pi[:,dbl[2]].astype(np.int64)
    r=lut[a,b,c]; assert (r>=0).all()
    idx=Rarr[r]            # (N,24)
    return np.take_along_axis(P,idx,axis=1)
def transform(P,s):
    Sv=Sp[s]; Sinv=np.argsort(Sv)
    Q=P[:,Sinv]; Pc=Sv[Q.astype(np.int64)].astype(np.uint8)
    return normalize(Pc)
def lexless(h1,l1,h2,l2): return (h1<h2)|((h1==h2)&(l1<l2))
bh=np.full(N,np.iinfo(np.uint64).max,dtype=np.uint64); bl=bh.copy()
SETK=np.zeros(N,dtype=[('hi','u8'),('lo','u8')]); h0,l0=pack(S); SETK['hi']=h0; SETK['lo']=l0
order=np.argsort(SETK,order=('hi','lo')); SETs=SETK[order]
ok_dist=True
def rank(P):
    h,l=pack(P); K=np.zeros(len(P),dtype=[('hi','u8'),('lo','u8')]); K['hi']=h; K['lo']=l
    pos=np.searchsorted(SETs,K); assert (SETs[pos]==K).all(); return order[pos]
minrank=np.full(N,N,dtype=np.int64); minrank_sym=minrank.copy()
for s in range(48):
    T=transform(S,s)
    # invariance of distance under the symmetry
    rk=rank(T)
    if not (D[rk]==D).all(): ok_dist=False; print('dist not invariant for sym',s)
    minrank_sym=np.minimum(minrank_sym,rk)
    rk2=rank(inverse(T))
    minrank=np.minimum(minrank,np.minimum(rk,rk2))
    print('sym',s,'done',flush=True)
cls_sym=len(np.unique(minrank_sym)); cls_all=len(np.unique(minrank))
print('classes by 48 symmetries:',cls_sym,' by symmetries+inverse:',cls_all,'dist invariant:',ok_dist)
# distances of classes
reps=np.unique(minrank); dd=np.bincount(D[reps])
print('class count per distance (symmetry+inverse):',dd.tolist(),'max',len(dd)-1)
import json; json.dump({'states':N,'classes_sym':cls_sym,'classes_sym_inv':cls_all,'dist_invariant':ok_dist,'class_dist':dd.tolist()},open('cube2_sym.json','w'))
