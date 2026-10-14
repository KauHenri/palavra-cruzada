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

# Strict common for short words (2, 3, 4)
good_2 = {"VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "PE", "PA", "DO", "RE", "MI", "FA", "TI", "EU", "AI", "OI", "RA", "MA", "VA", "VE", "CA", "TU", "NE", "TO", "FE", "LI", "AO"} - USED_WORDS
good_3 = {"SOL", "LUA", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "DAS", "DOS", "LHE", "VAO"} - USED_WORDS

# Load words
words_by_len = defaultdict(set)
word_display = {}

# 1. From top common clean
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            disp = parts[1] if len(parts) > 1 else parts[0]
            if w.isalpha() and w not in USED_WORDS:
                words_by_len[len(w)].add(w)
                if w not in word_display:
                    word_display[w] = disp

# Set short words to pure everyday vocabulary
words_by_len[2] = good_2
words_by_len[3] = words_by_len[3].intersection(good_3) | good_3

# 2. For len 6 and 8, also allow clean words from palavras_full
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        raw = line.strip()
        w = strip_accents(raw)
        if w.isalpha() and w not in USED_WORDS:
            if len(w) in (4, 5, 6, 8):
                # only add if reasonable length and not obscure
                if len(w) == 8 or len(w) == 6:
                    words_by_len[len(w)].add(w)
                    if w not in word_display:
                        word_display[w] = raw.upper()

print("Vocabulary sizes:")
for l in range(2, 9):
    print(f"Len {l}: {len(words_by_len[l])} words")

print("Building index...", flush=True)
index = defaultdict(set)
for l in range(2, 9):
    for w in words_by_len[l]:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

print("Index ready!", flush=True)

def solve_layout(interior_clues_list, name=""):
    clue_set = set(interior_clues_list)
    
    # Across slots
    across_slots = []
    for r in range(1, 9):
        c = 1
        while c <= 6:
            if (r, c) not in clue_set:
                cells = []
                while c <= 6 and (r, c) not in clue_set:
                    cells.append((r, c))
                    c += 1
                across_slots.append(cells)
            else:
                c += 1

    # Down slots
    down_slots = []
    for c in range(1, 7):
        r = 1
        while r <= 8:
            if (r, c) not in clue_set:
                cells = []
                while r <= 8 and (r, c) not in clue_set:
                    cells.append((r, c))
                    r += 1
                down_slots.append(cells)
            else:
                r += 1

    all_slots = []
    for i, s in enumerate(across_slots):
        all_slots.append({"id": f"A{i+1}", "dir": "A", "cells": s})
    for i, s in enumerate(down_slots):
        all_slots.append({"id": f"D{i+1}", "dir": "D", "cells": s})

    grid = {}
    assigned = [None] * len(all_slots)
    used_words = set()

    def get_candidates(si):
        slot = all_slots[si]
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

    start_time = time.time()
    nodes = [0]

    def backtrack():
        nodes[0] += 1
        if nodes[0] > 50000 or time.time() - start_time > 10:
            return False

        if all(a is not None for a in assigned):
            return True

        best_si = None
        best_cands = None
        best_count = 999999

        for si in range(len(all_slots)):
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

        slot = all_slots[best_si]
        cells = slot["cells"]

        cands_list = list(best_cands)
        random.shuffle(cands_list)

        for w in cands_list[:30]:
            prev = {cell: grid.get(cell) for cell in cells}
            for ci, cell in enumerate(cells):
                grid[cell] = w[ci]
            assigned[best_si] = w
            used_words.add(w)

            if backtrack():
                return True

            for cell, v in prev.items():
                if v is None:
                    del grid[cell]
                else:
                    grid[cell] = v
            assigned[best_si] = None
            used_words.remove(w)

        return False

    print(f"Testing {name}...", flush=True)
    if backtrack():
        print(f"SUCCESS in {time.time() - start_time:.2f}s ({nodes[0]} nodes)!", flush=True)
        for si, s in enumerate(all_slots):
            print(f"  {s['id']} ({s['dir']}): {assigned[si]} ({word_display.get(assigned[si], assigned[si])})", flush=True)
        print("Grid:", flush=True)
        for r in range(1, 9):
            row_str = []
            for c in range(1, 7):
                if (r, c) in clue_set:
                    row_str.append("[ ]")
                else:
                    row_str.append(grid.get((r, c), "?"))
            print(f"R{r}: " + " ".join(row_str), flush=True)
        return grid, all_slots, assigned, clue_set
    else:
        print(f"No solution in {time.time() - start_time:.2f}s ({nodes[0]} nodes)", flush=True)
        return None

# Candidates to try
test_layouts = [
    ([(3, 3), (4, 4), (6, 3)], "Layout A: (3,3), (4,4), (6,3)"),
    ([(3, 4), (5, 3), (6, 4)], "Layout B: (3,4), (5,3), (6,4)"),
    ([(3, 3), (5, 4), (6, 4)], "Layout C: (3,3), (5,4), (6,4)"),
    ([(3, 4), (4, 4), (6, 3)], "Layout D: (3,4), (4,4), (6,3)"),
    ([(3, 3), (4, 3), (5, 4), (6, 4)], "Layout E: (3,3), (4,3), (5,4), (6,4)"),
    ([(4, 3), (5, 4)], "Layout F: (4,3), (5,4)"),
    ([(4, 4), (5, 3)], "Layout G: (4,4), (5,3)"),
]

for attempt in range(5):
    print(f"\n=== ATTEMPT {attempt+1} ===", flush=True)
    for clues, name in test_layouts:
        res = solve_layout(clues, name)
        if res:
            print("\n!!! JACKPOT FOUND SOLUTION !!!", flush=True)
            import json
            grid, all_slots, assigned, clue_set = res
            sol_data = {
                "interior_clues": list(clues),
                "slots": [{"id": s["id"], "dir": s["dir"], "cells": s["cells"], "word": assigned[i], "display": word_display.get(assigned[i], assigned[i])} for i, s in enumerate(all_slots)],
                "grid": {f"{r},{c}": grid.get((r, c), "") for r in range(1, 9) for c in range(1, 7)}
            }
            with open("scripts/found_9x7_solution.json", "w", encoding="utf-8") as f:
                json.dump(sol_data, f, indent=2, ensure_ascii=False)
            sys.exit(0)
