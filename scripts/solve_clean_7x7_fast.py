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

# Strictly forbidden words
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
    'MARI', 'VINTAGE', 'HALL'
}

# 6-letter words: top 50k, in dictionary, not proper noun, not blacklisted
w6_cands = [w for w in (w50 & dict_words) - blacklist if len(w) == 6 and freq.get(w, 0) >= 30]

# 3-letter words: genuine Portuguese words
w3_cands = [w for w in (w50 & dict_words) - blacklist if len(w) == 3 and freq.get(w, 0) >= 50]

# 2-letter words: familiar everyday words
w2_cands = [
    'AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA', 'LE',
    'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA',
    'DE', 'EM', 'NA', 'SE', 'AO'
]

SET_6 = set(w6_cands)
SET_3 = set(w3_cands)
SET_2 = set(w2_cands)

print(f"Loaded clean pool: 6-letter: {len(SET_6)}, 3-letter: {len(SET_3)}, 2-letter: {len(SET_2)}")

# Fast prefix / pattern indices
idx6 = defaultdict(set)
for w in SET_6:
    for p, ch in enumerate(w):
        idx6[(p, ch)].add(w)

def query6(constraints):
    res = None
    for p, ch in constraints:
        s = idx6.get((p, ch), set())
        if res is None:
            res = set(s)
        else:
            res &= s
        if not res:
            return set()
    return res if res is not None else set(SET_6)

# Test search
found = []
t0 = time.time()
print("Searching for clean 7x7 solutions...")

# Strategy: iterate through C1 and C2
# Then A3_1 = C1[2] + C2[2] (must be in SET_2)
# Then A4_1 = C1[3] + C2[3] + ? (must start with C1[3]+C2[3], len 3 in SET_3)
c1_pool = list(SET_6)
random.seed(123)
random.shuffle(c1_pool)

for c1 in c1_pool[:300]:
    # c2 must have c1[2] + c2[2] in SET_2
    possible_c2_chars2 = {w[1] for w in SET_2 if w[0] == c1[2]}
    if not possible_c2_chars2:
        continue
    
    # Also c1[3] + c2[3] must be a prefix of a word in SET_3
    possible_c2_chars3 = {w[1] for w in SET_3 if w[0] == c1[3]}
    if not possible_c2_chars3:
        continue
        
    c2_cands = query6([])
    c2_valid = [w for w in c2_cands if w[2] in possible_c2_chars2 and w[3] in possible_c2_chars3 and w != c1]
    
    for c2 in c2_valid[:30]:
        a3_1 = c1[2] + c2[2]
        if a3_1 not in SET_2:
            continue
            
        cand_a4_1 = [w for w in SET_3 if w[0] == c1[3] and w[1] == c2[3]]
        if not cand_a4_1:
            continue
            
        for a4_1 in cand_a4_1:
            d3_2_first = a4_1[2] # (4,3)
            # R1 starts with c1[0], c2[0]
            r1_cands = query6([(0, c1[0]), (1, c2[0])])
            # R2 starts with c1[1], c2[1]
            r2_cands = query6([(0, c1[1]), (1, c2[1])])
            if not r1_cands or not r2_cands:
                continue
                
            for d3_1 in SET_2:
                # d3_1 is (1,3), (2,3) -> r1[2]=d3_1[0], r2[2]=d3_1[1]
                r1_sub = [w for w in r1_cands if w[2] == d3_1[0] and w not in (c1, c2)]
                r2_sub = [w for w in r2_cands if w[2] == d3_1[1] and w not in (c1, c2)]
                if not r1_sub or not r2_sub:
                    continue
                    
                for d4_1 in SET_3:
                    # d4_1 is (1,4), (2,4), (3,4) -> r1[3]=d4_1[0], r2[3]=d4_1[1]
                    r1_valid = [w for w in r1_sub if w[3] == d4_1[0]]
                    r2_valid = [w for w in r2_sub if w[3] == d4_1[1]]
                    if not r1_valid or not r2_valid:
                        continue
                        
                    cand_a3_2 = [w for w in SET_3 if w[0] == d4_1[2]]
                    if not cand_a3_2:
                        continue
                        
                    for a3_2 in cand_a3_2:
                        for r1 in r1_valid[:3]:
                            for r2 in r2_valid[:3]:
                                # Now C5 and C6
                                c5_cands = query6([(0, r1[4]), (1, r2[4]), (2, a3_2[1])])
                                c6_cands = query6([(0, r1[5]), (1, r2[5]), (2, a3_2[2])])
                                if not c5_cands or not c6_cands:
                                    continue
                                    
                                for col5 in list(c5_cands)[:5]:
                                    for col6 in list(c6_cands)[:5]:
                                        a4_2 = col5[3] + col6[3]
                                        if a4_2 not in SET_2:
                                            continue
                                            
                                        for d4_2 in SET_2:
                                            for d3_2 in SET_3:
                                                if d3_2[0] != d3_2_first:
                                                    continue
                                                # R5: (5,1)=c1[4], (5,2)=c2[4], (5,3)=d3_2[1], (5,4)=d4_2[0], (5,5)=col5[4], (5,6)=col6[4]
                                                r5_cands = query6([(0, c1[4]), (1, c2[4]), (2, d3_2[1]), (3, d4_2[0]), (4, col5[4]), (5, col6[4])])
                                                if not r5_cands:
                                                    continue
                                                # R6: (6,1)=c1[5], (6,2)=c2[5], (6,3)=d3_2[2], (6,4)=d4_2[1], (6,5)=col5[5], (6,6)=col6[5]
                                                r6_cands = query6([(0, c1[5]), (1, c2[5]), (2, d3_2[2]), (3, d4_2[1]), (4, col5[5]), (5, col6[5])])
                                                if not r6_cands:
                                                    continue
                                                    
                                                for r5 in r5_cands:
                                                    for r6 in r6_cands:
                                                        words = [r1, r2, a3_1, a3_2, a4_1, a4_2, r5, r6, c1, c2, d3_1, d3_2, d4_1, d4_2, col5, col6]
                                                        if len(set(words)) == len(words):
                                                            sol = {
                                                                'R1': r1, 'R2': r2, 'A3_1': a3_1, 'A3_2': a3_2,
                                                                'A4_1': a4_1, 'A4_2': a4_2, 'R5': r5, 'R6': r6,
                                                                'C1': c1, 'C2': c2, 'D3_1': d3_1, 'D3_2': d3_2,
                                                                'D4_1': d4_1, 'D4_2': d4_2, 'C5': col5, 'C6': col6
                                                            }
                                                            found.append(sol)
                                                            print(f"FOUND [{len(found)}] in {time.time()-t0:.2f}s:")
                                                            for k, v in sol.items():
                                                                print(f"  {k}: {v} ({dict_display.get(v, v)})")
                                                            if len(found) >= 10:
                                                                with open("scripts/clean_7x7_solutions.json", "w", encoding="utf-8") as out:
                                                                    json.dump(found, out, indent=2, ensure_ascii=False)
                                                                print("Saved 10 solutions to scripts/clean_7x7_solutions.json")
                                                                exit(0)
    if len(found) >= 10:
        break

print(f"Search ended. Total found: {len(found)}")
