# Small Sudoku toolkit used for every V10 number: solver, solution counter, units.
import itertools
ROWS=[[r*9+c for c in range(9)] for r in range(9)]
COLS=[[r*9+c for r in range(9)] for c in range(9)]
BOXES=[[ (br*3+r)*9+bc*3+c for r in range(3) for c in range(3)] for br in range(3) for bc in range(3)]
UNITS=ROWS+COLS+BOXES
PEERS=[set() for _ in range(81)]
CELL_UNITS=[[] for _ in range(81)]
for u in UNITS:
    for c in u:
        CELL_UNITS[c].append(u)
        PEERS[c].update(u)
for c in range(81): PEERS[c].discard(c)
PEERS=[sorted(p) for p in PEERS]

def parse(s):
    s=s.strip().replace('.','0')
    return [int(ch) for ch in s]
def show(g):
    return ''.join(str(d) if d else '.' for d in g)

def count_solutions(puz, limit=2):
    """number of solutions of puz (list of 81 ints, 0 = blank), stopping at `limit`"""
    g=list(puz)
    rows=[0]*9; cols=[0]*9; boxes=[0]*9
    for i,d in enumerate(g):
        if d:
            b=1<<d
            r,c=divmod(i,9); bx=(r//3)*3+c//3
            if rows[r]&b or cols[c]&b or boxes[bx]&b: return 0
            rows[r]|=b; cols[c]|=b; boxes[bx]|=b
    found=[0]; sol=[None]
    def rec():
        # most constrained empty cell
        best=-1; bm=0; bn=10
        for i in range(81):
            if g[i]==0:
                r,c=divmod(i,9); bx=(r//3)*3+c//3
                m=0x3FE&~(rows[r]|cols[c]|boxes[bx])
                n=bin(m).count('1')
                if n<bn:
                    best,bm,bn=i,m,n
                    if n<=1: break
        if best<0:
            found[0]+=1
            if sol[0] is None: sol[0]=list(g)
            return found[0]>=limit
        if bn==0: return False
        r,c=divmod(best,9); bx=(r//3)*3+c//3
        m=bm
        while m:
            b=m&-m; m^=b; d=b.bit_length()-1
            g[best]=d; rows[r]|=b; cols[c]|=b; boxes[bx]|=b
            stop=rec()
            g[best]=0; rows[r]^=b; cols[c]^=b; boxes[bx]^=b
            if stop: return True
        return False
    rec()
    return found[0], sol[0]

def is_valid_grid(g):
    for u in UNITS:
        if sorted(g[i] for i in u)!=list(range(1,10)): return False
    return True
