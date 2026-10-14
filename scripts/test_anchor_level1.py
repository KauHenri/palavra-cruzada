import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load clean words
words_by_len = {}
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        c = strip_accents(line.strip())
        if c.isalpha() and 2 <= len(c) <= 6:
            l = len(c)
            if l not in words_by_len: words_by_len[l] = set()
            words_by_len[l].add(c)

# Slots 7x7
rows, cols = 7, 7
slots = [
    # Across
    {"id": "A1", "dir": "right", "row": 1, "col": 1, "len": 6, "coords": [(1, c) for c in range(1, 7)]},
    {"id": "A2", "dir": "right", "row": 2, "col": 1, "len": 6, "coords": [(2, c) for c in range(1, 7)]},
    {"id": "A3", "dir": "right", "row": 3, "col": 1, "len": 2, "coords": [(3, 1), (3, 2)]},
    {"id": "A4", "dir": "right", "row": 3, "col": 4, "len": 3, "coords": [(3, 4), (3, 5), (3, 6)]},
    {"id": "A5", "dir": "right", "row": 4, "col": 1, "len": 3, "coords": [(4, 1), (4, 2), (4, 3)]},
    {"id": "A6", "dir": "right", "row": 4, "col": 5, "len": 2, "coords": [(4, 5), (4, 6)]},
    {"id": "A7", "dir": "right", "row": 5, "col": 1, "len": 6, "coords": [(5, c) for c in range(1, 7)]},
    {"id": "A8", "dir": "right", "row": 6, "col": 1, "len": 6, "coords": [(6, c) for c in range(1, 7)]},

    # Down
    {"id": "D1", "dir": "down", "row": 1, "col": 1, "len": 6, "coords": [(r, 1) for r in range(1, 7)]},
    {"id": "D2", "dir": "down", "row": 1, "col": 2, "len": 6, "coords": [(r, 2) for r in range(1, 7)]},
    {"id": "D3", "dir": "down", "row": 1, "col": 3, "len": 2, "coords": [(1, 3), (2, 3)]},
    {"id": "D4", "dir": "down", "row": 4, "col": 3, "len": 3, "coords": [(r, 3) for r in range(4, 7)]},
    {"id": "D5", "dir": "down", "row": 1, "col": 4, "len": 3, "coords": [(r, 4) for r in range(1, 4)]},
    {"id": "D6", "dir": "down", "row": 5, "col": 4, "len": 2, "coords": [(r, 4) for r in range(5, 7)]},
    {"id": "D7", "dir": "down", "row": 1, "col": 5, "len": 6, "coords": [(r, 5) for r in range(1, 7)]},
    {"id": "D8", "dir": "down", "row": 1, "col": 6, "len": 6, "coords": [(r, 6) for r in range(1, 7)]},
]

# Common words filter
common_words = set()
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        c, o, fr = line.strip().split()
        if int(fr) >= 80: common_words.add(c)

def solve_with_anchors(anchors, max_time=10):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()

    for s_idx, w in anchors.items():
        assigned[s_idx] = w
        used.add(w)
        for i, (r, c) in enumerate(slots[s_idx]["coords"]):
            grid[r][c] = w[i]

    # Candidates sorted by commonality
    slot_cands = []
    for s in slots:
        l = s["len"]
        cands = list(words_by_len.get(l, []))
        cands.sort(key=lambda w: (w in common_words, random.random()), reverse=True)
        slot_cands.append(cands)

    start_t = time.time()

    def backtrack():
        if time.time() - start_t > max_time: return None

        best_idx = None
        best_words = None

        for idx, s in enumerate(slots):
            if assigned[idx] is not None: continue
            pattern = [grid[r][c] for r, c in s["coords"]]
            matching = []
            for w in slot_cands[idx]:
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

# Let's test anchoring Level 1 with PRAIAS
print("Searching Level 1 (Theme: Viagens)...")
for anchor_w in ["PRAIAS", "VIAGEM", "CIDADE", "BRASIL"]:
    print(f"Testing anchor A1 = {anchor_w}...")
    res = solve_with_anchors({0: anchor_w}, max_time=6)
    if res:
        sol_grid, sol_words = res
        print(f"FOUND THEMATIC LEVEL FOR {anchor_w}!")
        for r in range(1, rows):
            print(f"  Row {r}: {' '.join(sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else '[]' for c in range(1, cols))}")
        for i, s in enumerate(slots):
            print(f"    {s['id']} ({s['dir']}): {sol_words[i]}")
        break
