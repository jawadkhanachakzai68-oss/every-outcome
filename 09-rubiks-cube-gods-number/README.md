V9 code (Python 3 + numpy, one C++ file)
arith.py      exact arithmetic (group size, H, boxes, years)
geo.py        geometric cube model, box labels (twist, flip, slice)
sym.py        the 16 symmetries and their action on box labels
burnside.py   counts families of boxes = 138,639,780
bfs3.cpp      positions within 7 moves (g++ -O2 bfs3.cpp; ./bfs3 7)
cube2.py      2x2x2 full search, both metrics
cube2sym.py   2x2x2 symmetry families and distance invariance
