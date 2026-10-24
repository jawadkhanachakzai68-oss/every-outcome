# Receipt 2: find the "unavoidable sets" of a solved grid: groups of cells whose digits can be
# swapped around to make a different valid grid. Any puzzle for this grid must give at least
# one clue inside every such group, or a second solution survives.
import sys, time
from sudoku_tools import *
def find_uas(G, maxsize=12):
    old=list(G); found=set()
    def run(S,new,c0):
        # S: set of changed cells, new: dict cell->digit (0 = not decided)
        # 1) a changed cell without a new digit
        for c in sorted(S):
            if new[c]==0:
                for d in range(1,10):
                    if d==old[c]: continue
                    if any(new[p]==d for p in PEERS[c] if p in S): continue
                    # peers outside S that hold d must change as well
                    add=[p for p in PEERS[c] if p not in S and old[p]==d]
                    if any(p<c0 for p in add): continue
                    if len(S)+len(add)>maxsize: continue
                    S2=set(S)|set(add); new2=dict(new); new2[c]=d
                    for p in add: new2[p]=0
                    run(S2,new2,c0)
                return
        # 2) every changed cell's old digit must land somewhere in each of its units
        for c in sorted(S):
            for u in CELL_UNITS[c]:
                dd=old[c]
                if any(q in S and new[q]==dd for q in u): continue
                for q in u:
                    if q==c or q<c0: continue
                    if q in S:
                        if new[q]!=0: continue
                        if any(new[p]==dd for p in PEERS[q] if p in S): continue
                        new2=dict(new); new2[q]=dd; S2=S
                        add=[p for p in PEERS[q] if p not in S and old[p]==dd and p!=q]
                        if add: continue   # keep it simple: handled when q is added fresh
                        run(S2,new2,c0)
                    else:
                        if len(S)+1>maxsize: continue
                        if any(new[p]==dd for p in PEERS[q] if p in S): continue
                        add=[p for p in PEERS[q] if p not in S and old[p]==dd]
                        if any(p<c0 for p in add): continue
                        if len(S)+1+len(add)>maxsize: continue
                        S2=set(S)|{q}|set(add); new2=dict(new); new2[q]=dd
                        for p in add: new2[p]=0
                        run(S2,new2,c0)
                return
        found.add(frozenset(S))
    for c0 in range(81):
        for d in range(1,10):
            if d==old[c0]: continue
            add=[p for p in PEERS[c0] if old[p]==d]
            if any(p<c0 for p in add): continue
            S={c0}|set(add); new={c0:d}
            for p in add: new[p]=0
            if len(S)<=maxsize: run(S,new,c0)
    # keep only minimal sets, and only sets that really are unavoidable (verified below)
    fs=sorted(found,key=len)
    mins=[]
    for s in fs:
        if not any(m<=s for m in mins): mins.append(s)
    return mins
def is_unavoidable(G,S):
    puz=[0 if i in S else G[i] for i in range(81)]
    n,_=count_solutions(puz,2)
    return n>=2
if __name__=="__main__":
    G=parse("527316489896542731314987562172453896689271354453698217941825673765134928238769145")
    t=time.time(); U=find_uas(G,12); print("found",len(U),"minimal unavoidable sets up to size 12 in %.1fs"%(time.time()-t))
    from collections import Counter
    print(sorted(Counter(len(s) for s in U).items()))
    bad=[s for s in U if not is_unavoidable(G,s)]
    print("self-check: sets that are NOT unavoidable:",len(bad))
