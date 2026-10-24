#!/bin/bash
# usage: ./runall.sh WORKER_NUMBER   (runs the three experiments for one worker)
# needs: pip install catanatron==3.3.0
for m in seat rules dice; do python exp.py $m $1 2 >> log_$1.txt 2>&1; done
