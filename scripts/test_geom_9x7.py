def test_mask(interior_clues):
    clue_set = set(interior_clues)
    print("Testing clues:", interior_clues)
    
    # Across
    across = []
    for r in range(1, 9):
        c = 1
        while c <= 6:
            if (r, c) not in clue_set:
                cells = []
                while c <= 6 and (r, c) not in clue_set:
                    cells.append((r, c))
                    c += 1
                across.append(cells)
            else:
                c += 1
                
    # Down
    down = []
    for c in range(1, 7):
        r = 1
        while r <= 8:
            if (r, c) not in clue_set:
                cells = []
                while r <= 8 and (r, c) not in clue_set:
                    cells.append((r, c))
                    r += 1
                down.append(cells)
            else:
                r += 1
                
    print(f"Total Across slots: {len(across)}")
    for a in across:
        print(f"  A len {len(a)}: {a[0]} to {a[-1]}")
    print(f"Total Down slots: {len(down)}")
    for d in down:
        print(f"  D len {len(d)}: {d[0]} to {d[-1]}")
        
    all_lens = [len(a) for a in across] + [len(d) for d in down]
    print(f"Min len: {min(all_lens)}, Max len: {max(all_lens)}")
    print(f"Length distribution: { {l: all_lens.count(l) for l in sorted(set(all_lens))} }")

test_mask([(2, 3), (3, 4), (6, 4), (8, 3)])
