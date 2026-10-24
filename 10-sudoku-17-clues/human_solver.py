# Receipt 4 (the human side): solve a puzzle only with techniques people use, easiest first,
# and log which ones were needed.
import itertools, sys
from collections import Counter
from sudoku_tools import *
def solve_human(puz, maxlevel=9):
    cand=[0]*81; g=list(puz)
    for i in range(81): cand[i]=0x3FE if g[i]==0 else 1<<g[i]
    used=Counter(); steps=[]
    def place(i,d):
        g[i]=d; cand[i]=1<<d
        for p in PEERS[i]: cand[p]&=~(1<<d)
    for i in range(81):
        if g[i]:
            d=g[i]
            for p in PEERS[i]: cand[p]&=~(1<<d)
    def contradiction(): return any(cand[i]==0 for i in range(81))
    def step():
        # level 1: naked single
        for i in range(81):
            if g[i]==0 and bin(cand[i]).count('1')==1:
                place(i,cand[i].bit_length()-1); return 'naked single'
        # level 1: hidden single
        for u in UNITS:
            for d in range(1,10):
                cells=[i for i in u if g[i]==0 and cand[i]>>d&1]
                if len(cells)==1 and not any(g[i]==d for i in u):
                    place(cells[0],d); return 'hidden single'
        # level 2: locked candidates
        for u in UNITS:
            for d in range(1,10):
                cells=[i for i in u if g[i]==0 and cand[i]>>d&1]
                if len(cells)<2: continue
                for u2 in UNITS:
                    if u2 is u or u2==u: continue
                    if all(c in u2 for c in cells):
                        kill=[i for i in u2 if i not in u and g[i]==0 and cand[i]>>d&1]
                        if kill:
                            for i in kill: cand[i]&=~(1<<d)
                            return 'locked candidates'
        # level 3: naked pairs / triples
        for size,name,lvl in ((2,'naked pair',3),(3,'naked triple',4)):
            if lvl>maxlevel: break
            for u in UNITS:
                free=[i for i in u if g[i]==0]
                for combo in itertools.combinations(free,size):
                    m=0
                    for i in combo: m|=cand[i]
                    if bin(m).count('1')==size:
                        kill=[i for i in free if i not in combo and cand[i]&m]
                        if kill:
                            for i in kill: cand[i]&=~m
                            return name
        # hidden pairs / triples
        for size,name,lvl in ((2,'hidden pair',3),(3,'hidden triple',4)):
            if lvl>maxlevel: break
            for u in UNITS:
                free=[i for i in u if g[i]==0]
                digs=[d for d in range(1,10) if any(cand[i]>>d&1 for i in free)]
                for dc in itertools.combinations(digs,size):
                    cells=[i for i in free if any(cand[i]>>d&1 for d in dc)]
                    if len(cells)==size:
                        m=sum(1<<d for d in dc); ch=False
                        for i in cells:
                            if cand[i]&~m: cand[i]&=m; ch=True
                        if ch: return name
        # level 5: X-wing
        if maxlevel>=5:
            for d in range(1,10):
                for units,other in ((ROWS,COLS),(COLS,ROWS)):
                    pos={}
                    for k,u in enumerate(units):
                        cs=[j for j,i in enumerate(u) if g[i]==0 and cand[i]>>d&1]
                        if len(cs)==2: pos[k]=tuple(cs)
                    for a,b in itertools.combinations(pos,2):
                        if pos[a]==pos[b]:
                            ch=False
                            for j in pos[a]:
                                for k,i in enumerate(other[j]):
                                    pass
                                for i in other[j]:
                                    r=units.index(next(u for u in units if i in u))
                                    if r not in (a,b) and g[i]==0 and cand[i]>>d&1:
                                        cand[i]&=~(1<<d); ch=True
                            if ch: return 'x-wing'
        return None
    while any(x==0 for x in g):
        if contradiction(): return None,used,g
        t=step()
        if t is None: return False,used,g
        used[t]+=1
    return True,used,g
if __name__=="__main__":
    P=sys.argv[1] if len(sys.argv)>1 else "52...6.........7.13...........4..8..6......5...........418.........3..2...87....."
    puz=parse(P)
    ok,used,g=solve_human(puz)
    print("solved with human techniques only:",ok,dict(used),"filled",sum(1 for x in g if x),"of 81")
