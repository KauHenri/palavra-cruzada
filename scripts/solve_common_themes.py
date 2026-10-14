import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load top common words
words_by_len = {}
freq_map = {}
orig_map = {}

with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        freq = int(freq)
        l = len(clean)
        if l not in words_by_len:
            words_by_len[l] = []
        words_by_len[l].append(clean)
        freq_map[clean] = freq
        orig_map[clean] = orig

print("Words loaded by length:")
for l in sorted(words_by_len.keys()):
    print(f"  Len {l}: {len(words_by_len[l])} words")

# Mask 8x7 with clues at (3, 3) and (4, 4)
rows, cols = 8, 7
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
    {"id": "A9", "dir": "right", "row": 7, "col": 1, "len": 6, "coords": [(7, c) for c in range(1, 7)], "clue": (7, 0)},

    # Down
    {"id": "D1", "dir": "down", "row": 1, "col": 1, "len": 7, "coords": [(r, 1) for r in range(1, 8)], "clue": (0, 1)},
    {"id": "D2", "dir": "down", "row": 1, "col": 2, "len": 7, "coords": [(r, 2) for r in range(1, 8)], "clue": (0, 2)},
    {"id": "D3", "dir": "down", "row": 1, "col": 3, "len": 2, "coords": [(1, 3), (2, 3)], "clue": (0, 3)},
    {"id": "D4", "dir": "down", "row": 4, "col": 3, "len": 4, "coords": [(r, 3) for r in range(4, 8)], "clue": (3, 3)},
    {"id": "D5", "dir": "down", "row": 1, "col": 4, "len": 3, "coords": [(r, 4) for r in range(1, 4)], "clue": (0, 4)},
    {"id": "D6", "dir": "down", "row": 5, "col": 4, "len": 3, "coords": [(r, 4) for r in range(5, 8)], "clue": (4, 4)},
    {"id": "D7", "dir": "down", "row": 1, "col": 5, "len": 7, "coords": [(r, 5) for r in range(1, 8)], "clue": (0, 5)},
    {"id": "D8", "dir": "down", "row": 1, "col": 6, "len": 7, "coords": [(r, 6) for r in range(1, 8)], "clue": (0, 6)},
]

# Pre-sort candidate words by frequency
slot_cand_lists = []
for s in slots:
    l = s["len"]
    # Sort by frequency descending with small random jitter
    cands = sorted(words_by_len.get(l, []), key=lambda w: freq_map.get(w, 0) + random.randint(-500, 500), reverse=True)
    slot_cand_lists.append(cands)

def solve_grid(theme_word=None, theme_slot_idx=0, max_time=12):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()

    if theme_word:
        s = slots[theme_slot_idx]
        assigned[theme_slot_idx] = theme_word
        used.add(theme_word)
        for i, (r, c) in enumerate(s["coords"]):
            grid[r][c] = theme_word[i]

    start_time = time.time()

    def backtrack():
        if time.time() - start_time > max_time:
            return None

        # MRV
        best_idx = None
        best_cands = None

        for idx in range(len(slots)):
            if assigned[idx] is not None: continue
            s = slots[idx]
            pattern = [grid[r][c] for r, c in s["coords"]]
            matching = []
            for w in slot_cand_lists[idx]:
                if w in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != w[i]:
                        match = False
                        break
                if match:
                    matching.append(w)
                    if len(matching) > 35: break

            if len(matching) == 0:
                return None

            if best_cands is None or len(matching) < len(best_cands):
                best_cands = matching
                best_idx = idx
                if len(best_cands) <= 1: break

        if best_idx is None:
            return grid, assigned

        s = slots[best_idx]
        coords = s["coords"]

        for w in best_cands[:12]:
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

# Let's search solutions for several themes!
themes = [
    ("BRASIL", 0),
    ("VIAGEM", 0),
    ("CIDADE", 0),
    ("CINEMA", 0),
    ("TEATRO", 0),
    ("COMIDA", 0),
    ("AMORES", 0),
    ("PRAIAS", 0),
]

solutions = []
for theme, s_idx in themes:
    print(f"Searching solution anchored at {theme}...")
    res = solve_grid(theme, s_idx, max_time=8)
    if res:
        sol_grid, sol_words = res
        print(f"--> FOUND SOLUTION FOR {theme}!")
        for r in range(1, rows):
            line = []
            for c in range(1, cols):
                if (r, c) in [(3, 3), (4, 4)]: line.append("[]")
                else: line.append(sol_grid[r][c])
            print(f"    {' '.join(line)}")
        solutions.append((theme, sol_grid, sol_words))
    else:
        print(f"--> Timeout for {theme}")

print(f"\nTotal solutions found: {len(solutions)}")
