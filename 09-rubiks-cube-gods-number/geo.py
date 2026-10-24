# Geometric Rubik's cube model: facelet = (cubie position p in {-1,0,1}^3, outward normal n)
import numpy as np, itertools
AX=[(1,0,0),(0,1,0),(0,0,1)]
# face colours: U=0 R=1 F=2 D=3 L=4 B=5  with outward normals
FACE_N={0:(0,1,0),1:(1,0,0),2:(0,0,1),3:(0,-1,0),4:(-1,0,0),5:(0,0,-1)}
N_FACE={v:k for k,v in FACE_N.items()}
FACELETS=[]
for c,n in FACE_N.items():
    for p in itertools.product((-1,0,1),repeat=3):
        if sum(a*b for a,b in zip(p,n))==1: FACELETS.append((p,n))
assert len(FACELETS)==54
FIDX={f:i for i,f in enumerate(FACELETS)}
def rotm(axis_vec,quarter):
    """rotation by quarter*(-90deg) about axis_vec (clockwise as seen from outside that face)"""
    a=np.array(axis_vec); 
    R=np.eye(3,dtype=int)
    # build -90deg rotation about axis via cross product matrix (integer): R90 = a a^T + [a]x  (for +90) ; -90 => a a^T - [a]x
    K=np.array([[0,-a[2],a[1]],[a[2],0,-a[0]],[-a[1],a[0],0]])
    Rm=np.outer(a,a)-K  # -90deg
    out=np.eye(3,dtype=int)
    for _ in range(quarter): out=Rm@out
    return out
def apply(M,v): return tuple(int(x) for x in M@np.array(v))
def move_perm(face,q):
    """perm array P with new_col[j]=col[P[j]] : facelet at j after the move came from P[j]"""
    n=FACE_N[face]; R=rotm(n,q)
    P=list(range(54))
    for i,(p,nn) in enumerate(FACELETS):
        if sum(a*b for a,b in zip(p,n))==1:     # in the turned layer
            j=FIDX[(apply(R,p),apply(R,nn))]
            P[j]=i
    return np.array(P)
MOVES={}   # name -> perm
for f,nm in zip(range(6),'URFDLB'):
    for q in (1,2,3): MOVES[nm+{1:'',2:'2',3:"'"}[q]]=move_perm(f,q)
NAMES=list(MOVES)
def solved(): 
    return np.array([N_FACE[n] for p,n in FACELETS])
def do(col,mv): return col[MOVES[mv]]
# ---- coordinates
CORNERS=[p for p in itertools.product((-1,1),repeat=3)]
EDGES=[p for p in itertools.product((-1,0,1),repeat=3) if sum(1 for x in p if x!=0)==2]
def corner_order(p):
    sx,sy,sz=p
    return [(0,1,0),(1,0,0),(0,0,1)] if sx*sy*sz>0 else [(0,1,0),(0,0,1),(1,0,0)]
def nrm(p,ax):  # outward normal vector along axis ax for slot p
    v=[0,0,0]; v[ax]=p[ax]; return tuple(v)
def corner_orient(col,p):
    order=[(0,1,0),(1,0,0),(0,0,1)] if p[0]*p[1]*p[2]>0 else [(0,1,0),(0,0,1),(1,0,0)]
    for t,axv in enumerate(order):
        ax=[i for i,x in enumerate(axv) if x][0]
        n=nrm(p,ax)
        if col[FIDX[(p,n)]] in (0,3): return t
    raise ValueError
def edge_first_second(p):
    axes=[i for i in range(3) if p[i]!=0]
    a1=1 if 1 in axes else 2    # first facelet: y-axis if present else z
    a2=[a for a in axes if a!=a1][0]
    return a1,a2
def edge_info(col,p):
    a1,a2=edge_first_second(p)
    cf=col[FIDX[(p,nrm(p,a1))]]; cs=col[FIDX[(p,nrm(p,a2))]]
    s={cf,cs}
    ref=[c for c in (0,3) if c in s]
    if not ref: ref=[c for c in (2,5) if c in s]
    ref=ref[0]
    flip=0 if cf==ref else 1
    eslice = s<= {1,2,4,5}
    return flip,eslice
def coords(col):
    tw=tuple(corner_orient(col,p) for p in CORNERS)
    fl=[];es=[]
    for p in EDGES:
        f,e=edge_info(col,p); fl.append(f); es.append(e)
    return tw,tuple(fl),tuple(es)
