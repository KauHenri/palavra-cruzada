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

words_by_len[2] = good_2
words_by_len[3] = words_by_len[3].intersection(good_3) | good_3

# Also add high quality 6 and 8 from full
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        raw = line.strip()
        w = strip_accents(raw)
        if w.isalpha() and w not in USED_WORDS:
            if len(w) in (6, 8):
                words_by_len[len(w)].add(w)
                if w not in word_display:
                    word_display[w] = raw.upper()

# Index for fast lookup: (len, pos, char) -> set of words
index = defaultdict(set)
for l in range(2, 9):
    for w in words_by_len[l]:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

print("Index ready. 8-letter words:", len(words_by_len[8]), "6-letter words:", len(words_by_len[6]))

# Test mask:
# Clues at (3, 3) and (6, 4)
# Let's see:
# Across slots:
# R1: (1, 1..6) len 6
# R2: (2, 1..6) len 6
# R3: (3, 1..2) len 2; (3, 4..6) len 3
# R4: (4, 1..6) len 6
# R5: (5, 1..6) len 6
# R6: (6, 1..3) len 3; (6, 5..6) len 2
# R7: (7, 1..6) len 6
# R8: (8, 1..6) len 6
# Down slots:
# C1: (1..8, 1) len 8
# C2: (1..8, 2) len 8
# C3: (1..2, 3) len 2; (4..8, 3) len 5
# C4: (1..5, 4) len 5; (7..8, 4) len 2
# C5: (1..8, 5) len 8
# C6: (1..8, 6) len 8

