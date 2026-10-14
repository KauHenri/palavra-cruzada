import unicodedata
from collections import defaultdict
import time
import json
import random

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

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

blacklist = {
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
    'GPS', 'FBI', 'KGB', 'CIA', 'BBC', 'BMW', 'BIG', 'BOX', 'GAY', 'SEX', 'HOT', 'RED', 'BUS',
    'MEN', 'BOY', 'GIRL', 'MAN', 'WAR', 'END', 'CAR', 'CAT', 'DOG', 'SUN', 'BAD', 'GET', 'RUN',
    'LET', 'SAY', 'PUT', 'NEW', 'OLD', 'ONE', 'TWO', 'TEN', 'FAR', 'HER', 'HIS', 'HIM', 'SHE',
    'WHO', 'WHY', 'HOW', 'ALL', 'ANY', 'MAY', 'WAY', 'DAY', 'OUR', 'NOW', 'OUT', 'OFF', 'PER',
    'MARI', 'VINTAGE', 'HALL', 'ISLAND', 'ICE', 'ARIA', 'ALF', 'ABI', 'ABU', 'AHN', 'ARE',
    'DEA', 'DUM', 'ECA', 'ELI', 'GIL', 'GOA', 'LEO', 'PAU', 'PUS', 'RAI', 'RUM', 'SOS', 'UNA',
    'VAL', 'VOS', 'CAM', 'CLA', 'POP', 'RAM', 'PAT', 'SACANA', 'ERECAO', 'PEITOS', 'MANE',
    'MORE', 'MOLE', 'CACADA', 'CIGANA', 'REATOR', 'MAMILO', 'REITOR', 'EUROPA', 'BANG',
    'BEST', 'HEM', 'HAN', 'ELAINE', 'HONG', 'ROUPAO'
}

w6 = [w for w in (w50 & dict_words) - blacklist if len(w) == 6 and freq.get(w, 0) >= 30 and not w.endswith("ND")]
w3 = [w for w in (w50 & dict_words) - blacklist if len(w) == 3 and freq.get(w, 0) >= 30]
w2 = [
    'AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA', 'LE',
    'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA',
    'DE', 'EM', 'NA', 'SE', 'AO'
]

SET_6 = set(w6)
SET_3 = set(w3)
SET_2 = set(w2)

idx6 = defaultdict(set)
for w in w6:
    for p, ch in enumerate(w):
        idx6[(p, ch)].add(w)

idx3 = defaultdict(set)
for w in w3:
    for p, ch in enumerate(w):
        idx3[(p, ch)].add(w)

def match6(constraints):
    res = None
    for p, ch in constraints:
        s = idx6.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return res if res is not None else set(w6)

def match3(constraints):
    res = None
    for p, ch in constraints:
        s = idx3.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return res if res is not None else set(w3)

# Search classic 7x7:
# (3, 3) is clue, (4, 4) is clue
# Across:
# R1: (1, 1..6)
# R2: (2, 1..6)
# A3_1: (3, 1..2), A3_2: (3, 4..6)
# A4_1: (4, 1..3), A4_2: (4, 5..6)
# R5: (5, 1..6)
# R6: (6, 1..6)
# Down:
# C1: (1..6, 1)
# C2: (1..6, 2)
# D3_1: (1..2, 3), D3_2: (4..6, 3)
# D4_1: (1..3, 4), D4_2: (5..6, 4)
# C5: (1..6, 5)
# C6: (1..6, 6)

t0 = time.time()
found_classic = []
print("Searching classic 7x7...")

# Strategy:
# 1. Pick A4_1 (3 letters: 4,1; 4,2; 4,3)
# 2. D3_2 starts with A4_1[2] (pos 0 of D3_2)
# 3. D4_1 ends with A3_2[0] (pos 2 of D4_1)

