import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Common words filter: we prefer words that are common/popular and easy to define
# Let's load wordlist
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

words_by_len = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha():
        continue
    l = len(clean)
    if l not in words_by_len:
        words_by_len[l] = set()
    words_by_len[l].add(clean)

def get_slots(grid_types, rows, cols):
    across_slots = []
    down_slots = []

    # Find across slots
    for r in range(rows):
        c = 0
        while c < cols:
            if grid_types[r][c] == 'L':
                c_start = c
                while c < cols and grid_types[r][c] == 'L':
                    c += 1
                c_end = c - 1
                length = c_end - c_start + 1
                # Must have clue to the left
                clue_c = c_start - 1
                has_clue = (clue_c >= 0 and grid_types[r][clue_c] == 'C')
                across_slots.append({
                    'dir': 'right',
                    'row': r,
                    'col': c_start,
                    'length': length,
                    'coords': [(r, cc) for cc in range(c_start, c_end + 1)],
                    'clue_cell': (r, clue_c) if has_clue else None
                })
            else:
                c += 1

    # Find down slots
    for c in range(cols):
        r = 0
        while r < rows:
            if grid_types[r][c] == 'L':
                r_start = r
                while r < rows and grid_types[r][c] == 'L':
                    r += 1
                r_end = r - 1
                length = r_end - r_start + 1
                # Must have clue above
                clue_r = r_start - 1
                has_clue = (clue_r >= 0 and grid_types[clue_r][c] == 'C')
                down_slots.append({
                    'dir': 'down',
                    'row': r_start,
                    'col': c,
                    'length': length,
                    'coords': [(rr, c) for rr in range(r_start, r_end + 1)],
                    'clue_cell': (clue_r, c) if has_clue else None
                })
            else:
                r += 1

    return across_slots, down_slots

# Let's test a sample layout
# Grid 8 rows x 7 cols
rows, cols = 8, 7
grid_types = [['E'] * cols for _ in range(rows)]
# Row 0: empty at (0,0), clue at (0, 1..6)
for c in range(1, cols):
    grid_types[0][c] = 'C'
# Col 0: clue at (1..7, 0)
for r in range(1, rows):
    grid_types[r][0] = 'C'

# All letters inside by default
for r in range(1, rows):
    for c in range(1, cols):
        grid_types[r][c] = 'L'

# Place internal clue cells:
# e.g., (2, 3), (4, 5), (5, 2)
grid_types[2][3] = 'C'
grid_types[4][4] = 'C'
grid_types[5][2] = 'C'

across, down = get_slots(grid_types, rows, cols)
print(f"Across slots: {len(across)}, Down slots: {len(down)}")
for s in across:
    print(f"Across: r={s['row']} c={s['col']} len={s['length']} clue={s['clue_cell']}")
for s in down:
    print(f"Down: r={s['row']} c={s['col']} len={s['length']} clue={s['clue_cell']}")
