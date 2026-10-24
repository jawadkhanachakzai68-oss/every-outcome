#!/bin/bash
# Fewest cells touching every swap group, then exact counts of the 14-, 15- and 16-cell choices that touch them all.
for k in 14 15 16 17; do ./hs ua_masks.txt $k; done
TIMEFORMAT="  time: %U s of CPU"
for k in 14 15 16; do time ./hscount ua_masks.txt $k; done
