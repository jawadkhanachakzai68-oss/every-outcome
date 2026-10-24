# Receipt 5: the same question on a tiny 4x4 Sudoku (2x2 boxes), answered by brute force.
import itertools
N=4
def peers(i):
    r,c=divmod(i,4); s=set()
    for k in range(4): s.add(r*4+k); s.add(k*4+c)
    br,bc=r//2*2,c//2*2
    for a in range(2):
        for b in range(2): s.add((br+a)*4+bc+b)
    s.discard(i); return s
PE=[peers(i) for i in range(16)]
def solutions(puz,limit=2):
    g=list(puz); out=[]
    def rec():
        if len(out)>=limit: return
        best=-1; bo=None
        for i in range(16):
            if g[i]==0:
                opts=[d for d in range(1,5) if all(g[p]!=d for p in PE[i])]
                if bo is None or len(opts)<len(bo): best,bo=i,opts
                if len(opts)==0: return
        if best<0: out.append(list(g)); return
        for d in bo:
            g[best]=d; rec(); g[best]=0
    rec(); return out
grids=solutions([0]*16,10**6)
print("4x4 grids:",len(grids))
best=99; cnt={}
for k in range(1,6):
    n=0
    for G in grids:
        for cells in itertools.combinations(range(16),k):
            puz=[G[i] if i in cells else 0 for i in range(16)]
            if len(solutions(puz,2))==1: n+=1
    cnt[k]=n
    print("clues",k,": puzzles with exactly one solution:",n)
    if n and best==99: best=k
print("fewest clues that can give one solution:",best)
