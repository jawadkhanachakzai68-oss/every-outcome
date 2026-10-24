# For each clue of the 17-clue puzzle: how many swap groups (14 cells or fewer) contain that clue and no other clue?
# If a clue were removed, each of those groups would have no clue left, so a second solution would appear.
from sudoku_tools import *
from unavoidable import find_uas
P="52...6.........7.13...........4..8..6......5...........418.........3..2...87....."
puz=parse(P); G=parse("527316489896542731314987562172453896689271354453698217941825673765134928238769145")
clues=set(i for i,d in enumerate(puz) if d)
U=find_uas(G,14); print("groups of 14 cells or fewer:",len(U))
mn=99
for i in sorted(clues):
    priv=[s for s in U if s&clues=={i}]
    mn=min(mn,len(priv))
    print("clue row %d col %d = %d: groups where it is the only clue: %d (smallest %d cells)"%(i//9+1,i%9+1,G[i],len(priv),min(len(s) for s in priv)))
print("fewest for any clue:",mn)
# what a person sees at the start
cand=[0x3FE if d==0 else 1<<d for d in puz]
for i,d in enumerate(puz):
    if d:
        for p in PEERS[i]: cand[p]&=~(1<<d)
ns=sum(1 for i in range(81) if puz[i]==0 and bin(cand[i]).count('1')==1)
hs=0
for u in UNITS:
    for d in range(1,10):
        if any(puz[i]==d for i in u): continue
        if len([i for i in u if puz[i]==0 and cand[i]>>d&1])==1: hs+=1
print("at the start: cells with one possibility:",ns,"; hidden singles:",hs)
