import json, glob, math
rows = []
for f in glob.glob('out/rep_worker*.jsonl'):
    rows += [json.loads(l) for l in open(f)]
def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h
for rule in ('pips', 'diverse'):
    R = [r for r in rows if r['rule'] == rule]
    n = len(R); k = sum(1 for r in R if r['winner_seat'] == r['challenger_seat'])
    lo, hi = wilson(k, n)
    dots = sum(r['opening'][r['challenger_seat']]['pips'] for r in R) / n
    allk = sum(1 for r in R if r['opening'][r['challenger_seat']]['kinds'] == 5)
    print(f'{rule}: {k}/{n} = {100*k/n:.1f}%  95% CI {100*lo:.1f}-{100*hi:.1f}  opening dots {dots:.1f}  all-5-resources in {allk} ({100*allk/n:.1f}%)')
