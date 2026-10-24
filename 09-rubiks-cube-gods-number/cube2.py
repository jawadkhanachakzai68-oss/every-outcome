import sys; sys.path.insert(0,'/home/claude/v9')
from geo import *
import numpy as np, itertools, time, json
cidx=[i for i,(p,n) in enumerate(FACELETS) if all(abs(x)==1 for x in p)]
assert len(cidx)==24
loc={g:k for k,g in enumerate(cidx)}   # global facelet idx -> 0..23
def restrict(P):
    return np.array([loc[P[g]] for g in cidx])
MV={nm:restrict(MOVES[nm]) for nm in MOVES}
HTM=['U','U2',"U'",'R','R2',"R'",'F','F2',"F'"]
QTM=['U',"U'",'R',"R'",'F',"F'"]
def pack(P):
    P=P.astype(np.uint64)
    hi=np.zeros(len(P),dtype=np.uint64); lo=np.zeros(len(P),dtype=np.uint64)
    for j in range(12): hi=(hi<<np.uint64(5))|P[:,j]
    for j in range(12,24): lo=(lo<<np.uint64(5))|P[:,j]
    return hi,lo
def uniq(P):
    hi,lo=pack(P)
    o=np.lexsort((lo,hi)); hi=hi[o]; lo=lo[o]; P=P[o]
    keep=np.ones(len(P),dtype=bool); keep[1:]=(hi[1:]!=hi[:-1])|(lo[1:]!=lo[:-1])
    return P[keep],hi[keep],lo[keep]
def bfs(moves):
    ident=np.arange(24,dtype=np.uint8)[None,:]
    seen_hi=np.zeros(1,dtype=np.uint64); seen_lo=np.zeros(1,dtype=np.uint64)
    allP=[ident.copy()]; dist=[0]; fr=ident; d=0; counts=[1]
    # keep a global sorted set as structured array for membership
    def key(hi,lo): return hi.astype(object)  # unused
    visP=ident.copy(); H,L=pack(visP)
    SET=np.zeros(1,dtype=[('hi','u8'),('lo','u8')]); SET['hi']=H; SET['lo']=L
    states=[ident]; dists=[np.zeros(1,dtype=np.uint8)]
    while True:
        d+=1
        cand=np.concatenate([fr[:,MV[m]] for m in moves],axis=0)
        cand,h,l=uniq(cand)
        K=np.zeros(len(cand),dtype=[('hi','u8'),('lo','u8')]); K['hi']=h; K['lo']=l
        pos=np.searchsorted(SET,K)
        pos[pos>=len(SET)]=len(SET)-1
        new=~((SET[pos]['hi']==K['hi'])&(SET[pos]['lo']==K['lo']))
        cand=cand[new]; K=K[new]
        if len(cand)==0: break
        counts.append(len(cand)); states.append(cand); dists.append(np.full(len(cand),d,dtype=np.uint8))
        SET=np.sort(np.concatenate([SET,K])); fr=cand
    return counts,np.concatenate(states),np.concatenate(dists)
if __name__=='__main__':
    t=time.time()
    c,S,D=bfs(HTM); print('HTM',c,sum(c),'God',len(c)-1,time.time()-t,flush=True)
    c2,S2,D2=bfs(QTM); print('QTM',c2,sum(c2),'God',len(c2)-1,time.time()-t,flush=True)
    json.dump({'HTM':c,'QTM':c2},open('cube2_counts.json','w'))
    np.save('c2_states.npy',S); np.save('c2_dist.npy',D)
