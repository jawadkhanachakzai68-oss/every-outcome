EVERY OUTCOME - VIDEO 10 - SUDOKU, THE 17-CLUE MINIMUM - CODE
Everything here is my own code. Needs Python 3 and gcc. Run in this folder.

1. Count every Sudoku grid
   gcc -O3 -o bandclasses bandclasses.c && ./bandclasses > band_classes.txt      (2,612,736 top bands -> 416 classes)
   gcc -O3 -o gridcount gridcount.c
   ./gridcount band_classes.txt 2 0 > gc0.txt & ./gridcount band_classes.txt 2 1 > gc1.txt     (about 20 minutes on two cores)
   python3 combine_gridcount.py
2. A real 17-clue puzzle: python3 check_17.py                      (1 solution; 17 of 17 clues needed)
3. Swap groups ("unavoidable sets") of its grid: python3 unavoidable.py ; python3 check_ua.py
   (ua_masks.txt and ua_masks_14.txt are the groups, as 81-bit masks, for the C programs)
4. Fewest cells that touch every group, and the counts: ./run_hitting_counts.sh   (gcc -O2 -o hs hs.c; gcc -O2 -o hscount hscount.c)
   List the 16-cell choices: gcc -O2 -o hslist hslist.c && ./hslist ua_masks.txt 16 > groups16.txt   (8,259 lines)
   Test them with the solver: see test_groups.py
5. The 4x4 version: python3 toy4x4.py
6. Human-style solver: python3 human_solver.py ; python3 human_stats.py 150 ; python3 private_groups.py (why each clue is needed)
7. Big-number arithmetic: python3 facts.py
Not included: the full proof (about 800 processor-years) by McGuire, Tugemann and Civario.
