import unicodedata
from collections import defaultdict
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words
common_words = defaultdict(set)
common_display = {}
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            disp = parts[1] if len(parts) > 1 else parts[0]
            if w.isalpha():
                common_words[len(w)].add(w)
                if w not in common_display:
                    common_display[w] = disp

full_words = defaultdict(set)
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        w = strip_accents(line.strip())
        if w.isalpha():
            full_words[len(w)].add(w)

USED_WORDS = {
    'RAPOSA', 'IMOVEL', 'SA', 'ARI', 'ADA', 'ME', 'DORIAN', 'ASTROS',
    'RISADA', 'AMADOS', 'PO', 'ART', 'OVA', 'IR', 'SERMAO', 'ALIENS',
    'CUSTAS', 'ANTIGA', 'SI', 'ACE', 'AM', 'CASADO', 'OSTRAS',
    'CASACO', 'UNICAS', 'ST', 'EST', 'TIA', 'AR', 'AGRADA', 'SAIMOS',
    'BRASIL', 'EURICO', 'LE', 'MAR', 'MIM', 'ARATUS', 'ZORAIA',
    'BELMAZ', 'RUEIRO', 'SIM', 'TA', 'ICAPUI', 'LOROSA'
}

for uw in USED_WORDS:
    for d in (common_words, full_words):
        for l in d:
            d[l].discard(uw)

good_2 = {"AR", "IR", "VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "LE", "PE", "PA", "PO", "DO", "RE", "MI", "FA", "SI", "TI", "EU", "AI", "OI", "RA", "MA", "VA", "TA", "VE", "CA", "TU", "NE", "TO", "FE", "LI", "AO"} - USED_WORDS
good_3 = {"SOL", "LUA", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "DAS", "DOS", "LHE", "VAO"} - USED_WORDS

common_words[2] = good_2
common_words[3] = common_words[3].intersection(good_3) | good_3

# Indexed vocabulary: (length, pos, char) -> set of words
word_dict_by_len = {}
for l in range(2, 9):
    # Prioritize common words, fallback to full_words for len 8
    ws = set(common_words[l])
    if l == 8 or len(ws) < 100:
        ws |= full_words[l]
    word_dict_by_len[l] = ws

index = defaultdict(set)
for l, ws in word_dict_by_len.items():
    for w in ws:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

print("Index built.")

def solve_layout(interior_clues_list, name=""):
    clue_set = set(interior_clues_list)
    
    # Across slots
    across_slots = []
    for r in range(1, 9):
        c = 1
        while c <= 6:
            if (r, c) not in clue_set:
                start_c = c
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
                start_r = r
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

    # Sort slots: short slots first, or most intersecting slots first
    # Cell to slots
    cell_to_slots = defaultdict(list)
    for si, s in enumerate(all_slots):
        for ci, cell in enumerate(s["cells"]):
            cell_to_slots[cell].append((si, ci))

    # Fast solver state
    grid = {}
    assigned = [None] * len(all_slots)
    used_words = set()

    def get_candidates(si):
        slot = all_slots[si]
        cells = slot["cells"]
        L = len(cells)
        # Check pattern
        constraints = []
        for ci, cell in enumerate(cells):
            if cell in grid:
                constraints.append((ci, grid[cell]))

        if not constraints:
            cands = word_dict_by_len[L]
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
        if nodes[0] > 100000:
            return False # timeout for this layout
        if time.time() - start_time > 8:
            return False

        if all(a is not None for a in assigned):
            return True

        # Pick slot with MRV
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

        # Sort candidates to prefer common words
        sorted_cands = sorted(best_cands, key=lambda w: (0 if w in common_words[len(w)] else 1))

        for w in sorted_cands[:40]:
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

    print(f"\n--- Solving {name} (Clues: {interior_clues_list}) ---")
    if backtrack():
        print(f"SUCCESS in {time.time() - start_time:.2f}s ({nodes[0]} nodes)!")
        for si, s in enumerate(all_slots):
            print(f"  {s['id']} ({s['dir']}): {assigned[si]}")
        print("Grid:")
        for r in range(1, 9):
            row_str = []
            for c in range(1, 7):
                if (r, c) in clue_set:
                    row_str.append("[ ]")
                else:
                    row_str.append(grid.get((r, c), "?"))
            print(f"R{r}: " + " ".join(row_str))
        return grid, all_slots, assigned
    else:
        print(f"Failed or timed out after {time.time() - start_time:.2f}s ({nodes[0]} nodes)")
        return None

# Try different layouts
layouts = [
    ([(4, 3), (5, 4)], "Layout 1"),
    ([(4, 4), (5, 3)], "Layout 2"),
    ([(3, 3), (6, 4)], "Layout 3"),
    ([(3, 4), (6, 3)], "Layout 4"),
    ([(3, 3), (4, 4), (6, 3)], "Layout 5"),
    ([(3, 4), (5, 3), (6, 4)], "Layout 6"),
]

for clues, name in layouts:
    res = solve_layout(clues, name)
    if res:
        print("\nFOUND SOLUTION!")
        break