def search_solutions(limit=3):
    # Pick common words for C1 and C6
    # Prioritize words from top_common_clean for C1 and C6
    with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
        common_8 = [strip_accents(line.strip().split()[0]) for line in f if len(strip_accents(line.strip().split()[0])) == 8 and strip_accents(line.strip().split()[0]) in words_by_len[8]]
        common_6 = [strip_accents(line.strip().split()[0]) for line in f if len(strip_accents(line.strip().split()[0])) == 6 and strip_accents(line.strip().split()[0]) in words_by_len[6]]

    random.shuffle(common_8)
    random.shuffle(common_6)

    print(f"Loaded {len(common_8)} common 8-letter words and {len(common_6)} common 6-letter words.")

    count = 0
    start_time = time.time()

    for c1 in common_8[:200]:
        for c6 in common_8[:200]:
            if c1 == c6: continue

            # R1 connects c1[0] and c6[0]
            r1_cands = index.get((6, 0, c1[0]), set()) & index.get((6, 5, c6[0]), set())
            if not r1_cands: continue

            # R8 connects c1[7] and c6[7]
            r8_cands = index.get((6, 0, c1[7]), set()) & index.get((6, 5, c6[7]), set())
            if not r8_cands: continue

            for r1 in list(r1_cands)[:5]:
                for r8 in list(r8_cands)[:5]:
                    if len({c1, c6, r1, r8}) < 4: continue

                    # Now C2 must match: C2[0] == r1[1] and C2[7] == r8[1]
                    c2_cands = index.get((8, 0, r1[1]), set()) & index.get((8, 7, r8[1]), set())
                    if not c2_cands: continue

                    # C5 must match: C5[0] == r1[4] and C5[7] == r8[4]
                    c5_cands = index.get((8, 0, r1[4]), set()) & index.get((8, 7, r8[4]), set())
                    if not c5_cands: continue

                    for c2 in list(c2_cands)[:3]:
                        for c5 in list(c5_cands)[:3]:
                            if len({c1, c6, r1, r8, c2, c5}) < 6: continue

                            # Check R2: R2[0]=c1[1], R2[1]=c2[1], R2[4]=c5[1], R2[5]=c6[1]
                            r2_cands = index.get((6, 0, c1[1]), set()) & index.get((6, 1, c2[1]), set()) & index.get((6, 4, c5[1]), set()) & index.get((6, 5, c6[1]), set())
                            if not r2_cands: continue

                            # Check R7: R7[0]=c1[6], R7[1]=c2[6], R7[4]=c5[6], R7[5]=c6[6]
                            r7_cands = index.get((6, 0, c1[6]), set()) & index.get((6, 1, c2[6]), set()) & index.get((6, 4, c5[6]), set()) & index.get((6, 5, c6[6]), set())
                            if not r7_cands: continue

                            for r2 in list(r2_cands)[:3]:
                                for r7 in list(r7_cands)[:3]:
                                    if len({c1, c6, r1, r8, c2, c5, r2, r7}) < 8: continue

                                    # Check C3_top (len 2): C3[0]=r1[2], C3[1]=r2[2]
                                    d3_1 = r1[2] + r2[2]
                                    if d3_1 not in words_by_len[2]: continue

                                    # Check C4_bot (len 2): C4[0]=r7[3], C4[1]=r8[3]
                                    d4_2 = r7[3] + r8[3]
                                    if d4_2 not in words_by_len[2]: continue

                                    # Now check middle rows R3, R4, R5, R6
                                    # R3: A3_1 (len 2) = c1[2] + c2[2]
                                    a3_1 = c1[2] + c2[2]
                                    if a3_1 not in words_by_len[2]: continue

                                    # R6: A6_2 (len 2) = c5[5] + c6[5]
                                    a6_2 = c5[5] + c6[5]
                                    if a6_2 not in words_by_len[2]: continue

                                    # R4: R4[0]=c1[3], R4[1]=c2[3], R4[4]=c5[3], R4[5]=c6[3]
                                    r4_cands = index.get((6, 0, c1[3]), set()) & index.get((6, 1, c2[3]), set()) & index.get((6, 4, c5[3]), set()) & index.get((6, 5, c6[3]), set())
                                    if not r4_cands: continue

                                    # R5: R5[0]=c1[4], R5[1]=c2[4], R5[4]=c5[4], R5[5]=c6[4]
                                    r5_cands = index.get((6, 0, c1[4]), set()) & index.get((6, 1, c2[4]), set()) & index.get((6, 4, c5[4]), set()) & index.get((6, 5, c6[4]), set())
                                    if not r5_cands: continue

                                    for r4 in list(r4_cands)[:3]:
                                        for r5 in list(r5_cands)[:3]:
                                            # Now C4_top (len 5): r1[3] + r2[3] + (char at r3[3]?? wait, r3 col 4 is start of A3_2!)
                                            # In col 4: row 1 is r1[3], row 2 is r2[3]. Row 3 is A3_2[0]. Row 4 is r4[3]. Row 5 is r5[3]!
                                            # So C4_top (len 5) has: [0]=r1[3], [1]=r2[3], [3]=r4[3], [4]=r5[3]
                                            c4_top_cands = index.get((5, 0, r1[3]), set()) & index.get((5, 1, r2[3]), set()) & index.get((5, 3, r4[3]), set()) & index.get((5, 4, r5[3]), set())
                                            if not c4_top_cands: continue

                                            for c4_top in list(c4_top_cands)[:3]:
                                                # char at (3, 4) is c4_top[2]
                                                # So A3_2 (len 3) has: [0]=c4_top[2], [1]=c5[2], [2]=c6[2]
                                                a3_2 = c4_top[2] + c5[2] + c6[2]
                                                if a3_2 not in words_by_len[3]: continue

                                                # Now C3_bot (len 5): rows 4..8 col 3:
                                                # [0]=r4[2], [1]=r5[2], row 6 is A6_1[2], [3]=r7[2], [4]=r8[2]
                                                c3_bot_cands = index.get((5, 0, r4[2]), set()) & index.get((5, 1, r5[2]), set()) & index.get((5, 3, r7[2]), set()) & index.get((5, 4, r8[2]), set())
                                                if not c3_bot_cands: continue

                                                for c3_bot in list(c3_bot_cands)[:3]:
                                                    # char at (6, 3) is c3_bot[2]
                                                    # So A6_1 (len 3) has: [0]=c1[5], [1]=c2[5], [2]=c3_bot[2]
                                                    a6_1 = c1[5] + c2[5] + c3_bot[2]
                                                    if a6_1 not in words_by_len[3]: continue

                                                    all_words = {c1, c6, r1, r8, c2, c5, r2, r7, d3_1, d4_2, a3_1, a6_2, r4, r5, c4_top, a3_2, c3_bot, a6_1}
                                                    if len(all_words) != 18: continue

                                                    print("\n" + "="*50)
                                                    print(f"FOUND 100% VALID 9x7 LEVEL in {time.time() - start_time:.2f}s!")
                                                    print("="*50)
                                                    print(f"R1: {r1} ({word_display.get(r1, r1)})")
                                                    print(f"R2: {r2} ({word_display.get(r2, r2)})")
                                                    print(f"R3: {a3_1} + [CLUE] + {a3_2}")
                                                    print(f"R4: {r4} ({word_display.get(r4, r4)})")
                                                    print(f"R5: {r5} ({word_display.get(r5, r5)})")
                                                    print(f"R6: {a6_1} + [CLUE] + {a6_2}")
                                                    print(f"R7: {r7} ({word_display.get(r7, r7)})")
                                                    print(f"R8: {r8} ({word_display.get(r8, r8)})")
                                                    print(f"C1: {c1} ({word_display.get(c1, c1)})")
                                                    print(f"C2: {c2} ({word_display.get(c2, c2)})")
                                                    print(f"C3: {d3_1} + [CLUE] + {c3_bot}")
                                                    print(f"C4: {c4_top} + [CLUE] + {d4_2}")
                                                    print(f"C5: {c5} ({word_display.get(c5, c5)})")
                                                    print(f"C6: {c6} ({word_display.get(c6, c6)})")

                                                    # Return solution dict
                                                    return {
                                                        "c1": c1, "c2": c2, "c3_bot": c3_bot, "c4_top": c4_top, "c5": c5, "c6": c6,
                                                        "d3_1": d3_1, "d4_2": d4_2,
                                                        "r1": r1, "r2": r2, "r4": r4, "r5": r5, "r7": r7, "r8": r8,
                                                        "a3_1": a3_1, "a3_2": a3_2, "a6_1": a6_1, "a6_2": a6_2,
                                                        "display": {w: word_display.get(w, w) for w in all_words}
                                                    }

    print("Search completed, no solution found.")
    return None

res = search_solutions()
if res:
    import json
    with open("scripts/solution_9x7_exact.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
