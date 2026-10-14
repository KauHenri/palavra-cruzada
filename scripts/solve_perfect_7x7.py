# Script to find complete valid Swedish crossword grids
from solve_grid import DICT

# Let's test a clean 7x7:
# Col 1: B-R-A-S-I-L (6 letters, r1..r6: BRASIL)
# Col 6: P-O-R-T-O-S (6 letters, r1..r6: PORTOS)
# Row 1: B-O-L-O-S-P?
# Let's write a solver that finds words for a 7x7 grid:
# Grid: 7 rows (0..6), 7 cols (0..6)
# r=0 is clue, c=0 is clue.
# letter area is r: 1..6, c: 1..6 (6x6 letter area with some clue cells inside).

# Let's find 6-letter across words for row 1, row 3, row 5
# and 6-letter down words for col 1, col 3, col 5
words_6 = [w for w in DICT if len(w) == 6]
words_5 = [w for w in DICT if len(w) == 5]
words_4 = [w for w in DICT if len(w) == 4]
words_3 = [w for w in DICT if len(w) == 3]
words_2 = [w for w in DICT if len(w) == 2]

print(f"Words 6: {len(words_6)}, 5: {len(words_5)}, 4: {len(words_4)}, 3: {len(words_3)}, 2: {len(words_2)}")
