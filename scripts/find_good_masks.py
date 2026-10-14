import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words from top_common_clean.txt
words_by_len = {}
freq_map = {}

with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        freq = int(freq)
        l = len(clean)
        if l not in words_by_len:
            words_by_len[l] = []
        words_by_len[l].append(clean)
        freq_map[clean] = freq

print("Loaded common words.")

# Function to get slots for any grid mask
def get_slots(grid_mask, rows, cols):
    across_slots = []
    down_slots = []
    for r in range(rows):
        c = 0
        while c < cols:
            if grid_mask[r][c] == 'L':
                c_start = c
                while c < cols and grid_mask[r][c] == 'L':
                    c += 1
                c_end = c - 1
                length = c_end - c_start + 1
                if length < 2: return None, None
                clue_c = c_start - 1
                if clue_c < 0 or grid_mask[r][clue_c] != 'C': return None, None
                across_slots.append({'dir': 'right', 'row': r, 'col': c_start, 'len': length, 'coords': [(r, cc) for cc in range(c_start, c_end + 1)], 'clue': (r, clue_c)})
            else:
                c += 1

    for c in range(cols):
        r = 0
        while r < rows:
            if grid_mask[r][c] == 'L':
                r_start = r
                while r < rows and grid_mask[r][c] == 'L':
                    r += 1
                r_end = r - 1
                length = r_end - r_start + 1
                if length < 2: return None, None
                clue_r = r_start - 1
                if clue_r < 0 or grid_mask[clue_r][c] != 'C': return None, None
                down_slots.append({'dir': 'down', 'row': r_start, 'col': c, 'len': length, 'coords': [(rr, c) for rr in range(r_start, r_end + 1)], 'clue': (clue_r, c)})
            else:
                r += 1

    return across_slots, down_slots

# Let's test different 8x7 and 9x7 clue masks with 4-6 clues
# In 8x7 (rows 0..7, cols 0..6):
# What clue placements give words of length 3..6?
def test_mask(R, C, clues):
    m = [['L'] * C for _ in range(R)]
    m[0][0] = 'E'
    for c in range(1, C): m[0][c] = 'C'
    for r in range(1, R): m[r][0] = 'C'
    for r, c in clues: m[r][c] = 'C'
    ac, dw = get_slots(m, R, C)
    if ac and dw:
        return ac + dw
    return None

# Let's search candidates
cand_masks = [
    # 8x7 patterns
    (8, 7, [(2, 2), (3, 4), (5, 3), (6, 5)]),
    (8, 7, [(2, 3), (3, 5), (5, 2), (6, 4)]),
    (8, 7, [(2, 4), (4, 2), (5, 4), (6, 3)]),
    (8, 7, [(2, 3), (4, 4), (5, 2), (6, 4)]),
    (8, 7, [(3, 2), (4, 4), (6, 3)]),
    (8, 7, [(2, 4), (4, 3), (6, 4)]),
    (8, 7, [(3, 3), (4, 4), (6, 3)]),
    (8, 7, [(2, 3), (4, 3), (5, 4)]),
    (8, 7, [(3, 3), (5, 4), (6, 3)]),
    (8, 7, [(2, 4), (4, 4), (6, 3)]),
    # 9x7 patterns
    (9, 7, [(2, 3), (4, 4), (6, 3), (7, 5)]),
    (9, 7, [(3, 3), (4, 4), (6, 3), (7, 4)]),
    (9, 7, [(3, 3), (4, 4), (6, 4), (7, 3)]),
    (9, 7, [(2, 4), (4, 3), (6, 4), (7, 3)]),
    (9, 7, [(3, 4), (4, 3), (6, 3), (7, 4)]),
    (9, 7, [(3, 3), (5, 4), (7, 3)]),
    (9, 7, [(3, 4), (5, 3), (7, 4)]),
    (9, 7, [(4, 3), (5, 4), (7, 3)]),
    (9, 7, [(3, 3), (4, 4), (6, 3), (7, 4), (8, 3)]),
    (9, 7, [(2, 2), (4, 4), (6, 3), (7, 5)]),
]

valid_candidates = []
for R, C, clues in cand_masks:
    slots = test_mask(R, C, clues)
    if slots:
        lens = [s['len'] for s in slots]
        valid_candidates.append((R, C, clues, slots, lens))
        print(f"Mask {R}x{C} with clues {clues}: {len(slots)} slots, lengths {sorted(lens)}")

print(f"\nTotal valid masks: {len(valid_candidates)}")
