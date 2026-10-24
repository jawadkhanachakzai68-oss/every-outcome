"""Analysis of out/*.jsonl -> prints the numbers used in the Video 8 script."""
import json, glob, math, collections, statistics, sys
def load(mode):
    rows = []
    for p in sorted(glob.glob(f"out/{mode}_worker*.jsonl")):
        for l in open(p):
            try: rows.append(json.loads(l))
            except Exception: pass
    return rows
def wilson(k, n, z=1.96):
    if n == 0: return (0, 0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (c-h, c+h)
def pct(x): return f"{100*x:.1f}%"
def seat():
    R = load("seat"); n = len(R)
    fin = [r for r in R if r["winner_seat"] is not None]
    print(f"SEAT: {n} games, finished {len(fin)} ({pct(len(fin)/max(n,1))}); avg turns {statistics.mean(r['turns'] for r in fin):.1f}, median {statistics.median(r['turns'] for r in fin)}")
    c = collections.Counter(r["winner_seat"] for r in fin)
    for s in range(4):
        lo, hi = wilson(c[s], len(fin))
        print(f"  seat {s+1}: {c[s]} wins = {pct(c[s]/len(fin))}  (95% CI {pct(lo)} to {pct(hi)})")
    # opening strength
    tot = collections.Counter(); win = collections.Counter()
    top_win = 0; top_n = 0; low_win = 0; low_n = 0
    spread = []
    for r in fin:
        pp = [o["pips"] for o in r["opening"]]
        spread.append(max(pp) - min(pp))
        mx, mn = max(pp), min(pp)
        if pp.count(mx) == 1:
            top_n += 1; top_win += (pp.index(mx) == r["winner_seat"])
        if pp.count(mn) == 1:
            low_n += 1; low_win += (pp.index(mn) == r["winner_seat"])
    print(f"  opening pips gap (best seat minus worst seat): mean {statistics.mean(spread):.2f}, max {max(spread)}")
    print(f"  sole-best opening wins: {top_win}/{top_n} = {pct(top_win/top_n)} ; sole-worst opening wins: {low_win}/{low_n} = {pct(low_win/low_n)}")
    # by pips value
    byp = collections.defaultdict(lambda: [0,0])
    for r in fin:
        for i,o in enumerate(r["opening"]):
            byp[o["pips"]][0] += 1; byp[o["pips"]][1] += (i == r["winner_seat"])
    print("  win rate by opening pips (n>=300):", {k: (v[0], pct(v[1]/v[0])) for k,v in sorted(byp.items()) if v[0] >= 300})
    byk = collections.defaultdict(lambda: [0,0])
    for r in fin:
        for i,o in enumerate(r["opening"]):
            byk[o["kinds"]][0] += 1; byk[o["kinds"]][1] += (i == r["winner_seat"])
    print("  win rate by distinct resources in opening:", {k: (v[0], pct(v[1]/v[0])) for k,v in sorted(byk.items())})
def rules():
    R = load("rules")
    by = collections.defaultdict(list)
    for r in R: by[r["rule"]].append(r)
    print("RULES: challenger (one seat, random seat) vs three default bots")
    for rule, rs in by.items():
        fin = [r for r in rs if r["winner_seat"] is not None]
        k = sum(r["winner_seat"] == r["challenger_seat"] for r in fin)
        lo, hi = wilson(k, len(fin))
        print(f"  {rule:9s}: {k}/{len(fin)} = {pct(k/len(fin))}  (95% CI {pct(lo)} to {pct(hi)}); avg opening pips {statistics.mean(r['opening'][r['challenger_seat']]['pips'] for r in fin):.1f}")
def dice():
    R = load("dice")
    by = collections.defaultdict(list)
    for r in R: by[r["board"]].append(r)
    tops = []; spreads = []; ngames = []
    for b, rs in by.items():
        fin = [r for r in rs if r["winner_seat"] is not None]
        if len(fin) < 30: continue
        c = collections.Counter(r["winner_seat"] for r in fin)
        tops.append(max(c.values())/len(fin))
        ngames.append(len(fin))
        pp = [o["pips"] for o in fin[0]["opening"]]
        spreads.append(max(pp)-min(pp))
    print(f"DICE: {len(tops)} boards x ~{statistics.mean(ngames):.0f} dice seeds; same board, same seating, same (deterministic) openings")
    print(f"  most-successful seat wins on average {pct(statistics.mean(tops))} of games on a board (pure luck-free equal would be 25%)")
    print(f"  boards where one seat wins >50%: {sum(t>0.5 for t in tops)}/{len(tops)} ; >40%: {sum(t>0.4 for t in tops)}")
    # how many different seats win at least once per board
    kinds = [len(set(r['winner_seat'] for r in rs if r['winner_seat'] is not None)) for rs in by.values()]
    print(f"  distinct winners per board (of 4 seats): mean {statistics.mean(kinds):.2f}; boards where all 4 seats win at least once: {sum(k==4 for k in kinds)}/{len(kinds)}")
    # null expectation: top-seat share if each game were a fair 25% coin flip with n=40
    import random
    rnd = random.Random(1); sim = []
    for _ in range(20000):
        n = 40; c = collections.Counter(rnd.randrange(4) for _ in range(n)); sim.append(max(c.values())/n)
    print(f"  null (fair 4-way coin, 40 games): top-seat share averages {pct(statistics.mean(sim))}")

def extras():
    """Numbers used in the script that need more than the basic tables."""
    import random as _r
    R = load("rules"); S = load("seat"); D = load("dice")
    print("EXTRAS")
    # opening resource kinds per rule (challenger)
    for rule in ["pips", "orewheat", "diverse", "random", "worst"]:
        rs = [r for r in R if r["rule"] == rule]
        kinds = collections.Counter(r["opening"][r["challenger_seat"]]["kinds"] for r in rs)
        print(f"  rule {rule}: opening kinds {dict(sorted(kinds.items()))}")
        for k in sorted(kinds):
            sub = [r for r in rs if r["opening"][r["challenger_seat"]]["kinds"] == k]
            w = sum(r["winner_seat"] == r["challenger_seat"] for r in sub)
            print(f"     {k} kinds: {len(sub)} games, challenger wins {pct(w/len(sub))}")
    kc = collections.Counter(o["kinds"] for r in S for o in r["opening"]); n = sum(kc.values())
    print("  default bots opening kinds:", {k: pct(v/n) for k, v in sorted(kc.items())},
          "avg pips", round(statistics.mean(o["pips"] for r in S for o in r["opening"]), 2))
    print("  other bots avg pips in 'pips' challenger games:",
          round(statistics.mean(o["pips"] for r in R if r["rule"] == "pips" for i, o in enumerate(r["opening"]) if i != r["challenger_seat"]), 2))
    # dice: honest favourite estimate (split half: pick on 20 seeds, measure on other 20)
    by = collections.defaultdict(list)
    for r in D: by[r["board"]].append(r)
    for b in by: by[b].sort(key=lambda r: int(r["key"].split("-")[2]))
    est = []
    for b, rs in by.items():
        for A, B in ((rs[:20], rs[20:]), (rs[20:], rs[:20])):
            c = collections.Counter(r["winner_seat"] for r in A)
            top = max(c.values()); favs = [s for s in range(4) if c[s] == top]
            cb = collections.Counter(r["winner_seat"] for r in B)
            est.append(statistics.mean(cb[s] for s in favs) / len(B))
    print(f"  dice-only: favourite chosen on 20 dice seeds wins {pct(statistics.mean(est))} of the other 20 (fair would be 25%)")
    share = []
    for b, rs in by.items():
        o = rs[0]["opening"]; c = collections.Counter(r["winner_seat"] for r in rs)
        for s in range(4): share.append((o[s]["kinds"], o[s]["pips"], c[s]/len(rs)))
    def corr(a, b):
        ma, mb = statistics.mean(a), statistics.mean(b)
        return sum((x-ma)*(y-mb) for x, y in zip(a, b)) / math.sqrt(sum((x-ma)**2 for x in a) * sum((y-mb)**2 for y in b))
    print(f"  dice-only: correlation of seat win share with opening pips {corr([x[1] for x in share],[x[2] for x in share]):.3f}, with resource kinds {corr([x[0] for x in share],[x[2] for x in share]):.3f}")
    for k in (4, 5):
        v = [x[2] for x in share if x[0] == k]
        print(f"  dice-only: seats with {k} resource kinds win {pct(statistics.mean(v))} on average ({len(v)} seats)")
    ok = tot = 0
    for b, rs in by.items():
        pp = [x["pips"] for x in rs[0]["opening"]]; c = collections.Counter(r["winner_seat"] for r in rs)
        if pp.count(max(pp)) == 1:
            tot += 1; ok += (c.most_common(1)[0][0] == pp.index(max(pp)))
    print(f"  dice-only: the seat with the single most opening pips is the board's favourite on {ok} of {tot} boards")


if __name__ == "__main__":
    for m in sys.argv[1:] or ["seat","rules","dice","extras"]:
        {"seat":seat,"rules":rules,"dice":dice,"extras":extras}[m]()
