import itertools

def solve_grid(grid_mask, rows, cols):
    across_slots = []
    down_slots = []
    clue_counts = {}
    for r in range(rows):
        for c in range(cols):
            if grid_mask[r][c] == 'C':
                clue_counts[(r, c)] = 0

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
                clue_counts[(r, clue_c)] = clue_counts.get((r, clue_c), 0) + 1
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
                clue_counts[(clue_r, c)] = clue_counts.get((clue_r, c), 0) + 1
                down_slots.append({'dir': 'down', 'row': r_start, 'col': c, 'length': length, 'clue': (clue_r, c)})
            else:
                r += 1

    # Check that no clue cell has more than 2 clues, and no clue cell is unused
    for pos, count in clue_counts.items():
        if count == 0: return None
        if count > 2: return None

    return across_slots, down_slots

def make_base(R, C):
    m = [['L'] * C for _ in range(R)]
    m[0][0] = 'E'
    for c in range(1, C): m[0][c] = 'C'
    for r in range(1, R): m[r][0] = 'C'
    return m

rows, cols = 7, 7
interior_cells = [(r, c) for r in range(1, rows) for c in range(1, cols)]

valid_layouts = []
for num_clues in [2, 3, 4]:
    for cand in itertools.combinations(interior_cells, num_clues):
        m = make_base(rows, cols)
        for r, c in cand: m[r][c] = 'C'
        res = solve_grid(m, rows, cols)
        if res:
            across, down = res
            slots = across + down
            lens = [s['length'] for s in slots]
            # Must have no 1-letter words
            if min(lens) >= 2:
                valid_layouts.append((cand, len(slots), lens, m, across, down))

print(f"Found {len(valid_layouts)} valid layouts for 7x7!")
# Sort by min length >= 2, max length <= 6, nice distribution
for cand, n_slots, lens, m, across, down in valid_layouts[:15]:
    print(f"\nLayout clues={cand}: {n_slots} slots, lens={sorted(lens)}")
    for row in m:
        print("  " + " ".join(row))
