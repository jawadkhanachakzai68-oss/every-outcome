"""Counts what the standard bots actually do in a game (limits section)."""
import collections
from catanatron import Game, Color
from catanatron.players.value import ValueFunctionPlayer
tot = collections.Counter(); N = 100
for s in range(N):
    g = Game([ValueFunctionPlayer(c) for c in (Color.RED, Color.BLUE, Color.ORANGE, Color.WHITE)], seed=s)
    while g.winning_color() is None:
        tot[g.play_tick().action.action_type.name] += 1
print(f"{N} games of four standard bots, average actions per game:")
for k, v in sorted(tot.items()): print(f"  {k:22s} {v/N:7.2f}")
