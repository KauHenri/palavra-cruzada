import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
print("Loading words...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

clean_words = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha():
        continue
    l = len(clean)
    if 2 <= l <= 8:
        if l not in clean_words:
            clean_words[l] = set()
        clean_words[l].add(clean)

print(f"Words loaded: {sum(len(v) for v in clean_words.values())}")

def solve_grid(grid_mask, rows, cols):
    across_slots = []
    down_slots = []

    # Check across
    for r in range(rows):
        c = 0
        while c < cols:
            if grid_mask[r][c] == 'L':
                c_start = c
                while c < cols and grid_mask[r][c] == 'L':
                    c += 1
                c_end = c - 1
                length = c_end - c_start + 1
                if length < 2:
                    return None # No 1-letter words
                clue_c = c_start - 1
                if clue_c < 0 or grid_mask[r][clue_c] != 'C':
                    return None # Missing clue
                across_slots.append({
                    'id': f'A_{r}_{c_start}',
                    'dir': 'right',
                    'row': r,
                    'col': c_start,
                    'length': length,
                    'coords': [(r, cc) for cc in range(c_start, c_end + 1)],
                    'clue': (r, clue_c)
                })
            else:
                c += 1

    # Check down
    for c in range(cols):
        r = 0
        while r < rows:
            if grid_mask[r][c] == 'L':
                r_start = r
                while r < rows and grid_mask[r][c] == 'L':
                    r += 1
                r_end = r - 1
                length = r_end - r_start + 1
                if length < 2:
                    return None # No 1-letter words
                clue_r = r_start - 1
                if clue_r < 0 or grid_mask[clue_r][c] != 'C':
                    return None # Missing clue
                down_slots.append({
                    'id': f'D_{r_start}_{c}',
                    'dir': 'down',
                    'row': r_start,
                    'col': c,
                    'length': length,
                    'coords': [(rr, c) for rr in range(r_start, r_end + 1)],
                    'clue': (clue_r, c)
                })
            else:
                r += 1

    all_slots = across_slots + down_slots
    return all_slots

def make_base(R, C):
    m = [['L'] * C for _ in range(R)]
    m[0][0] = 'E'
    for c in range(1, C):
        m[0][c] = 'C'
    for r in range(1, R):
        m[r][0] = 'C'
    return m

rows, cols = 8, 7
print(f"Searching valid mask configurations for {rows}x{cols}...")

valid_masks = []
candidates = [
    [(2, 2), (4, 4), (6, 3)],
    [(2, 3), (4, 5), (5, 2)],
    [(2, 4), (4, 2), (6, 4)],
    [(3, 2), (4, 4), (5, 3)],
    [(2, 3), (4, 3), (6, 4)],
    [(2, 2), (4, 3), (6, 4)],
    [(2, 4), (4, 3), (6, 2)],
    [(3, 3), (5, 4)],
    [(2, 3), (5, 3)],
    [(2, 4), (5, 3)],
    [(3, 2), (5, 4)],
    [(3, 4), (5, 2)],
    [(2, 2), (3, 4), (5, 3), (6, 5)],
    [(2, 3), (3, 5), (5, 2), (6, 4)],
]

for cand in candidates:
    m = make_base(rows, cols)
    for r, c in cand:
        m[r][c] = 'C'
    slots = solve_grid(m, rows, cols)
    if slots:
        print(f"Found valid layout with {len(cand)} internal clues: {cand}")
        print(f"  Slots count: {len(slots)}")
        lens = [s['length'] for s in slots]
        print(f"  Lengths: min={min(lens)} max={max(lens)} avg={sum(lens)/len(lens):.1f}")
        valid_masks.append((cand, m, slots))

print(f"Total valid layouts found: {len(valid_masks)}")
