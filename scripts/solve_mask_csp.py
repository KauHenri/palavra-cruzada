import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
print("Loading words...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

words_by_len = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha():
        continue
    l = len(clean)
    if 2 <= l <= 8:
        if l not in words_by_len:
            words_by_len[l] = set()
        words_by_len[l].add(clean)

# Also let's keep track of common/frequent words so the puzzle is enjoyable, not obscure biology terms
# Let's see: we can test if a candidate mask can be solved with common words.

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
                if length < 2: return None
                clue_c = c_start - 1
                if clue_c < 0 or grid_mask[r][clue_c] != 'C': return None
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

    for c in range(cols):
        r = 0
        while r < rows:
            if grid_mask[r][c] == 'L':
                r_start = r
                while r < rows and grid_mask[r][c] == 'L':
                    r += 1
                r_end = r - 1
                length = r_end - r_start + 1
                if length < 2: return None
                clue_r = r_start - 1
                if clue_r < 0 or grid_mask[clue_r][c] != 'C': return None
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

    return across_slots, down_slots

def solve_csp(slots, rows, cols, max_time=15):
    # Setup cell to slots mapping
    cell_slots = {}
    for s_idx, s in enumerate(slots):
        for pos, (r, c) in enumerate(s['coords']):
            if (r, c) not in cell_slots:
                cell_slots[(r, c)] = []
            cell_slots[(r, c)].append((s_idx, pos))

    # Grid of characters
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned_words = [None] * len(slots)
    used_words = set()

    # Pre-index words by length and letter patterns
    # For speed, word lists per slot
    slot_words = []
    for s in slots:
        l = s['length']
        # Take a subset of words of this length (common words if possible)
        cand_list = list(words_by_len.get(l, []))
        random.shuffle(cand_list)
        slot_words.append(cand_list)

    start_time = time.time()

    def backtrack():
        if time.time() - start_time > max_time:
            return None

        # MRV: pick slot with fewest valid remaining words
        best_s = None
        best_cands = None

        for s_idx in range(len(slots)):
            if assigned_words[s_idx] is not None:
                continue

            s = slots[s_idx]
            pattern = [grid[r][c] for r, c in s['coords']]
            # Check matching words
            valid = []
            for w in slot_words[s_idx]:
                if w in used_words:
                    continue
                match = True
                for i, char in enumerate(pattern):
                    if char != '' and char != w[i]:
                        match = False
                        break
                if match:
                    valid.append(w)
                    if len(valid) > 200: # cap for speed
                        break

            if len(valid) == 0:
                return None # dead end

            if best_cands is None or len(valid) < len(best_cands):
                best_cands = valid
                best_s = s_idx
                if len(best_cands) <= 1:
                    break

        if best_s is None:
            return grid # All slots filled!

        s = slots[best_s]
        coords = s['coords']

        # Try words
        random.shuffle(best_cands)
        for w in best_cands[:30]:
            # Apply word
            old_chars = [grid[r][c] for r, c in coords]
            for i, (r, c) in enumerate(coords):
                grid[r][c] = w[i]
            assigned_words[best_s] = w
            used_words.add(w)

            res = backtrack()
            if res is not None:
                return res

            # Undo
            for i, (r, c) in enumerate(coords):
                grid[r][c] = old_chars[i]
            assigned_words[best_s] = None
            used_words.remove(w)

        return None

    res = backtrack()
    if res:
        return grid, assigned_words
    return None, None

# Test candidate 1: 8x7 with clues at (3, 3) and (5, 4)
rows, cols = 8, 7
m = [['L'] * cols for _ in range(rows)]
m[0][0] = 'E'
for c in range(1, cols): m[0][c] = 'C'
for r in range(1, rows): m[r][0] = 'C'
m[3][3] = 'C'
m[5][4] = 'C'

across, down = get_slots(m, rows, cols)
slots = across + down
print(f"Solving 8x7 grid with {len(slots)} slots...")
sol_grid, sol_words = solve_csp(slots, rows, cols, max_time=10)
if sol_grid:
    print("SOLVED SUCCESSFULLY!")
    for r in range(rows):
        row_str = " ".join(sol_grid[r][c] if m[r][c] == 'L' else ('[]' if m[r][c]=='C' else '..') for c in range(cols))
        print(f"Row {r}: {row_str}")
    for s_idx, s in enumerate(slots):
        print(f"{s['dir'].upper()} ({s['row']},{s['col']}) len={s['length']}: {sol_words[s_idx]}")
else:
    print("Could not solve within time limit.")
