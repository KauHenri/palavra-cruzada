import itertools

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
                across_slots.append({'id': f'A_{r}_{c_start}', 'dir': 'right', 'row': r, 'col': c_start, 'len': length, 'coords': [(r, cc) for cc in range(c_start, c_end + 1)], 'clue': (r, clue_c)})
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
                down_slots.append({'id': f'D_{r_start}_{c}', 'dir': 'down', 'row': r_start, 'col': c, 'len': length, 'coords': [(rr, c) for rr in range(r_start, r_end + 1)], 'clue': (clue_r, c)})
            else:
                r += 1

    return across_slots + down_slots

def make_base(R, C):
    m = [['L'] * C for _ in range(R)]
    m[0][0] = 'E'
    for c in range(1, C): m[0][c] = 'C'
    for r in range(1, R): m[r][0] = 'C'
    return m

rows, cols = 8, 7
interior_cells = [(r, c) for r in range(2, rows - 1) for c in range(2, cols - 1)]

print(f"Finding best masks for 8x7...")
good_masks_8x7 = []
for num_clues in [2, 3, 4]:
    for cand in itertools.combinations(interior_cells, num_clues):
        m = make_base(rows, cols)
        for r, c in cand: m[r][c] = 'C'
        slots = get_slots(m, rows, cols)
        if slots:
            lens = [s['len'] for s in slots]
            if min(lens) >= 2:
                # Count how many slots are >= 3
                c_ge3 = sum(1 for l in lens if l >= 3)
                good_masks_8x7.append((cand, len(slots), c_ge3, lens))

# Sort by most >=3 words
good_masks_8x7.sort(key=lambda x: (x[2], x[1]), reverse=True)
print("Top 5 masks for 8x7:")
for cand, total, ge3, lens in good_masks_8x7[:5]:
    print(f"  Clues {cand}: {total} slots total, {ge3} of them len>=3. Distribution: {sorted(lens)}")

rows, cols = 9, 7
interior_cells = [(r, c) for r in range(2, rows - 1) for c in range(2, cols - 1)]
good_masks_9x7 = []
for num_clues in [2, 3, 4]:
    for cand in itertools.combinations(interior_cells, num_clues):
        m = make_base(rows, cols)
        for r, c in cand: m[r][c] = 'C'
        slots = get_slots(m, rows, cols)
        if slots:
            lens = [s['len'] for s in slots]
            if min(lens) >= 2:
                c_ge3 = sum(1 for l in lens if l >= 3)
                good_masks_9x7.append((cand, len(slots), c_ge3, lens))

good_masks_9x7.sort(key=lambda x: (x[2], x[1]), reverse=True)
print("\nTop 5 masks for 9x7:")
for cand, total, ge3, lens in good_masks_9x7[:5]:
    print(f"  Clues {cand}: {total} slots total, {ge3} of them len>=3. Distribution: {sorted(lens)}")
