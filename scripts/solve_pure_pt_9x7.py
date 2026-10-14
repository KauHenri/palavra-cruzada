import sys
import unicodedata
from collections import defaultdict
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Excluded words (from Level 1, 2, 3)
USED_WORDS = {
    'RAPOSA', 'IMOVEL', 'SA', 'ARI', 'ADA', 'ME', 'DORIAN', 'ASTROS',
    'RISADA', 'AMADOS', 'PO', 'ART', 'OVA', 'IR', 'SERMAO', 'ALIENS',
    'CUSTAS', 'ANTIGA', 'SI', 'ACE', 'AM', 'CASADO', 'OSTRAS',
    'CASACO', 'UNICAS', 'ST', 'EST', 'TIA', 'AR', 'AGRADA', 'SAIMOS',
    'BRASIL', 'EURICO', 'LE', 'MAR', 'MIM', 'ARATUS', 'ZORAIA',
    'BELMAZ', 'RUEIRO', 'SIM', 'TA', 'ICAPUI', 'LOROSA'
}

# Load standard Portuguese dictionary
pt_dict = set()
pt_display = {}
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        raw = line.strip()
        w = strip_accents(raw)
        if w.isalpha():
            pt_dict.add(w)
            if w not in pt_display:
                pt_display[w] = raw.upper()

# Curated common 3-letter words
good_3 = {"SOL", "LUA", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "DAS", "DOS", "LHE", "VAO"} - USED_WORDS

words_by_len = defaultdict(set)
word_display = {}

with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            disp = parts[1] if len(parts) > 1 else parts[0]
            # Must be in standard Portuguese dictionary!
            if w.isalpha() and w in pt_dict and w not in USED_WORDS:
                words_by_len[len(w)].add(w)
                word_display[w] = pt_display.get(w, disp.upper())

words_by_len[3] = words_by_len[3].intersection(good_3) | (good_3 & pt_dict)

print("Standard Portuguese common word counts:")
for l in [3, 4, 6, 8]:
    print(f"Len {l}: {len(words_by_len[l])} words")

index = defaultdict(set)
for l in [3, 4, 6, 8]:
    for w in words_by_len[l]:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

clue_set = {(4, 1), (4, 2), (5, 5), (5, 6)}

slots = [
    # Across
    {"id": "A1", "dir": "A", "cells": [(1, c) for c in range(1, 7)]},
    {"id": "A2", "dir": "A", "cells": [(2, c) for c in range(1, 7)]},
    {"id": "A3", "dir": "A", "cells": [(3, c) for c in range(1, 7)]},
    {"id": "A4", "dir": "A", "cells": [(4, c) for c in range(3, 7)]}, # len 4
    {"id": "A5", "dir": "A", "cells": [(5, c) for c in range(1, 5)]}, # len 4
    {"id": "A6", "dir": "A", "cells": [(6, c) for c in range(1, 7)]},
    {"id": "A7", "dir": "A", "cells": [(7, c) for c in range(1, 7)]},
    {"id": "A8", "dir": "A", "cells": [(8, c) for c in range(1, 7)]},

    # Down
    {"id": "D1_top", "dir": "D", "cells": [(1, 1), (2, 1), (3, 1)]}, # len 3
    {"id": "D1_bot", "dir": "D", "cells": [(5, 1), (6, 1), (7, 1), (8, 1)]}, # len 4
    {"id": "D2_top", "dir": "D", "cells": [(1, 2), (2, 2), (3, 2)]}, # len 3
    {"id": "D2_bot", "dir": "D", "cells": [(5, 2), (6, 2), (7, 2), (8, 2)]}, # len 4
    {"id": "D3", "dir": "D", "cells": [(r, 3) for r in range(1, 9)]}, # len 8
    {"id": "D4", "dir": "D", "cells": [(r, 4) for r in range(1, 9)]}, # len 8
    {"id": "D5_top", "dir": "D", "cells": [(1, 5), (2, 5), (3, 5), (4, 5)]}, # len 4
    {"id": "D5_bot", "dir": "D", "cells": [(6, 5), (7, 5), (8, 5)]}, # len 3
    {"id": "D6_top", "dir": "D", "cells": [(1, 6), (2, 6), (3, 6), (4, 6)]}, # len 4
    {"id": "D6_bot", "dir": "D", "cells": [(6, 6), (7, 6), (8, 6)]}, # len 3
]

