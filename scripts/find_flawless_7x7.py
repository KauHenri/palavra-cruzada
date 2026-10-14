import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Permitted 2-letter words: ONLY genuine Portuguese words
raw_2 = ["AR", "IR", "VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "LE", "PE", "PA", "PO", "DO", "RE", "MI", "FA", "SI", "TI", "EU", "AI", "OI", "RA", "MA"]
valid_2_letter = set(strip_accents(w) for w in raw_2 if len(strip_accents(w)) == 2)

# Permitted 3-letter words: ONLY genuine Portuguese words
raw_3 = [
    "SOL", "LUA", "MAR", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI",
    "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR",
    "VER", "DAR", "SER", "VOZ", "BEM", "SIM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS",
    "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR",
    "BOI", "TIO", "TIA", "AVO", "PAI", "MAE", "GOL"
]
valid_3_letter = set(strip_accents(w) for w in raw_3 if len(strip_accents(w)) == 3)

# Load 6-letter words from common list
words_6 = []
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        if len(clean) == 6 and int(freq) >= 150:
            if all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in clean):
                words_6.append(clean)

print(f"Candidates: {len(valid_2_letter)} 2-letter, {len(valid_3_letter)} 3-letter, {len(words_6)} 6-letter words.")

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

slot_cands = []
for s in slots:
    if s["len"] == 2:
        slot_cands.append([w for w in valid_2_letter if len(w) == 2])
    elif s["len"] == 3:
        slot_cands.append([w for w in valid_3_letter if len(w) == 3])
    else:
        slot_cands.append([w for w in words_6 if len(w) == 6])

def solve(max_time=15):
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
            for w in slot_cands[idx]:
                if w in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != w[i]:
                        match = False
                        break
                if match:
                    matching.append(w)
                    if len(matching) > 20: break

            if len(matching) == 0: return None

            if best_words is None or len(matching) < len(best_words):
                best_words = matching
                best_idx = idx
                if len(best_words) <= 1: break

        if best_idx is None:
            return [row[:] for row in grid], assigned[:]

        s = slots[best_idx]
        coords = s["coords"]

        for w in best_words[:10]:
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
for attempt in range(25):
    for idx, s in enumerate(slots):
        random.shuffle(slot_cands[idx])
    res = solve(8)
    if res:
        sol_grid, sol_words = res
        key = tuple(sol_words)
        if key not in [tuple(s[1]) for s in solutions]:
            print(f"\n[FOUND FLAWLESS 7x7 SOLUTION #{len(solutions) + 1}]:")
            for r in range(1, rows):
                line = [sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else "[]" for c in range(1, cols)]
                print(f"  {' '.join(line)}")
            for i, s in enumerate(slots):
                print(f"    {s['id']} ({s['dir']}): {sol_words[i]}")
            solutions.append((sol_grid, sol_words))
            if len(solutions) >= 3:
                break

print(f"\nTotal flawless levels ready: {len(solutions)}")
