import itertools
from sudoku_tools import *
from unavoidable import *
G=parse("527316489896542731314987562172453896689271354453698217941825673765134928238769145")
U=find_uas(G,12)
# test 1: rectangles by brute force (cells r1c1 r1c2 r2c1 r2c2 holding a b / b a, spread over exactly 2 boxes)
rect=set()
for r1,r2 in itertools.combinations(range(9),2):
    for c1,c2 in itertools.combinations(range(9),2):
        a,b,c,d=G[r1*9+c1],G[r1*9+c2],G[r2*9+c1],G[r2*9+c2]
        if a==d and b==c:
            cells=frozenset([r1*9+c1,r1*9+c2,r2*9+c1,r2*9+c2])
            boxes={(r//3,cc//3) for r in (r1,r2) for cc in (c1,c2)}
            if len(boxes)==2: rect.add(cells)
mine4={s for s in U if len(s)==4}
print("size-4 sets: brute force",len(rect),"search",len(mine4),"same:",rect==mine4)
# test 2: run the search on the grid turned upside down, so it takes a different path
rot=[G[80-i] for i in range(81)]
U2=find_uas(rot,12)
back={frozenset(80-i for i in s) for s in U2}
print("upside-down search gives",len(back),"sets; same family:",back==set(U))
