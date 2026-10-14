import unicodedata
from collections import defaultdict
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words
common_words = defaultdict(set)
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            if w.isalpha():
                common_words[len(w)].add(w)

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

# Allow words that are either in common_words or high quality
valid_words_by_len = {}
for l in range(2, 9):
    # for len 6 and 8, common words first, but full_words if needed
    valid_words_by_len[l] = common_words[l] if len(common_words[l]) > 100 else (common_words[l] | full_words[l])

print("Setting up CSP solver for Mask 1...")

# Grid coordinates: (r, c) for r in 1..8, c in 1..6
# Clues at (4, 3) and (5, 4)
interior_clues = {(4, 3), (5, 4)}

slots = [
    # Across
    {"id": "A1", "dir": "A", "cells": [(1, c) for c in range(1, 7)]},
    {"id": "A2", "dir": "A", "cells": [(2, c) for c in range(1, 7)]},
    {"id": "A3", "dir": "A", "cells": [(3, c) for c in range(1, 7)]},
    {"id": "A4_1", "dir": "A", "cells": [(4, 1), (4, 2)]},
    {"id": "A4_2", "dir": "A", "cells": [(4, 4), (4, 5), (4, 6)]},
    {"id": "A5_1", "dir": "A", "cells": [(5, 1), (5, 2), (5, 3)]},
    {"id": "A5_2", "dir": "A", "cells": [(5, 5), (5, 6)]},
    {"id": "A6", "dir": "A", "cells": [(6, c) for c in range(1, 7)]},
    {"id": "A7", "dir": "A", "cells": [(7, c) for c in range(1, 7)]},
    {"id": "A8", "dir": "A", "cells": [(8, c) for c in range(1, 7)]},

    # Down
    {"id": "D1", "dir": "D", "cells": [(r, 1) for r in range(1, 9)]},
    {"id": "D2", "dir": "D", "cells": [(r, 2) for r in range(1, 9)]},
    {"id": "D3_1", "dir": "D", "cells": [(1, 3), (2, 3), (3, 3)]},
    {"id": "D3_2", "dir": "D", "cells": [(5, 3), (6, 3), (7, 3), (8, 3)]},
    {"id": "D4_1", "dir": "D", "cells": [(1, 4), (2, 4), (3, 4), (4, 4)]},
    {"id": "D4_2", "dir": "D", "cells": [(6, 4), (7, 4), (8, 4)]},
    {"id": "D5", "dir": "D", "cells": [(r, 5) for r in range(1, 9)]},
    {"id": "D6", "dir": "D", "cells": [(r, 6) for r in range(1, 9)]},
]

# Map cell to slot indices
cell_to_slots = defaultdict(list)
for slot_idx, slot in enumerate(slots):
    for cell_idx, cell in enumerate(slot["cells"]):
        cell_to_slots[cell].append((slot_idx, cell_idx))

print("Total slots:", len(slots))

# Pre-filter candidate lists for each slot
slot_domains = []
for slot in slots:
    l = len(slot["cells"])
    candidates = list(valid_words_by_len[l])
    random.shuffle(candidates)
    slot_domains.append(candidates)

def solve():
    # Grid state: (r, c) -> char
    grid = {}
    assigned_words = [None] * len(slots)
    used_words_in_solution = set()

    def get_slot_candidates(slot_idx):
        slot = slots[slot_idx]
        cells = slot["cells"]
        pattern = []
        for cell in cells:
            pattern.append(grid.get(cell, None))
        
        candidates = []
        for w in slot_domains[slot_idx]:
            if w in used_words_in_solution:
                continue
            match = True
            for i, ch in enumerate(pattern):
                if ch is not None and w[i] != ch:
                    match = False
                    break
            if match:
                candidates.append(w)
        return candidates

    def backtrack():
        if all(assigned_words[i] is not None for i in range(len(slots))):
            return True

        # MRV: Choose unassigned slot with fewest candidates
        best_slot_idx = None
        best_candidates = None
        min_candidates_count = float('inf')

        for i in range(len(slots)):
            if assigned_words[i] is None:
                cands = get_slot_candidates(i)
                if len(cands) == 0:
                    return False  # Dead end!
                if len(cands) < min_candidates_count:
                    min_candidates_count = len(cands)
                    best_slot_idx = i
                    best_candidates = cands
                    if min_candidates_count == 1:
                        break # Can't get smaller than 1

        slot = slots[best_slot_idx]
        cells = slot["cells"]

        # Try candidates (prioritize common words if candidate list is large)
        # Limit branching to top 50 to keep search fast
        for word in best_candidates[:50]:
            # Save cell states to undo later
            prev_cells = {cell: grid.get(cell) for cell in cells}

            # Assign
            for i, cell in enumerate(cells):
                grid[cell] = word[i]
            assigned_words[best_slot_idx] = word
            used_words_in_solution.add(word)

            if backtrack():
                return True

            # Undo
            for cell, prev_val in prev_cells.items():
                if prev_val is None:
                    del grid[cell]
                else:
                    grid[cell] = prev_val
            assigned_words[best_slot_idx] = None
            used_words_in_solution.remove(word)

        return False

    start_time = time.time()
    print("Starting backtrack...")
    if backtrack():
        print(f"Solved in {time.time() - start_time:.2f}s!")
        for i, slot in enumerate(slots):
            print(f"{slot['id']} ({slot['dir']}): {assigned_words[i]}")
        print("\nGrid:")
        for r in range(1, 9):
            row_str = []
            for c in range(1, 7):
                if (r, c) in interior_clues:
                    row_str.append("[CLUE]")
                else:
                    row_str.append(grid.get((r, c), "?"))
            print(f"Row {r}: " + " ".join(row_str))
        return grid, assigned_words
    else:
        print("No solution found.")
        return None

solve()
