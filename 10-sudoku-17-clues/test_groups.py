# Gives every listed clue choice to the solver and counts how many leave exactly one solution.
from sudoku_tools import *
G=parse("527316489896542731314987562172453896689271354453698217941825673765134928238769145")
for fn in ('groups15.txt','groups16.txt'):
    n=0; uniq=0
    for line in open(fn):
        cells=[int(x) for x in line.split()]
        if not cells: continue
        n+=1
        puz=[G[i] if i in cells else 0 for i in range(81)]
        if count_solutions(puz,2)[0]==1: uniq+=1
    print(fn,"choices tested:",n,"with exactly one solution:",uniq)