grid = {}
assigned = [None] * len(slots)
used_words = set()

def get_candidates(si):
    slot = slots[si]
    cells = slot["cells"]
    L = len(cells)
    constraints = [(ci, grid[cell]) for ci, cell in enumerate(cells) if cell in grid]

    if not constraints:
        cands = words_by_len[L]
    else:
        cands = None
        for ci, ch in constraints:
            matching = index.get((L, ci, ch), set())
            if cands is None:
                cands = set(matching)
            else:
                cands &= matching
            if not cands:
                return []

    return [w for w in cands if w not in used_words]

nodes = [0]

def backtrack(start_time):
    nodes[0] += 1
    if nodes[0] > 60000 or time.time() - start_time > 8:
        return False

    if all(a is not None for a in assigned):
        return True

    best_si = None
    best_cands = None
    best_count = 999999

    for si in range(len(slots)):
        if assigned[si] is None:
            cands = get_candidates(si)
            cnt = len(cands)
            if cnt == 0:
                return False
            if cnt < best_count:
                best_count = cnt
                best_si = si
                best_cands = cands
                if cnt == 1:
                    break

    slot = slots[best_si]
    cells = slot["cells"]

    cands_list = list(best_cands)
    random.shuffle(cands_list)

    for w in cands_list[:35]:
        prev = {cell: grid.get(cell) for cell in cells}
        for ci, cell in enumerate(cells):
            grid[cell] = w[ci]
        assigned[best_si] = w
        used_words.add(w)

        if backtrack(start_time):
            return True

        for cell, v in prev.items():
            if v is None:
                del grid[cell]
            else:
                grid[cell] = v
        assigned[best_si] = None
        used_words.remove(w)

    return False

print("Searching pure 100% authentic Portuguese solution...")
for attempt in range(50):
    nodes[0] = 0
    t0 = time.time()
    grid.clear()
    assigned = [None] * len(slots)
    used_words.clear()

    if backtrack(t0):
        print(f"\n=======================================================")
        print(f"BINGO! PURE PORTUGUESE 9x7 FOUND IN ATTEMPT {attempt+1} ({time.time() - t0:.2f}s, {nodes[0]} nodes)")
        print(f"=======================================================")
        for si, s in enumerate(slots):
            print(f"  {s['id']} ({s['dir']}): {assigned[si]} -> {word_display.get(assigned[si], assigned[si])}")
        print("\nGrid:")
        for r in range(1, 9):
            row_str = []
            for c in range(1, 7):
                if (r, c) in clue_set:
                    row_str.append("[ ]")
                else:
                    row_str.append(grid.get((r, c), "?"))
            print(f"R{r}: " + " ".join(row_str))

        # Save to json
        import json
        sol = {
            "clues": list(clue_set),
            "slots": [{"id": s["id"], "dir": s["dir"], "cells": s["cells"], "word": assigned[i], "display": word_display.get(assigned[i], assigned[i])} for i, s in enumerate(slots)],
            "grid": {f"{r},{c}": grid[(r, c)] for r in range(1, 9) for c in range(1, 7) if (r, c) not in clue_set}
        }
        with open("scripts/found_pure_pt_solution.json", "w", encoding="utf-8") as f:
            json.dump(sol, f, indent=2, ensure_ascii=False)
        sys.exit(0)
    else:
        print(f"Attempt {attempt+1} finished in {time.time() - t0:.2f}s ({nodes[0]} nodes)")
