# Video 8: Catan opening strategies

Every number in the video is listed in `CLAIMS.txt` with where it came from.

**Needs:** Python 3 and `pip install catanatron==3.3.0` (open-source Catan simulator by Bryan Collazo, GPL-3.0).

| File | What it does |
| --- | --- |
| `exp.py` | Plays the games. Only the way the first two settlements are chosen changes between bots. Usage: `python exp.py MODE WORKER NWORKERS` (MODE = seat, rules or dice) |
| `analyze.py` | Turns the game files into the win rates in the video |
| `math8.py` | The exact dice and board arithmetic |
| `rep_analyze.py` | Re-analysis of the repeat run |
| `actions_count.py` | Counts the actions the simulator allows |
| `results_jsonl.zip`, `results_rep.zip` | The raw game results, one JSON line per game |
| `code_output.txt` | What the code printed |

This is the paper's and the simulator's model, not the real game with real people. Limits are stated in the video.
