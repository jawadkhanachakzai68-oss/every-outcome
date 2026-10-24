"""Every Outcome - Video 8 (Catan) experiments.
Uses the open-source Catanatron simulator (v3.3.0, GPL-3.0). All bots are the
simulator's own ValueFunctionPlayer; the only thing we change is HOW the first
two settlements are chosen. Everything after the opening is identical code.

Usage:  python exp.py MODE WORKER NWORKERS
MODE: seat | rules | dice
Output: out/MODE_workerW.jsonl  (one json line per game, resumable)
"""
import sys, os, json, random, time
from catanatron import Game, Color
from catanatron.models.actions import ActionType, generate_playable_actions
from catanatron.models.map import CatanMap, BASE_MAP_TEMPLATE, number_probability
from catanatron.players.value import ValueFunctionPlayer

COLORS = (Color.RED, Color.BLUE, Color.ORANGE, Color.WHITE)
RULES = ["default", "pips", "diverse", "orewheat", "random", "worst"]

def pips(cmap, node):
    return round(sum(number_probability(t.number) for t in cmap.adjacent_tiles[node] if t.number) * 36)

def node_res_pips(cmap, node):
    d = {}
    for t in cmap.adjacent_tiles[node]:
        if t.number and t.resource:
            d[t.resource] = d.get(t.resource, 0) + round(number_probability(t.number) * 36)
    return d

class OpeningPlayer(ValueFunctionPlayer):
    """ValueFunctionPlayer, but the two opening settlements follow `rule`."""
    def __init__(self, color, rule="default", seed=0):
        super().__init__(color)
        self.rule = rule
        self.rng = random.Random(seed)

    def decide(self, game, playable_actions):
        if (self.rule != "default" and game.state.is_initial_build_phase
                and playable_actions[0].action_type == ActionType.BUILD_SETTLEMENT):
            cmap = game.state.board.map
            mine = self._owned_res(game)
            best, best_s = None, None
            cands = list(playable_actions)
            if self.rule == "random":
                return self.rng.choice(cands)
            for a in cands:
                n = a.value
                rp = node_res_pips(cmap, n)
                p = sum(rp.values())
                if self.rule == "pips":
                    s = p
                elif self.rule == "worst":
                    s = -p
                elif self.rule == "diverse":
                    s = 100 * len(set(rp) - mine) + p
                elif self.rule == "orewheat":
                    s = p + rp.get("ORE", 0) + rp.get("WHEAT", 0)
                else:
                    raise ValueError(self.rule)
                if best_s is None or s > best_s or (s == best_s and n < best.value):
                    best, best_s = a, s
            return best
        return super().decide(game, playable_actions)

    def _owned_res(self, game):
        cmap = game.state.board.map
        out = set()
        for n in game.state.buildings_by_color[self.color].get("SETTLEMENT", []):
            out |= set(node_res_pips(cmap, n))
        return out

def opening_stats(game):
    cmap = game.state.board.map
    res = []
    for c in game.state.colors:
        nodes = game.state.buildings_by_color[c].get("SETTLEMENT", [])
        rs = {}
        for n in nodes:
            for r, v in node_res_pips(cmap, n).items():
                rs[r] = rs.get(r, 0) + v
        res.append({"pips": sum(rs.values()), "kinds": len(rs), "nodes": list(nodes)})
    return res

def play(game):
    # run opening, snapshot, then rest of game
    while game.state.is_initial_build_phase:
        game.play_tick()
    op = opening_stats(game)
    while game.winning_color() is None and game.state.num_turns < 1000:
        game.play_tick()
    w = game.winning_color()
    st = game.state
    vps = [st.player_state[f"P{i}_ACTUAL_VICTORY_POINTS"] for i in range(4)]
    return {"winner_seat": (st.colors.index(w) if w else None), "turns": st.num_turns,
            "vps": vps, "opening": op}

def main():
    mode, w, nw = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    nmax = int(os.environ.get("N", "0"))
    os.makedirs("out", exist_ok=True)
    path = f"out/{mode}_worker{w}.jsonl"
    done = set()
    if os.path.exists(path):
        for line in open(path):
            try: done.add(json.loads(line)["key"])
            except Exception: pass
    jobs = []
    if mode == "seat":
        N = nmax or 10000
        jobs = [(f"seat-{s}", s, None) for s in range(N)]
    elif mode == "rules":
        N = nmax or 1500
        jobs = [(f"rules-{r}-{s}", s, r) for s in range(N) for r in RULES[1:]]
    elif mode == "rep":   # replication with fresh seeds, two key rules only
        N = nmax or 2000
        jobs = [(f"rep-{r}-{s}", 50000 + s, r) for s in range(N) for r in ("pips", "diverse")]
    elif mode == "dice":
        B = nmax or 150
        D = 40
        jobs = [(f"dice-{b}-{d}", (b, d), None) for b in range(B) for d in range(D)]
    jobs = jobs[w::nw]
    f = open(path, "a")
    t0 = time.time(); n = 0
    for key, s, rule in jobs:
        if key in done: continue
        if mode == "dice":
            b, d = s
            cmap = CatanMap.from_template(BASE_MAP_TEMPLATE, "official_spiral", rng=random.Random(9000 + b))
            ps = [OpeningPlayer(c, "default", 0) for c in COLORS]
            g = Game(ps, seed=100000 + d, catan_map=cmap)
            # fixed seating: RED, BLUE, ORANGE, WHITE
            order = {c: i for i, c in enumerate(COLORS)}
            g.state.players = sorted(g.state.players, key=lambda p: order[p.color])
            g.state.colors = tuple(p.color for p in g.state.players)
            g.state.color_to_index = {c: i for i, c in enumerate(g.state.colors)}
            g.playable_actions = generate_playable_actions(g.state)
            res = play(g)
            res["board"] = b
        else:
            seat_rng = random.Random(s)
            ps = [OpeningPlayer(c, "default", s + i) for i, c in enumerate(COLORS)]
            g = Game(ps, seed=s)
            if rule:
                # challenger = player in a seat chosen by the game's own shuffle (random seat)
                ch = g.state.players[s % 4]
                ch.rule = rule
            res = play(g)
            if rule: res["challenger_seat"] = s % 4; res["rule"] = rule
        res["key"] = key
        f.write(json.dumps(res) + "\n"); f.flush()
        n += 1
        if n % 50 == 0:
            print(w, n, round(time.time() - t0), flush=True)

if __name__ == "__main__":
    main()
