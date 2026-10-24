import sys; sys.path.insert(0,'/home/claude/v9')
from geo import *
import numpy as np, itertools, random
# the 16 symmetries preserving the U/D axis (as set): signed permutation matrices with y -> +-y
def sym16():
    out=[]
    for perm in itertools.permutations(range(3)):
        if perm[1]!=1: continue
        for sg in itertools.product((1,-1),repeat=3):
            M=np.zeros((3,3),dtype=int)
            for i in range(3): M[perm[i],i]=sg[i]   # e_i -> sg[i]*e_perm[i]
            out.append(M)
    return out
S16=sym16(); assert len(S16)==16
CI={p:i for i,p in enumerate(CORNERS)}; EI={p:i for i,p in enumerate(EDGES)}
def conj_state(col,M):
    new=np.zeros(54,dtype=int)
    phi={c:N_FACE[apply(M,FACE_N[c])] for c in range(6)}
    for i,(p,n) in enumerate(FACELETS):
        j=FIDX[(apply(M,p),apply(M,n))]
        new[j]=phi[col[i]]
    return new
def corner_tab(M):
    tab={}
    for i,p in enumerate(CORNERS):
        order=corner_order(p)
        for t in range(3):
            n=order[t]
            p2=apply(M,p); n2=apply(M,n)
            ax2=[k for k,x in enumerate(n2) if x][0]
            order2=corner_order(p2); 
            t2=[k for k,o in enumerate(order2) if [q for q,x in enumerate(o) if x][0]==ax2][0]
            tab[(i,t)]=(CI[p2],t2)
    return tab
def edge_tab(M):
    swapxz = (abs(M[0,0])==0)   # x axis not mapped to x axis
    tab={}
    for i,p in enumerate(EDGES):
        a1,a2=edge_first_second(p)
        p2=apply(M,p)
        b1,b2=edge_first_second(p2)
        for f in (0,1):
            for e in (0,1):
                # axis holding the ref-class sticker
                refax = a1 if f==0 else a2
                if e and swapxz: refax = a2 if refax==a1 else a1   # E-slice: FB colour becomes LR colour
                # in the new slot the reference sticker is the image of that sticker
                # old sticker normal axis refax -> new axis
                nvec=[0,0,0]; nvec[refax]=p[refax]; n2=apply(M,nvec)
                ax2=[k for k,x in enumerate(n2) if x][0]
                tab[(i,f,e)]=(EI[p2],0 if ax2==b1 else 1)
    return tab
