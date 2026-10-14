import unicodedata
import random
import time
import json
from strict_verifier import test_level_design

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# English/acronym blacklist
bad_2_3 = {
    "OH", "AH", "UH", "OK", "TV", "US", "IT", "OF", "IN", "SR", "KM", "PM", "DJ", "CD", "PC", "RH", "DR",
    "BIG", "GIN", "ST", "AIR", "TL", "IOF", "LII", "NG", "USC", "SP", "MG", "AV", "GA", "OC", "OPI", "ROP",
    "DNA", "FBI", "CIA", "PDF", "MY", "WE", "GO", "NO", "HE", "IS", "AM", "AT", "BY", "UP", "AN", "BE", "AS",
    "BO", "ER", "ARI", "ACE", "ADA", "DORIAN", "AROMIA", "SOREAR", "ASCUAR", "PNEUMA", "ZAC", "CEL", "AROUND"
}

# Note: AS, NO, AM, AT, BE, BO are Portuguese in some contexts, but let's exclude the ambiguous ones so words are crystal clear!
# Allowed 2-letter words:
pure_2 = {
    "DE", "EU", "UM", "SE", "EM", "ME", "DO", "DA", "OS", "NO", "NA", "SO", "TE", "JA", "OU", "AO", "HA", "LA",
    "IR", "AI", "EI", "VA", "OI", "VI", "TA", "IA", "VE", "CA", "SI", "PE", "AR", "TU", "NE", "TO", "MA", "FE",
    "TI", "LI", "RA", "PA", "PO"
}

# Load clean words
words_by_len = {2: list(pure_2), 3: [], 6: []}
freq_map = {}
orig_map = {w: w.lower() for w in pure_2}

# Accents for 2-letter
orig_map.update({
    "SO": "só", "JA": "já", "HA": "há", "LA": "lá", "VA": "vá", "TA": "tá", "VE": "vê", "CA": "cá",
    "PE": "pé", "NE": "né", "TO": "tô", "MA": "má", "FE": "fé", "RA": "rã", "PA": "pá", "PO": "pó"
})

with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        freq = int(freq)
        if clean in bad_2_3 or len(clean) not in [3, 6]: continue
        if not all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in clean): continue
        if freq >= 80:
            words_by_len[len(clean)].append(clean)
            freq_map[clean] = freq
            orig_map[clean] = orig

print(f"Candidate pools: len2={len(words_by_len[2])}, len3={len(words_by_len[3])}, len6={len(words_by_len[6])}")

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

slot_candidates = []
for s in slots:
    l = s["len"]
    cands = sorted(words_by_len[l], key=lambda w: freq_map.get(w, 0) + random.randint(-150, 150), reverse=True)
    slot_candidates.append(cands)

def solve(max_time=10):
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
                    if len(matching) > 35: break

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

found_levels = []
for attempt in range(40):
    for idx, s in enumerate(slots):
        l = s["len"]
        slot_candidates[idx] = sorted(words_by_len[l], key=lambda w: freq_map.get(w, 0) + random.randint(-300, 300), reverse=True)

    res = solve(8)
    if res:
        sol_grid, sol_words = res
        # Quality check: ensure no bad words slipped in
        if any(w in bad_2_3 for w in sol_words): continue
        key = tuple(sol_words)
        if key not in [tuple(x[1]) for x in found_levels]:
            print(f"\n=======================================================")
            print(f"[FOUND CLEAN LEVEL #{len(found_levels) + 1}]:")
            print(f"=======================================================")
            for r in range(1, rows):
                line = [sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else "[]" for c in range(1, cols)]
                print(f"  Row {r}: {' '.join(line)}")
            for i, s in enumerate(slots):
                orig = orig_map.get(sol_words[i], sol_words[i])
                print(f"    {s['id']} ({s['dir']}): {sol_words[i]} ({orig})")
            found_levels.append((sol_grid, sol_words))
            if len(found_levels) >= 3:
                break

print(f"\nTotal clean levels generated: {len(found_levels)}")

# Save found levels to json for compilation
if len(found_levels) >= 3:
    with open("scripts/raw_3_levels.json", "w", encoding="utf-8") as f:
        json.dump([{"grid": g, "words": w} for g, w in found_levels], f, indent=2)
    print("Saved to scripts/raw_3_levels.json!")
