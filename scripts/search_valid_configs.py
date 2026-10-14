import itertools

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
                    return None
                clue_c = c_start - 1
                if clue_c < 0 or grid_mask[r][clue_c] != 'C':
                    return None
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
                    return None
                clue_r = r_start - 1
                if clue_r < 0 or grid_mask[clue_r][c] != 'C':
                    return None
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

    return across_slots + down_slots

def make_base(R, C):
    m = [['L'] * C for _ in range(R)]
    m[0][0] = 'E'
    for c in range(1, C):
        m[0][c] = 'C'
    for r in range(1, R):
        m[r][0] = 'C'
    return m

rows, cols = 8, 7
interior_cells = [(r, c) for r in range(2, rows - 1) for c in range(2, cols - 1)]

print(f"Testing 2 to 4 clues combinations among {len(interior_cells)} interior positions...")
valid_configs = []

for num_clues in [2, 3, 4]:
    for cand in itertools.combinations(interior_cells, num_clues):
        m = make_base(rows, cols)
        for r, c in cand:
            m[r][c] = 'C'
        slots = solve_grid(m, rows, cols)
        if slots:
            lens = [s['length'] for s in slots]
            # Must have no 1-letter words, and ideally min length >= 2 or 3
            if min(lens) >= 2:
                valid_configs.append((cand, len(slots), min(lens), max(lens), sum(lens)/len(lens)))

print(f"Found {len(valid_configs)} valid configurations for 8x7!")
for cand, n_slots, min_l, max_l, avg_l in valid_configs[:15]:
    print(f"  Clues {cand} -> {n_slots} slots, lengths [{min_l}..{max_l}], avg {avg_l:.1f}")

# Also check 9x7
rows, cols = 9, 7
interior_cells = [(r, c) for r in range(2, rows - 1) for c in range(2, cols - 1)]
valid_9x7 = []
for num_clues in [2, 3, 4]:
    for cand in itertools.combinations(interior_cells, num_clues):
        m = make_base(rows, cols)
        for r, c in cand:
            m[r][c] = 'C'
        slots = solve_grid(m, rows, cols)
        if slots:
            lens = [s['length'] for s in slots]
            if min(lens) >= 2:
                valid_9x7.append((cand, len(slots), min(lens), max(lens), sum(lens)/len(lens)))

print(f"Found {len(valid_9x7)} valid configurations for 9x7!")
for cand, n_slots, min_l, max_l, avg_l in valid_9x7[:15]:
    print(f"  Clues {cand} -> {n_slots} slots, lengths [{min_l}..{max_l}], avg {avg_l:.1f}")