for a3_2 in list(w3):
    d4_1_cands = match3([(2, a3_2[0])])
    if not d4_1_cands: continue
    
    for d4_1 in d4_1_cands:
        for d3_1 in w2:
            # R1: (2, d3_1[0]), (3, d4_1[0])
            # R2: (2, d3_1[1]), (3, d4_1[1])
            r1_cands = match6([(2, d3_1[0]), (3, d4_1[0])])
            r2_cands = match6([(2, d3_1[1]), (3, d4_1[1])])
            if not r1_cands or not r2_cands: continue
            
            for r1 in list(r1_cands)[:5]:
                for r2 in list(r2_cands)[:5]:
                    # C5: (0, r1[4]), (1, r2[4]), (2, a3_2[1])
                    # C6: (0, r1[5]), (1, r2[5]), (2, a3_2[2])
                    c5_cands = match6([(0, r1[4]), (1, r2[4]), (2, a3_2[1])])
                    c6_cands = match6([(0, r1[5]), (1, r2[5]), (2, a3_2[2])])
                    if not c5_cands or not c6_cands: continue
                    
                    for c5 in list(c5_cands)[:3]:
                        for c6 in list(c6_cands)[:3]:
                            a4_2 = c5[3] + c6[3]
                            if a4_2 not in SET_2: continue
                            
                            for d4_2 in w2:
                                for a4_1 in list(w3):
                                    # D3_2 starts with a4_1[2]
                                    d3_2_cands = match3([(0, a4_1[2])])
                                    if not d3_2_cands: continue
                                    
                                    for d3_2 in list(d3_2_cands)[:3]:
                                        # R5: (2, d3_2[1]), (3, d4_2[0]), (4, c5[4]), (5, c6[4])
                                        # R6: (2, d3_2[2]), (3, d4_2[1]), (4, c5[5]), (5, c6[5])
                                        r5_cands = match6([(2, d3_2[1]), (3, d4_2[0]), (4, c5[4]), (5, c6[4])])
                                        r6_cands = match6([(2, d3_2[2]), (3, d4_2[1]), (4, c5[5]), (5, c6[5])])
                                        if not r5_cands or not r6_cands: continue
                                        
                                        for r5 in list(r5_cands)[:2]:
                                            for r6 in list(r6_cands)[:2]:
                                                # C1: (0, r1[0]), (1, r2[0]), (3, a4_1[0]), (4, r5[0]), (5, r6[0])
                                                # C2: (0, r1[1]), (1, r2[1]), (3, a4_1[1]), (4, r5[1]), (5, r6[1])
                                                c1_cands = match6([(0, r1[0]), (1, r2[0]), (3, a4_1[0]), (4, r5[0]), (5, r6[0])])
                                                c2_cands = match6([(0, r1[1]), (1, r2[1]), (3, a4_1[1]), (4, r5[1]), (5, r6[1])])
                                                if not c1_cands or not c2_cands: continue
                                                
                                                for c1 in list(c1_cands)[:2]:
                                                    for c2 in list(c2_cands)[:2]:
                                                        a3_1 = c1[2] + c2[2]
                                                        if a3_1 not in SET_2: continue
                                                        
                                                        all_words = [r1, r2, a3_1, a3_2, a4_1, a4_2, r5, r6, c1, c2, d3_1, d3_2, d4_1, d4_2, c5, c6]
                                                        if len(set(all_words)) == len(all_words):
                                                            sol = {
                                                                "R1": r1, "R2": r2, "A3_1": a3_1, "A3_2": a3_2,
                                                                "A4_1": a4_1, "A4_2": a4_2, "R5": r5, "R6": r6,
                                                                "C1": c1, "C2": c2, "D3_1": d3_1, "D3_2": d3_2,
                                                                "D4_1": d4_1, "D4_2": d4_2, "C5": c5, "C6": c6
                                                            }
                                                            found_classic.append(sol)
                                                            print(f"FOUND CLASSIC [{len(found_classic)}] in {time.time()-t0:.2f}s!")
                                                            for k, v in sol.items():
                                                                print(f"  {k}: {v} ({dict_display.get(v, v)})")
                                                            if len(found_classic) >= 5:
                                                                with open("scripts/classic_7x7_solutions.json", "w", encoding="utf-8") as out:
                                                                    json.dump(found_classic, out, indent=2, ensure_ascii=False)
                                                                print("Saved 5 classic solutions!")
                                                                exit(0)

print(f"Done classic. Found: {len(found_classic)}")
