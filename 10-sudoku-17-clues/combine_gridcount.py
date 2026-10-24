# Adds the two halves printed by gridcount (even and odd classes) and multiplies by 9! (renaming digits).
import re
parts=[int(re.search(r'= (\d+)',open(f).read().split('\n')[1]).group(1)) for f in ('gc0.txt','gc1.txt')]
total=sum(parts)*362880
print("part sums:",parts)
print("total Sudoku grids =",f"{total:,}")
print("equals the published 6,670,903,752,021,072,936,960:",total==6670903752021072936960)
