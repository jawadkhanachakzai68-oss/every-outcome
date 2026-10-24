"""Exact dice + board counting for Catan (Video 8). Pure arithmetic, no simulation except the sampled-boards block."""
from math import factorial as f, comb
from fractions import Fraction
import random, itertools, statistics
# --- dice
ways = {s: 6 - abs(s - 7) for s in range(2, 13)}
print("ways to roll each sum:", ways, "total", sum(ways.values()))
pips = {s: ways[s] for s in ways}
print("pips (= ways out of 36):", pips)
print("P(7) =", Fraction(6,36), "=", 6/36)
# token multiset
tokens = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
print("tokens", len(tokens), "total pips on 18 hexes:", sum(ways[t] for t in tokens))
# P(a hex with number n produces nothing in k rolls)
for n in (6, 8, 5, 9, 2, 12):
    p = Fraction(ways[n], 36)
    for k in (5, 10, 20):
        print(f"hex {n}: P(no production in {k} rolls) = {float((1-p)**k):.4f}")
# expected rolls until a '6' hex pays once: 36/5 ; P(6 hex silent for 20 rolls)
print("6/8 hex expected wait:", 36/5, "rolls")
# P(at least one 6-or-8 roll in 1 turn) = 10/36
# --- board counts
tiles = f(19)//(f(4)*f(4)*f(4)*f(3)*f(3)*f(1))
print("resource+desert arrangements 19!/(4!4!4!3!3!1!) =", tiles)
nums_random = f(18)//(2**8)
print("number token arrangements on 18 land hexes (random) 18!/2^8 =", nums_random)
print("total boards if tokens random:", tiles*nums_random)
print("harbours: 9!/(4!) =", f(9)//f(4), "(4 generic identical, 5 distinct specials)")
print("official spiral: tokens fixed by order -> boards =", tiles, "(x desert position already inside tiles); x harbours =", tiles*(f(9)//f(4)))
# --- sampled boards: how good can one opening get?
from catanatron.models.map import CatanMap, BASE_MAP_TEMPLATE, number_probability
from catanatron.models.board import STATIC_GRAPH
def node_pips(cm):
    return {n: round(sum(number_probability(t.number) for t in cm.adjacent_tiles[n] if t.number)*36) for n in cm.land_nodes}
def best_pair(npips, cm):
    nodes = sorted(npips, key=lambda n: -npips[n])
    best = 0
    for i, a in enumerate(nodes):
        if npips[a]*2 <= best: break
        for b in nodes[i+1:]:
            if npips[a]+npips[b] <= best: break
            if b in STATIC_GRAPH[a]: continue
            # distance rule: no two settlements adjacent (distance >=2)
            best = max(best, npips[a]+npips[b]); break
    return best
for mode in ("official_spiral", "random"):
    rng = random.Random(8)
    mx, bp, adj68 = [], [], 0
    N = 5000
    for _ in range(N):
        cm = CatanMap.from_template(BASE_MAP_TEMPLATE, mode, rng=rng)
        np_ = node_pips(cm)
        mx.append(max(np_.values())); bp.append(best_pair(np_, cm))
        # are any 6/8 hexes adjacent?
        hot = [t for t in cm.land_tiles.values() if t.number in (6, 8)]
        found = False
        for a, b in itertools.combinations(hot, 2):
            if set(a.nodes.values()) & set(b.nodes.values()) and len(set(a.nodes.values()) & set(b.nodes.values())) >= 2:
                found = True
        adj68 += found
    print(mode, f"N={N}: best single node pips avg {statistics.mean(mx):.2f} max {max(mx)} min {min(mx)}; best legal pair total avg {statistics.mean(bp):.2f} min {min(bp)} max {max(bp)}; boards with adjacent 6/8 hexes: {adj68/N:.3%}")
