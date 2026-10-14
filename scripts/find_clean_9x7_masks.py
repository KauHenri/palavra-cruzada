import sys
import itertools

# Cells that can contain clues without trivially isolating adjacent boundary cells:
# If single clue: r in {3,4,5,6}, c in {3,4}
# But if double clue in row (e.g. c=3 and c=4): cols 1..2 (2 letters), cols 5..6 (2 letters)
# What if clues are in cols 2 and 3? (r, 1) is 1 letter, bad.

candidate_cells = [(r, c) for r in range(3, 7) for c in range(3, 5)]
print("Candidate cells:", candidate_cells)

valid_masks = []
for k in range(2, 5):
    for clue_comb in itertools.combinations(candidate_cells, k):
        clue_set = set(clue_comb)
        
        # Check Across slots
        across_lens = []
        bad = False
        for r in range(1, 9):
            c = 1
            while c <= 6:
                if (r, c) not in clue_set:
                    l = 0
                    while c <= 6 and (r, c) not in clue_set:
                        l += 1
                        c += 1
                    if l < 2:
                        bad = True
                        break
                    across_lens.append(l)
                else:
                    c += 1
            if bad:
                break
        if bad:
            continue

        # Check Down slots
        down_lens = []
        for c in range(1, 7):
            r = 1
            while r <= 8:
                if (r, c) not in clue_set:
                    l = 0
                    while r <= 8 and (r, c) not in clue_set:
                        l += 1
                        r += 1
                    if l < 2:
                        bad = True
                        break
                    down_lens.append(l)
                else:
                    r += 1
            if bad:
                break
        if bad:
            continue

        num_2 = across_lens.count(2) + down_lens.count(2)
        valid_masks.append({
            "clues": clue_comb,
            "num_clues": len(clue_comb),
            "num_2": num_2,
            "across": across_lens,
            "down": down_lens,
            "total_words": len(across_lens) + len(down_lens)
        })

print(f"Found {len(valid_masks)} valid masks!")
valid_masks.sort(key=lambda m: (m["num_2"], -m["total_words"]))
for m in valid_masks:
    print(f"Clues: {m['clues']} | Total words: {m['total_words']} | 2-letter words: {m['num_2']}")
    print(f"  Across: {sorted(m['across'])}")
    print(f"  Down:   {sorted(m['down'])}")
