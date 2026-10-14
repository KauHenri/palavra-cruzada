import unicodedata
import random
import time
from clues_database import CLUES_DB
from strict_verifier import test_level_design

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Filter CLUES_DB for clean uppercase keys
clue_keys_by_len = {}
for w in CLUES_DB.keys():
    clean = strip_accents(w)
    l = len(clean)
    if l not in clue_keys_by_len: clue_keys_by_len[l] = []
    if clean not in clue_keys_by_len[l]:
        clue_keys_by_len[l].append(clean)

print("Words available in CLUES_DB:")
for l in sorted(clue_keys_by_len.keys()):
    print(f"  Len {l}: {len(clue_keys_by_len[l])} words")

# Mask 7x7
rows, cols = 7, 7
slots = [
    # Across
    {"id": "A1", "dir": "right", "row": 1, "col": 1, "len": 6, "coords": [(1, c) for c in range(1, 7)], "clue": (1, 0)},
    {"id": "A2", "dir": "right", "row": 2, "col": 1, "len": 6, "coords": [(2, c) for c in range(1, 7)], "clue": (2, 0)},
    {"id": "A3", "dir": "right", "row": 3, "col": 1, "len": 2, "coords": [(3, 1), (3, 2)], "clue": (3, 0)},
    {"id": "A4", "dir": "right", "row": 3, "col": 4, "len": 3, "coords": [(3, 4), (3, 5), (3, 6)], "clue": (3, 3)},
    {"id": "A5", "dir": "right", "row": 4, "col": 1, "len": 3, "coords": [(4, 1), (4, 2), (4, 3)], "clue": (4, 0)},
    {"id": "A6", "dir": "right", "row": 4, "col": 5, "len": 2, "coords": [(4, 5), (4, 6)], "clue": (4, 4)},
    {"id": "A7", "dir": "right", "row": 5, "col": 1, "len": 6, "coords": [(5, c) for c in range(1, 7)], "clue": (5, 0)},
    {"id": "A8", "dir": "right", "row": 6, "col": 1, "len": 6, "coords": [(6, c) for c in range(1, 7)], "clue": (6, 0)},

    # Down
    {"id": "D1", "dir": "down", "row": 1, "col": 1, "len": 6, "coords": [(r, 1) for r in range(1, 7)], "clue": (0, 1)},
    {"id": "D2", "dir": "down", "row": 1, "col": 2, "len": 6, "coords": [(r, 2) for r in range(1, 7)], "clue": (0, 2)},
    {"id": "D3", "dir": "down", "row": 1, "col": 3, "len": 2, "coords": [(1, 3), (2, 3)], "clue": (0, 3)},
    {"id": "D4", "dir": "down", "row": 4, "col": 3, "len": 3, "coords": [(r, 3) for r in range(4, 7)], "clue": (3, 3)},
    {"id": "D5", "dir": "down", "row": 1, "col": 4, "len": 3, "coords": [(r, 4) for r in range(1, 4)], "clue": (0, 4)},
    {"id": "D6", "dir": "down", "row": 5, "col": 4, "len": 2, "coords": [(r, 4) for r in range(5, 7)], "clue": (4, 4)},
    {"id": "D7", "dir": "down", "row": 1, "col": 5, "len": 6, "coords": [(r, 5) for r in range(1, 7)], "clue": (0, 5)},
    {"id": "D8", "dir": "down", "row": 1, "col": 6, "len": 6, "coords": [(r, 6) for r in range(1, 7)], "clue": (0, 6)},
]

# Load additional common 6-letter words from top_common_clean.txt so solver has enough 6-letter choices
words_6_all = list(clue_keys_by_len.get(6, []))
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        c, o, fr = line.strip().split()
        if len(c) == 6 and int(fr) >= 100:
            if c not in words_6_all:
                words_6_all.append(c)

print(f"Total 6-letter words available: {len(words_6_all)}")

slot_candidates = []
for s in slots:
    if s["len"] == 2:
        slot_candidates.append(list(clue_keys_by_len.get(2, [])))
    elif s["len"] == 3:
        slot_candidates.append(list(clue_keys_by_len.get(3, [])))
    else:
        slot_candidates.append(list(words_6_all))

def solve(max_time=12):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()
    start_t = time.time()

    def backtrack():
        if time.time() - start_t > max_time: return None

        best_idx = None
        best_words = None

        for idx, s in enumerate(slots):
            if assigned[idx] is not None: continue
            pattern = [grid[r][c] for r, c in s["coords"]]
            matching = []
            for w in slot_candidates[idx]:
                if w in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != w[i]:
                        match = False
                        break
                if match:
                    matching.append(w)
                    if len(matching) > 30: break

            if len(matching) == 0: return None

            if best_words is None or len(matching) < len(best_words):
                best_words = matching
                best_idx = idx
                if len(best_words) <= 1: break

        if best_idx is None:
            return [row[:] for row in grid], assigned[:]

        s = slots[best_idx]
        coords = s["coords"]

        for w in best_words[:12]:
            old = [grid[r][c] for r, c in coords]
            for i, (r, c) in enumerate(coords): grid[r][c] = w[i]
            assigned[best_idx] = w
            used.add(w)

            res = backtrack()
            if res: return res

            for i, (r, c) in enumerate(coords): grid[r][c] = old[i]
            assigned[best_idx] = None
            used.remove(w)

        return None

    return backtrack()

solutions = []
for attempt in range(30):
    for idx, s in enumerate(slots):
        random.shuffle(slot_candidates[idx])
    res = solve(8)
    if res:
        sol_grid, sol_words = res
        key = tuple(sol_words)
        if key not in [tuple(s[1]) for s in solutions]:
            print(f"\n[FOUND VERIFIED SOLUTION #{len(solutions) + 1}]:")
            for r in range(1, rows):
                line = [sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else "[]" for c in range(1, cols)]
                print(f"  {' '.join(line)}")
            for i, s in enumerate(slots):
                print(f"    {s['id']} ({s['dir']}): {sol_words[i]}")
            solutions.append((sol_grid, sol_words))
            if len(solutions) >= 5:
                break

print(f"\nTotal verified solutions: {len(solutions)}")
