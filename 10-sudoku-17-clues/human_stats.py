# How hard are puzzles for people? Generate random puzzles (remove clues while the solution stays unique),
# then see which techniques the human-style solver needed.
import random, sys
from collections import Counter
from sudoku_tools import *
from human_solver import solve_human
rng=random.Random(2026)
def random_grid():
    puz=[0]*81
    # fill by randomized backtracking
    g=[0]*81
    def rec(i):
        if i==81: return True
        r,c=divmod(i,9)
        opts=[d for d in range(1,10) if all(g[p]!=d for p in PEERS[i] if p<i)]
        rng.shuffle(opts)
        for d in opts:
            g[i]=d
            if rec(i+1): return True
        g[i]=0; return False
    rec(0); return g
def random_minimal(g):
    puz=list(g); order=list(range(81)); rng.shuffle(order)
    for i in order:
        d=puz[i]; puz[i]=0
        if count_solutions(puz,2)[0]!=1: puz[i]=d
    return puz
def level(used):
    if used.get('x-wing'): return 'needs x-wing'
    if used.get('naked triple') or used.get('hidden triple'): return 'needs triples'
    if used.get('naked pair') or used.get('hidden pair'): return 'needs pairs'
    if used.get('locked candidates'): return 'singles + locked candidates'
    return 'singles only'
if __name__=="__main__":
    N=int(sys.argv[1]) if len(sys.argv)>1 else 150
    lv=Counter(); clues=[]
    for k in range(N):
        g=random_grid(); p=random_minimal(g); clues.append(sum(1 for x in p if x))
        ok,used,_=solve_human(p)
        lv[level(used) if ok else 'stuck (ran out of the techniques I coded)']+=1
    print("random minimal puzzles:",N,"clues min/mean/max:",min(clues),round(sum(clues)/N,1),max(clues))
    for k,v in lv.most_common(): print(" ",k,v)
