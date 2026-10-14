import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Pure Portuguese 2-letter words (NO abbreviations, NO English):
p2_list = [
    "AR", "IR", "VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "LE",
    "PE", "PA", "PO", "DO", "RE", "MI", "FA", "SI", "TI", "EU", "AI", "OI", "RA", "MA", "VA", "TA",
    "VE", "CA", "TU", "NE", "TO", "FE", "LI", "AO"
]
pure_2 = set(strip_accents(w) for w in p2_list)

# Pure Portuguese 3-letter words (NO abbreviations, NO English):
p3_list = [
    "SOL", "LUA", "MAR", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI",
    "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR",
    "VER", "DAR", "SER", "VOZ", "BEM", "SIM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS",
    "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR",
    "BOI", "TIO", "TIA", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU",
    "SOU", "NOS", "VOZ", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "QUER", "FAZ", "FEZ", "VIU",
    "DIZ", "FUI", "FIZ", "TEM", "SAO", "MIM", "DAS", "DOS", "LHE", "VAO", "ALVO", "AQUI", "HOJE"
]
pure_3 = set(strip_accents(w) for w in p3_list if len(strip_accents(w)) == 3)

# Load 6-letter words from top_common_clean.txt
# Filter out names or strange words
bad_6 = {"PHILIP", "GORDON", "VAUGHN", "VERNON", "EILEEN", "EDISON", "STEVEN", "SHARON", "STEFAN", "IORQUE", "IRAQUE", "RONNIE", "RAYLAN", "REAGAN", "ELIJAH", "BISHOP", "BACKUP", "BATMAN", "BURTON", "BONNIE", "BROOKE", "TROUXE", "TRUMAN", "TARZAN", "NICOLE", "NADINE", "NATHAN", "NELSON", "NORMAN", "PEYTON", "EVELYN", "ORANGE", "YELLOW", "SILVER", "GEORGE", "ARTHUR", "ROBERT", "THOMAS"}

words_6 = []
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        if len(clean) == 6 and int(freq) >= 120:
            if clean not in bad_6 and all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in clean):
                words_6.append(clean)

print(f"Pool sizes: 2-letter={len(pure_2)}, 3-letter={len(pure_3)}, 6-letter={len(words_6)}")

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
        slot_cands.append(list(pure_2))
    elif s["len"] == 3:
        slot_cands.append(list(pure_3))
    else:
        slot_cands.append(list(words_6))

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
            for w in slot_cands[idx]:
                if w in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != w[i]:
                        match = False
                        break
                if match:
                    matching.append(w)
                    if len(matching) > 25: break

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

found_solutions = []
for attempt in range(50):
    for idx, s in enumerate(slots):
        random.shuffle(slot_cands[idx])
    res = solve(8)
    if res:
        sol_grid, sol_words = res
        key = tuple(sol_words)
        if key not in [tuple(x[1]) for x in found_solutions]:
            print(f"\n[FOUND 100% PURE PORTUGUESE SOLUTION #{len(found_solutions) + 1}]:")
            for r in range(1, rows):
                line = [sol_grid[r][c] if (r, c) not in [(3, 3), (4, 4)] else "[]" for c in range(1, cols)]
                print(f"  Row {r}: {' '.join(line)}")
            for i, s in enumerate(slots):
                print(f"    {s['id']} ({s['dir']}): {sol_words[i]}")
            found_solutions.append((sol_grid, sol_words))
            if len(found_solutions) >= 3:
                break

print(f"\nTotal solutions found: {len(found_solutions)}")
