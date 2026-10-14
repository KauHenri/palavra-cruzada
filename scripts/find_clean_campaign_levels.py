import unicodedata
import random
import time
from strict_verifier import test_level_design

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words from palavras_full.txt
print("Loading clean dictionary...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw_lines = [l.strip() for l in f if l.strip()]

# Exclude rare endings, proper nouns, archaic verb forms
bad_suffixes = ("ISSE", "ISSEM", "ASSE", "ASSEM", "ARDES", "ERDES", "IRDES", "ARMO", "ERMO", "IRMO", "AREIS", "EREIS", "IREIS")

clean_dict_by_len = {}
raw_map = {}

for w in raw_lines:
    # If original word starts with uppercase, it might be a name
    if w[0].isupper() and w.lower() in raw_lines:
        w = w.lower()

    clean = strip_accents(w)
    if not clean.isalpha() or not (2 <= len(clean) <= 8):
        continue

    # Skip obscure suffixes
    if any(clean.endswith(suf) for suf in bad_suffixes):
        continue

    l = len(clean)
    if l not in clean_dict_by_len:
        clean_dict_by_len[l] = set()
    clean_dict_by_len[l].add(clean)
    if clean not in raw_map:
        raw_map[clean] = w

print(f"Clean dictionary loaded: {sum(len(v) for v in clean_dict_by_len.values())} words.")

# Load common words
common_words = set()
with open("scripts/top_common_clean.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        if int(freq) > 100:
            common_words.add(clean)

print(f"High frequency vocabulary: {len(common_words)} words.")

# 8x7 mask with clues at (3, 3) and (4, 4)
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

# Build candidate lists sorted: common words FIRST, then normal clean words
slot_candidates = []
for s in slots:
    l = s["len"]
    cands = list(clean_dict_by_len.get(l, []))
    # Score by commonality
    cands.sort(key=lambda w: (w in common_words, random.random()), reverse=True)
    slot_candidates.append(cands)

def solve(anchor_slot=None, anchor_word=None, max_time=10):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()

    if anchor_slot is not None and anchor_word:
        assigned[anchor_slot] = anchor_word
        used.add(anchor_word)
        for i, (r, c) in enumerate(slots[anchor_slot]["coords"]):
            grid[r][c] = anchor_word[i]

    start_t = time.time()

    def backtrack():
        if time.time() - start_t > max_time:
            return None

        # MRV
        best_idx = None
        best_cands = None

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
                    if len(matching) > 50: break

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

        for w in best_cands[:20]:
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

# Let's search for 3 distinct, beautiful solutions!
themes = ["BRASIL", "VIAGEM", "CINEMA", "COMIDA", "AMORES", "NUVENS", "FLORES", "PARQUE"]

found_levels = []
for t in themes:
    print(f"Searching for level with anchor '{t}'...")
    res = solve(0, t, max_time=15)
    if res:
        sol_grid, sol_words = res
        common_count = sum(1 for w in sol_words if w in common_words)
        print(f"  [SUCCESS] Found grid for {t}! Common words: {common_count}/{len(sol_words)}")
        for r in range(1, rows):
            row_chars = [sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else "[]" for c in range(1, cols)]
            print(f"    {' '.join(row_chars)}")
        for i, s in enumerate(slots):
            is_comm = "[★]" if sol_words[i] in common_words else "[ ]"
            print(f"      {is_comm} {s['id']} ({s['dir']}): {sol_words[i]}")
        found_levels.append((t, sol_grid, sol_words))
        if len(found_levels) >= 3:
            break
    else:
        print(f"  [TIMEOUT] Could not solve with anchor '{t}'.")

print(f"\nTotal levels ready: {len(found_levels)}")
