import itertools

def solve_grid(grid_mask, rows, cols):
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
                across_slots.append({'dir': 'right', 'row': r, 'col': c_start, 'length': length, 'clue': (r, clue_c)})
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
                down_slots.append({'dir': 'down', 'row': r_start, 'col': c, 'length': length, 'clue': (clue_r, c)})
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

print("Searching for layouts with max_length <= 5 or 6...")
best_layouts = []
for num_clues in [3, 4, 5, 6]:
    for cand in itertools.combinations(interior_cells, num_clues):
        m = make_base(rows, cols)
        for r, c in cand: m[r][c] = 'C'
        slots = solve_grid(m, rows, cols)
        if slots:
            lens = [s['length'] for s in slots]
            if min(lens) >= 2 and max(lens) <= 6:
                best_layouts.append((cand, len(slots), min(lens), max(lens), sum(lens)/len(lens)))

print(f"Found {len(best_layouts)} layouts with max_length <= 6!")
# Sort by lowest max_length, then highest number of slots
best_layouts.sort(key=lambda x: (x[3], -x[1]))
for cand, n_slots, min_l, max_l, avg_l in best_layouts[:20]:
    print(f"  Clues {cand}: {n_slots} slots, [{min_l}..{max_l}], avg {avg_l:.1f}")
