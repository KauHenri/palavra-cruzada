import unicodedata
from collections import defaultdict
import random
import time
import json

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load standard PT dictionary
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

# Load top common clean words
word_freq = defaultdict(int)
proper_names = set()
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            w = strip_accents(parts[0])
            disp = parts[1]
            if disp[0].isupper():
                proper_names.add(w)
            if len(parts) >= 3:
                try:
                    word_freq[w] = max(word_freq[w], int(parts[2]))
                except:
                    pass

# Load top 50k
w50 = set()
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            if w.isalpha():
                w50.add(w)

# Explicit blacklist of foreign, weird, slang, or offensive
forbidden = {
    "DICK", "FUCK", "SHIT", "VAGINA", "PENIS", "COCK", "BITCH", "CORNO",
    "STAN", "CHET", "HORACE", "CHAD", "HOME", "NERO", "ERIC", "DAMIEN", "ALAN",
    "IVES", "LAOS", "ELISSA", "MARISA", "MARIACHI", "SECTOR", "OLOFRO", "MEBOSA",
    "AMAL", "TAMA", "CAMADA", "AMADAS", "MICADO", "ROBE", "UNOS", "ARSENICO",
    "ZELOSO", "LOIROS", "LOIRAS", "LEAR", "ELAINE", "NAPIER", "MADI",
    "SA", "ADA", "ART", "ALIENS", "DORIAN", "VINTAGE", "ACE", "ST", "EST",
    "BELMAZ", "ZORAIA", "RUEIRO", "LOROSA", "ARATUS", "ICAPUI", "ASIM", "NAOS",
    "VECTOR", "TOTO", "ARGO", "RAMONA", "OTAN", "JIRO", "ANAS", "MAMILO",
    "SOIOTO", "ERGUER", "MADRIA", "AMICAL", "MATESE", "ARARAI", "IGDLOITA",
    "OURESCER", "BENJAMIN", "CAMARA", "ALOMORFO", "ESTEREIS", "HALL", "DALE",
    "LIONEL", "DUMA", "ME", "ARI"
}

# Ultra-clean 2-letter words (familiar Portuguese only!)
clean_2 = {"AR", "IR", "PA", "PE", "PO", "LA", "FE", "NO", "NA", "DO", "DA", "DE", "EM", "UM", "SE", "OU", "JA", "HA", "SO", "RE", "MI", "FA", "TI", "EU", "TU", "VA", "VE", "CA", "TO", "LI", "AO"} - forbidden

# Ultra-clean 3-letter words
clean_3 = {"SOL", "LUA", "MAR", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "DAS", "DOS", "LHE", "VAO"} - forbidden

pure_vocab = (w50 & pt_dict) - proper_names - forbidden

words_by_len = defaultdict(list)
for w in pure_vocab:
    l = len(w)
    if l == 2 and w in clean_2:
        words_by_len[2].append(w)
    elif l == 3 and w in clean_3:
        words_by_len[3].append(w)
    elif l in (4, 5, 6, 8) and word_freq[w] >= 50:
        words_by_len[l].append(w)

index = defaultdict(set)
for l in words_by_len:
    for w in words_by_len[l]:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

print(f"Loaded clean index: 2:{len(words_by_len[2])}, 3:{len(words_by_len[3])}, 4:{len(words_by_len[4])}, 5:{len(words_by_len[5])}, 6:{len(words_by_len[6])}, 8:{len(words_by_len[8])}")

# Function to solve 7x7 grid
# Row 3: A3_1 (len 2) cols 1..2, clue at (3,3), A3_2 (len 3) cols 4..6
# Row 4: A4_1 (len 3) cols 1..3, clue at (4,4), A4_2 (len 2) cols 5..6
# Col 3: D3_1 (len 2) rows 1..2, clue at (3,3), D3_2 (len 3) rows 4..6
# Col 4: D4_1 (len 3) rows 1..3, clue at (4,4), D4_2 (len 2) rows 5..6
def solve_7x7(used_game_words, seed_word=None):
    slots = [
        {"id": "R1", "dir": "A", "cells": [(1, c) for c in range(1, 7)]},
        {"id": "R2", "dir": "A", "cells": [(2, c) for c in range(1, 7)]},
        {"id": "A3_1", "dir": "A", "cells": [(3, 1), (3, 2)]},
        {"id": "A3_2", "dir": "A", "cells": [(3, 4), (3, 5), (3, 6)]},
        {"id": "A4_1", "dir": "A", "cells": [(4, 1), (4, 2), (4, 3)]},
        {"id": "A4_2", "dir": "A", "cells": [(4, 5), (4, 6)]},
        {"id": "R5", "dir": "A", "cells": [(5, c) for c in range(1, 7)]},
        {"id": "R6", "dir": "A", "cells": [(6, c) for c in range(1, 7)]},

        {"id": "C1", "dir": "D", "cells": [(r, 1) for r in range(1, 7)]},
        {"id": "C2", "dir": "D", "cells": [(r, 2) for r in range(1, 7)]},
        {"id": "D3_1", "dir": "D", "cells": [(1, 3), (2, 3)]},
        {"id": "D3_2", "dir": "D", "cells": [(4, 3), (5, 3), (6, 3)]},
        {"id": "D4_1", "dir": "D", "cells": [(1, 4), (2, 4), (3, 4)]},
        {"id": "D4_2", "dir": "D", "cells": [(5, 4), (6, 4)]},
        {"id": "C5", "dir": "D", "cells": [(r, 5) for r in range(1, 7)]},
        {"id": "C6", "dir": "D", "cells": [(r, 6) for r in range(1, 7)]},
    ]

    for attempt in range(100):
        grid = {}
        assigned = [None] * len(slots)
        local_used = set(used_game_words)

        def get_cands(si):
            slot = slots[si]
            cells = slot["cells"]
            L = len(cells)
            constraints = [(ci, grid[cell]) for ci, cell in enumerate(cells) if cell in grid]
            if not constraints:
                return words_by_len[L]
            cands = None
            for ci, ch in constraints:
                matching = index.get((L, ci, ch), set())
                if cands is None:
                    cands = set(matching)
                else:
                    cands &= matching
                if not cands:
                    return []
            return [w for w in cands if w not in local_used]

        t0 = time.time()
        nodes = [0]

        def backtrack():
            nodes[0] += 1
            if nodes[0] > 1200 or time.time() - t0 > 0.35:
                return False
            if all(a is not None for a in assigned):
                return True

            best_si = None
            best_cands = None
            best_count = 999999

            for si in range(len(slots)):
                if assigned[si] is None:
                    cands = get_cands(si)
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

            for w in cands_list[:25]:
                prev = {cell: grid.get(cell) for cell in cells}
                for ci, cell in enumerate(cells):
                    grid[cell] = w[ci]
                assigned[best_si] = w
                local_used.add(w)

                if backtrack():
                    return True

                for cell, v in prev.items():
                    if v is None:
                        del grid[cell]
                    else:
                        grid[cell] = v
                assigned[best_si] = None
                local_used.discard(w)

            return False

        if backtrack():
            words_dict = {slots[i]["id"]: assigned[i] for i in range(len(slots))}
            return grid, words_dict, set(assigned)

    return None

print("Testing 7x7 generator...")
t0 = time.time()
sol = solve_7x7(set())
if sol:
    grid, words_dict, words_set = sol
    print(f"Solved 7x7 in {time.time() - t0:.2f}s!")
    for k, v in words_dict.items():
        print(f"  {k}: {v} ({pt_display.get(v, v)})")
