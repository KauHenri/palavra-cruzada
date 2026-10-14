import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words, excluding English loan words or abbreviations
blacklist = {"BIG", "GIN", "ST", "AIR", "TL", "IOF", "LII", "NG", "USC", "AT", "MR", "SP", "MG", "AV", "GA", "OC", "OPI", "ROP"}

words_by_len = {}
freq_map = {}
orig_map = {}

with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        freq = int(freq)
        if clean in blacklist or len(clean) < 2: continue
        # Only words with standard Portuguese letters
        if not all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in clean): continue
        if freq >= 100:
            l = len(clean)
            if l not in words_by_len: words_by_len[l] = []
            words_by_len[l].append(clean)
            freq_map[clean] = freq
            orig_map[clean] = orig

# Add our rich Portuguese words
extra_portuguese = [
    # 2 letters
    ("AR", "ar", 10000), ("PA", "pá", 5000), ("PE", "pé", 8000), ("PO", "pó", 6000),
    ("LA", "lá", 9000), ("LE", "lê", 7000), ("NO", "nó", 6000), ("OU", "ou", 12000),
    ("SE", "se", 15000), ("DO", "dó", 8000), ("RE", "ré", 7000), ("MI", "mi", 6000),
    ("FA", "fá", 6000), ("SI", "si", 8000), ("TI", "ti", 9000), ("EU", "eu", 15000),
    ("AI", "ai", 10000), ("OI", "oi", 12000), ("IR", "ir", 14000), ("VI", "vi", 11000),
    ("JA", "já", 13000), ("HA", "há", 12000), ("SO", "só", 14000), ("UM", "um", 15000),
    ("AS", "as", 15000), ("OS", "os", 15000), ("EM", "em", 15000), ("NA", "na", 15000),
    ("DA", "da", 15000), ("DE", "de", 15000), ("RA", "rã", 5000), ("MA", "má", 7000),
    # 3 letters
    ("SOL", "sol", 9000), ("LUA", "lua", 9000), ("MAR", "mar", 9000), ("RIO", "rio", 9000),
    ("RUA", "rua", 9000), ("CEU", "céu", 9000), ("MEL", "mel", 8000), ("PAO", "pão", 8000),
    ("PAZ", "paz", 9000), ("LUZ", "luz", 9000), ("COR", "cor", 8000), ("SOM", "som", 8000),
    ("REI", "rei", 8000), ("MAO", "mão", 9000), ("FIM", "fim", 9000), ("ANO", "ano", 9000),
    ("ATO", "ato", 7000), ("ELO", "elo", 6000), ("ERA", "era", 9000), ("SAL", "sal", 7000),
    ("ASA", "asa", 7000), ("UVA", "uva", 7000), ("OVO", "ovo", 8000), ("ACO", "aço", 7000),
    ("BOA", "boa", 9000), ("RIR", "rir", 8000), ("VER", "ver", 9000), ("DAR", "dar", 9000),
    ("SER", "ser", 9000), ("VOZ", "voz", 8000), ("BEM", "bem", 9000), ("SIM", "sim", 9000),
    ("CHA", "chá", 7000), ("DIA", "dia", 9000), ("DOM", "dom", 7000), ("LEI", "lei", 8000),
    ("PIA", "pia", 6000), ("GEL", "gel", 5000), ("GAS", "gás", 7000), ("LAR", "lar", 8000),
    ("FIO", "fio", 7000), ("OLA", "olá", 8000), ("MAS", "mas", 9000), ("ATE", "até", 9000),
    ("POR", "por", 9000), ("SEM", "sem", 9000), ("SOB", "sob", 8000), ("TAL", "tal", 8000),
    ("MAL", "mal", 8000), ("VEM", "vem", 9000), ("VAI", "vai", 9000),
]
for clean, orig, freq in extra_portuguese:
    l = len(clean)
    if l not in words_by_len: words_by_len[l] = []
    if clean not in words_by_len[l]:
        words_by_len[l].append(clean)
    freq_map[clean] = freq
    orig_map[clean] = orig

print("Filtered clean vocabulary ready.")

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
    cands = sorted(words_by_len.get(l, []), key=lambda w: freq_map.get(w, 0) + random.randint(-100, 100), reverse=True)
    slot_candidates.append(cands)

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

found = []
for attempt in range(8):
    # Jitter the candidate lists
    for idx, s in enumerate(slots):
        l = s["len"]
        slot_candidates[idx] = sorted(words_by_len.get(l, []), key=lambda w: freq_map.get(w, 0) + random.randint(-300, 300), reverse=True)

    print(f"Attempt {attempt + 1}...")
    res = solve(10)
    if res:
        sol_grid, sol_words = res
        # Check if contains any blacklisted or weird words
        if any(w in blacklist for w in sol_words):
            continue
        print(f"--> Found Valid Level #{len(found) + 1}!")
        for r in range(1, rows):
            line = [sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else "[]" for c in range(1, cols)]
            print(f"    {' '.join(line)}")
        for i, s in enumerate(slots):
            orig = orig_map.get(sol_words[i], sol_words[i])
            print(f"      {s['id']} ({s['dir']}): {sol_words[i]} ({orig})")
        found.append((sol_grid, sol_words))
        if len(found) >= 3:
            break

print(f"\nTotal levels found: {len(found)}")
