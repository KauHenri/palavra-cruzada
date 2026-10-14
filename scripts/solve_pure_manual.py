import unicodedata
import random
from verified_dict import manual_words

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

clean_manual = {}
for w, clue in manual_words.items():
    c = strip_accents(w)
    l = len(c)
    if l not in clean_manual: clean_manual[l] = []
    clean_manual[l].append((c, w, clue))

print("Manual words by length:")
for l in sorted(clean_manual.keys()):
    print(f"  Len {l}: {len(clean_manual[l])} words")

# Mask 7x7 with clues at (3, 3) and (4, 4)
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

# Let's search if manual words alone can fill 7x7!
def solve():
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()

    def backtrack():
        best_idx = None
        best_words = None

        for idx, s in enumerate(slots):
            if assigned[idx] is not None: continue
            pattern = [grid[r][c] for r, c in s["coords"]]
            matching = []
            for clean, orig, clue in clean_manual.get(s["len"], []):
                if clean in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != clean[i]:
                        match = False
                        break
                if match:
                    matching.append((clean, orig, clue))

            if len(matching) == 0: return None

            if best_words is None or len(matching) < len(best_words):
                best_words = matching
                best_idx = idx
                if len(best_words) <= 1: break

        if best_idx is None:
            return grid, assigned

        s = slots[best_idx]
        coords = s["coords"]

        for clean, orig, clue in best_words:
            old = [grid[r][c] for r, c in coords]
            for i, (r, c) in enumerate(coords): grid[r][c] = clean[i]
            assigned[best_idx] = (clean, orig, clue)
            used.add(clean)

            res = backtrack()
            if res: return res

            for i, (r, c) in enumerate(coords): grid[r][c] = old[i]
            assigned[best_idx] = None
            used.remove(clean)

        return None

    return backtrack()

print("Solving 7x7 strictly with manual words...")
res = solve()
if res:
    print("SOLVED STRICTLY WITH MANUAL WORDS!")
    sol_grid, sol_words = res
    for r in range(1, rows):
        print(f"Row {r}: {' '.join(sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else '[]' for c in range(1, cols))}")
else:
    print("Manual words alone too sparse for full 6-letter stack.")
