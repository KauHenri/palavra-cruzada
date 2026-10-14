import sys
import unicodedata
from collections import defaultdict
import random
import time
import json

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

# 1. Full standard PT dictionary
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

# 2. Top 50k words
w50 = set()
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            if w.isalpha():
                w50.add(w)

good_2 = {"VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "PE", "PA", "DO", "RE", "MI", "FA", "TI", "EU", "AI", "OI", "RA", "MA", "VA", "VE", "CA", "TU", "NE", "TO", "FE", "LI", "AO"} - USED_WORDS
good_3 = {"SOL", "LUA", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "DAS", "DOS", "LHE", "VAO"} - USED_WORDS

clean_vocab = (w50 & pt_dict) - USED_WORDS

# Exclude foreign words if any
foreign_blacklist = {"DICK", "FUCK", "SHIT", "VAGINA", "PENIS", "COCK", "BITCH", "CORNO", "STAN", "CHET", "HORACE", "CHAD", "HOME", "NERO", "ERIC", "DAMIEN", "ALAN"}
clean_vocab -= foreign_blacklist

words_by_len = defaultdict(list)
word_display = {}

for w in clean_vocab:
    l = len(w)
    if l == 2 and w in good_2:
        words_by_len[2].append(w)
        word_display[w] = pt_display.get(w, w)
    elif l == 3 and w in good_3:
        words_by_len[3].append(w)
        word_display[w] = pt_display.get(w, w)
    elif l in (4, 5, 6, 8):
        words_by_len[l].append(w)
        word_display[w] = pt_display.get(w, w)

print(f"Top 50k PT Vocab: 2:{len(words_by_len[2])}, 3:{len(words_by_len[3])}, 4:{len(words_by_len[4])}, 5:{len(words_by_len[5])}, 6:{len(words_by_len[6])}, 8:{len(words_by_len[8])}", flush=True)

index = defaultdict(set)
for l in words_by_len:
    for w in words_by_len[l]:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

masks = [
    ([(4, 1), (4, 2), (5, 5), (5, 6)], "Pinwheel 1"),
    ([(5, 1), (5, 2), (4, 5), (4, 6)], "Pinwheel 2"),
    ([(3, 3), (4, 4), (6, 3)], "Ladder 1"),
    ([(3, 4), (5, 3), (6, 4)], "Ladder 2"),
    ([(3, 3), (5, 4), (6, 4)], "Ladder 3"),
    ([(3, 4), (4, 4), (6, 3)], "Ladder 4"),
    ([(3, 3), (4, 3), (5, 4), (6, 4)], "Ladder 4-clue A"),
    ([(3, 4), (4, 4), (5, 3), (6, 3)], "Ladder 4-clue B"),
]

def build_slots(clue_comb):
    clue_set = set(clue_comb)
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
    return all_slots, clue_set

total_start = time.time()
print("Starting search with Top 50k authentic Portuguese...", flush=True)

solutions_found = []
for attempt in range(1, 401):
    for clue_comb, mask_name in masks:
        slots, clue_set = build_slots(clue_comb)
        grid = {}
        assigned = [None] * len(slots)
        used_words = set()

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
            return [w for w in cands if w not in used_words]

        nodes = [0]
        t0 = time.time()

        def backtrack():
            nodes[0] += 1
            if nodes[0] > 1800 or time.time() - t0 > 0.45:
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
                used_words.add(w)

                if backtrack():
                    return True

                for cell, v in prev.items():
                    if v is None:
                        del grid[cell]
                    else:
                        grid[cell] = v
                assigned[best_si] = None
                used_words.discard(w)

            return False

        if backtrack():
            print("\n" + "="*60, flush=True)
            print(f"CANDIDATE in {mask_name} (attempt {attempt}, {time.time() - total_start:.2f}s)!", flush=True)
            print("="*60, flush=True)
            words_collected = []
            for si, s in enumerate(slots):
                w = assigned[si]
                disp = word_display.get(w, w)
                words_collected.append(disp)
                print(f"  {s['id']} ({s['dir']}): {w} -> {disp}", flush=True)

            print("\nGrid:", flush=True)
            for r in range(1, 9):
                row_str = []
                for c in range(1, 7):
                    if (r, c) in clue_set:
                        row_str.append("[ ]")
                    else:
                        row_str.append(grid.get((r, c), "?"))
                print(f"R{r}: " + " ".join(row_str), flush=True)

            solutions_found.append({
                "mask_name": mask_name,
                "clues": list(clue_set),
                "slots": [{"id": s["id"], "dir": s["dir"], "cells": s["cells"], "word": assigned[i], "display": word_display.get(assigned[i], assigned[i])} for i, s in enumerate(slots)],
                "grid": {f"{r},{c}": grid[(r, c)] for r in range(1, 9) for c in range(1, 7) if (r, c) not in clue_set}
            })
            if len(solutions_found) >= 5:
                with open("scripts/found_top50k_candidates.json", "w", encoding="utf-8") as f:
                    json.dump(solutions_found, f, indent=2, ensure_ascii=False)
                sys.exit(0)

    if attempt % 5 == 0:
        print(f"Completed {attempt} attempts in {time.time() - total_start:.2f}s...", flush=True)

print("Search finished without solution.", flush=True)
