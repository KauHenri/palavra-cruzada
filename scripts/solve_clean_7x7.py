import unicodedata
from collections import defaultdict
import time
import json
import random

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
dict_words = set()
dict_display = {}
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        raw = line.strip()
        w = strip_accents(raw)
        if w.isalpha():
            dict_words.add(w)
            if w not in dict_display:
                dict_display[w] = raw.upper()

freq = {}
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if len(p) >= 3 and not p[1][0].isupper():
            w = strip_accents(p[0])
            freq[w] = max(freq.get(w, 0), int(p[2]))

w50 = set()
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if p and p[0].isalpha():
            w50.add(strip_accents(p[0]))

# Blacklist foreign, weird, abbreviations
bad = {
    'ART', 'ALIENS', 'SA', 'ADA', 'ARI', 'ME', 'DORIAN', 'ACE', 'ST', 'EST', 'AM',
    'BELMAZ', 'ZORAIA', 'RUEIRO', 'LOROSA', 'ARATUS', 'ICAPUI', 'TA', 'SI', 'TI',
    'DUMA', 'LIONEL', 'DALE', 'ESTEREIS', 'ALOMORFO', 'BENJAMIN', 'CAMARA', 'OURESCER',
    'IGDLOITA', 'ARARAI', 'MATESE', 'AMICAL', 'MADRIA', 'ERGUER', 'SOIOTO', 'MAMILO',
    'ANAS', 'JIRO', 'OTAN', 'RAMONA', 'ARGO', 'TOTO', 'VECTOR', 'ASIM', 'NAOS',
    'LOIRAS', 'LOIROS', 'ZELOSO', 'ARSENICO', 'UNOS', 'ROBE', 'MICADO', 'AMADAS',
    'CAMADA', 'TAMA', 'AMAL', 'MEBOSA', 'OLOFRO', 'SECTOR', 'MARIACHI', 'MARISA',
    'ELISSA', 'LAOS', 'IVES', 'ALAN', 'DAMIEN', 'ERIC', 'NERO', 'HOME', 'CHAD',
    'HORACE', 'CHET', 'STAN', 'CORNO', 'BITCH', 'COCK', 'PENIS', 'VAGINA', 'SHIT',
    'FUCK', 'DICK', 'DIE', 'MIN', 'DOC', 'TOP', 'DNA', 'DVD', 'CDS', 'CSI', 'HIV',
    'GPS', 'FBI', 'KGB', 'CIA', 'BBC', 'BMW', 'BIG', 'BOX', 'GAY', 'SEX', 'HOT', 'RED', 'BUS'
}

WORDS_6 = [w for w in (w50 & dict_words) - bad if len(w) == 6 and freq.get(w, 0) >= 60]
WORDS_3 = [w for w in (w50 & dict_words) - bad if len(w) == 3 and freq.get(w, 0) >= 100]
WORDS_2 = ['AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA', 'LE', 'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA', 'DE', 'EM', 'NA', 'SE', 'AO']

SET_3 = set(WORDS_3)
SET_2 = set(WORDS_2)

print(f"WORDS_6: {len(WORDS_6)}, WORDS_3: {len(SET_3)}, WORDS_2: {len(SET_2)}")

idx6 = defaultdict(set)
for w in WORDS_6:
    for p, ch in enumerate(w):
        idx6[(p, ch)].add(w)

def match6(constraints):
    res = None
    for p, ch in constraints:
        s = idx6.get((p, ch), set())
        if res is None:
            res = set(s)
        else:
            res &= s
        if not res:
            return set()
    return res if res is not None else set(WORDS_6)

found = []
t0 = time.time()
print("Starting search...")

# Shuffle to find diverse solutions
c3_list = list(WORDS_3)
random.seed(42)
random.shuffle(c3_list)

for d4_1 in c3_list:
    # A3_2 starts with d4_1[2]
    cand_a3_2 = [w for w in WORDS_3 if w[0] == d4_1[2]]
    if not cand_a3_2:
        continue
    for a3_2 in cand_a3_2:
        for d3_1 in WORDS_2:
            r1_cands = match6([(2, d3_1[0]), (3, d4_1[0])])
            if not r1_cands:
                continue
            r2_cands = match6([(2, d3_1[1]), (3, d4_1[1])])
            if not r2_cands:
                continue
            
            for r1 in r1_cands:
                for r2 in r2_cands:
                    c5_cands = match6([(0, r1[4]), (1, r2[4]), (2, a3_2[1])])
                    if not c5_cands:
                        continue
                    c6_cands = match6([(0, r1[5]), (1, r2[5]), (2, a3_2[2])])
                    if not c6_cands:
                        continue
                    
                    for col5 in c5_cands:
                        for col6 in c6_cands:
                            a4_2 = col5[3] + col6[3]
                            if a4_2 not in SET_2:
                                continue
                            
                            for d4_2 in WORDS_2:
                                for d3_2 in WORDS_3:
                                    r5_cands = match6([(2, d3_2[1]), (3, d4_2[0]), (4, col5[4]), (5, col6[4])])
                                    if not r5_cands:
                                        continue
                                    r6_cands = match6([(2, d3_2[2]), (3, d4_2[1]), (4, col5[5]), (5, col6[5])])
                                    if not r6_cands:
                                        continue
                                    
                                    for r5 in r5_cands:
                                        for r6 in r6_cands:
                                            c1_cands = match6([(0, r1[0]), (1, r2[0]), (4, r5[0]), (5, r6[0])])
                                            if not c1_cands:
                                                continue
                                            c2_cands = match6([(0, r1[1]), (1, r2[1]), (4, r5[1]), (5, r6[1])])
                                            if not c2_cands:
                                                continue
                                            
                                            for col1 in c1_cands:
                                                for col2 in c2_cands:
                                                    a3_1 = col1[2] + col2[2]
                                                    if a3_1 not in SET_2:
                                                        continue
                                                    a4_1 = col1[3] + col2[3] + d3_2[0]
                                                    if a4_1 not in SET_3:
                                                        continue
                                                    
                                                    words = [r1, r2, a3_1, a3_2, a4_1, a4_2, r5, r6, col1, col2, d3_1, d3_2, d4_1, d4_2, col5, col6]
                                                    if len(set(words)) == len(words):
                                                        sol = {
                                                            'R1': r1, 'R2': r2, 'A3_1': a3_1, 'A3_2': a3_2,
                                                            'A4_1': a4_1, 'A4_2': a4_2, 'R5': r5, 'R6': r6,
                                                            'C1': col1, 'C2': col2, 'D3_1': d3_1, 'D3_2': d3_2,
                                                            'D4_1': d4_1, 'D4_2': d4_2, 'C5': col5, 'C6': col6
                                                        }
                                                        found.append(sol)
                                                        print(f"[{len(found)}] in {time.time()-t0:.2f}s:")
                                                        for k, v in sol.items():
                                                            print(f"  {k}: {v} ({dict_display.get(v, v)})")
                                                        if len(found) >= 5:
                                                            with open("scripts/found_solutions.json", "w", encoding="utf-8") as out:
                                                                json.dump(found, out, indent=2, ensure_ascii=False)
                                                            print("SAVED 5 SOLUTIONS!")
                                                            exit(0)
