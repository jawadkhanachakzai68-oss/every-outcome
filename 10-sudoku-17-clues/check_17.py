# Receipt 1: a real 17-clue puzzle. Is it unique? Is every one of the 17 clues needed?
import time
from sudoku_tools import *
P="52...6.........7.13...........4..8..6......5...........418.........3..2...87....."
puz=parse(P)
clues=[i for i,d in enumerate(puz) if d]
print("clues:",len(clues))
t=time.time(); n,sol=count_solutions(puz,2); print("solutions:",n,"in %.2fs"%(time.time()-t))
print("solution grid:",show(sol), "valid:",is_valid_grid(sol))
crit=0
for i in clues:
    q=list(puz); q[i]=0
    k,_=count_solutions(q,2)
    r,c=divmod(i,9)
    print("remove clue at row %d col %d (digit %d): %d solution(s)"%(r+1,c+1,puz[i],k))
    if k>=2: crit+=1
print("clues that cannot be removed:",crit,"of",len(clues))
