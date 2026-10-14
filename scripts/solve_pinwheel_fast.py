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
    'BEST', 'HEM', 'HAN', 'ELAINE', 'HONG', 'ROUPAO', 'APACHE', 'GIBI', 'PIVE', 'GAFE',
    'THE', 'SAM', 'DON', 'DUO', 'EIA', 'EMA', 'EPA', 'ETA', 'GEO', 'GIA', 'GUA', 'HEI',
    'IAO', 'IMO', 'INA', 'IRA', 'ITA', 'ITU', 'IUA', 'IVA', 'IZA', 'JUS', 'LAO', 'LIA',
    'MEO', 'MIA', 'MIO', 'MOA', 'MOI', 'MUA', 'NEO', 'NIA', 'NOA', 'NOI', 'NUA', 'OBA',
    'OCA', 'ODA', 'ODE', 'OIA', 'OLE', 'OPA', 'ORO', 'OSA', 'OTO', 'OVA', 'PAN', 'PIA',
    'PIO', 'POA', 'POI', 'PUM', 'QUA', 'RAD', 'RAI', 'RAO', 'ROA', 'ROU', 'RUI', 'SED',
    'SEI', 'SEN', 'SIA', 'SIO', 'SOA', 'SOB', 'SOI', 'TAI', 'TAO', 'TEO', 'TOA', 'TRI',
    'TUI', 'UBA', 'UIA', 'UIS', 'UJA', 'UMA', 'UNI', 'URA', 'URI', 'USA', 'USO', 'VEE',
    'VEO', 'VIO', 'VIS', 'VIU', 'ZUM', 'AGI', 'AGU', 'AIA', 'ALU', 'ANI', 'ANU', 'APO',
    'ARU', 'ATI', 'AVO', 'AZA', 'AZI', 'BAL', 'BEI', 'BEL', 'BES', 'BIM', 'BIS', 'BOB',
    'BOI', 'BON', 'BOR', 'BOU', 'BRA', 'BRE', 'BRI', 'BRO', 'BRU', 'BUA', 'BUE', 'BUI',
    'BUL', 'BUR', 'BUZ', 'CAB', 'CAD', 'CAI', 'CAL', 'CAS', 'CEI', 'CHA', 'CHE', 'CHI',
    'CHU', 'CIS', 'COL', 'CON', 'COS', 'COT', 'COX', 'CRA', 'CRE', 'CRI', 'CRO', 'CRU',
    'CUB', 'CUE', 'CUI', 'CUM', 'CUR', 'CUS', 'DAN', 'DAS', 'DEL', 'DEM', 'DEN', 'DES',
    'DET', 'DEV', 'DIL', 'DIN', 'DIS', 'DIV', 'DOS', 'DOU', 'DRO', 'DRU', 'DUB', 'DUC',
    'AIR', 'BIP', 'BLA', 'BUM', 'ETC', 'EUA', 'FAX', 'FOX', 'GIM', 'HIP', 'HOP',
    'HUM', 'III', 'JAN', 'JIM', 'JOE', 'KIT', 'LEX', 'LIV', 'LUX', 'MAX', 'MMM',
    'NOE', 'ONU', 'OPS', 'PEN', 'PIT', 'RAY', 'SET', 'SPA', 'STA', 'SUB', 'TAJ',
    'TIM', 'UAU', 'UTI', 'VAN', 'VIP', 'VON', 'ZEN', 'ZOE'
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
    for p, ch in enumerate(w): idx6[(p, ch)].add(w)

idx3 = defaultdict(set)
for w in w3:
    for p, ch in enumerate(w): idx3[(p, ch)].add(w)

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

t0 = time.time()
solutions = []
random.seed(777)

print(f"Pinwheel Pool sizes: w6={len(w6)}, w3={len(w3)}, w2={len(w2)}")

# Pinwheel solving:
# 1. R1 and R2
# 2. C1 and C2
# 3. R3_L = (C1[2], C2[2]) must be in SET_2
# 4. R4_L = (C1[3], C2[3], C3_B[0]) -> find C3_B
# 5. C3_T = (R1[2], R2[2]) must be in SET_2
# 6. C4_T = (R1[3], R2[3], R3_R[0]) -> find R3_R
# 7. C5 and C6
# 8. R3_R = (C4_T[2], C5[2], C6[2]) must match
# 9. R4_R = (C5[3], C6[3]) must be in SET_2
# 10. R5 and R6
# 11. C4_B = (R5[3], R6[3]) must be in SET_2

# Let's start with C1 and C2:
w6_shuffled = list(w6)
random.shuffle(w6_shuffled)

for c1 in w6_shuffled:
    # C2
    c2_cands = match6([(2, None)])
    for c2 in c2_cands:
        if c1 == c2: continue
        r3_l = c1[2] + c2[2]
        if r3_l not in SET_2: continue
        
        # R4_L starts with c1[3] + c2[3]
        r4_l_cands = match3([(0, c1[3]), (1, c2[3])])
        if not r4_l_cands: continue
        
        for r4_l in r4_l_cands:
            # C3_B starts with r4_l[2]
            c3_b_cands = match3([(0, r4_l[2])])
            if not c3_b_cands: continue
            
            for c3_b in c3_b_cands:
                # Now R1 and R2:
                # R1[0] = c1[0], R1[1] = c2[0]
                # R2[0] = c1[1], R2[1] = c2[1]
                r1_cands = match6([(0, c1[0]), (1, c2[0])])
                r2_cands = match6([(0, c1[1]), (1, c2[1])])
                if not r1_cands or not r2_cands: continue
                
                for r1 in r1_cands:
                    if r1 in {c1, c2}: continue
                    for r2 in r2_cands:
                        if r2 in {c1, c2, r1}: continue
                        c3_t = r1[2] + r2[2]
                        if c3_t not in SET_2: continue
                        
                        # C4_T starts with r1[3] + r2[3]
                        c4_t_cands = match3([(0, r1[3]), (1, r2[3])])
                        if not c4_t_cands: continue
                        
                        for c4_t in c4_t_cands:
                            # R3_R starts with c4_t[2]
                            r3_r_cands = match3([(0, c4_t[2])])
                            if not r3_r_cands: continue
                            
                            for r3_r in r3_r_cands:
                                # Now C5 and C6:
                                # C5: index 0 is r1[4], index 1 is r2[4], index 2 is r3_r[1]
                                # C6: index 0 is r1[5], index 1 is r2[5], index 2 is r3_r[2]
                                c5_cands = match6([(0, r1[4]), (1, r2[4]), (2, r3_r[1])])
                                c6_cands = match6([(0, r1[5]), (1, r2[5]), (2, r3_r[2])])
                                if not c5_cands or not c6_cands: continue
                                
                                for c5 in c5_cands:
                                    if c5 in {c1, c2, r1, r2}: continue
                                    for c6 in c6_cands:
                                        if c6 in {c1, c2, r1, r2, c5}: continue
                                        r4_r = c5[3] + c6[3]
                                        if r4_r not in SET_2: continue
                                        
                                        # Now R5 and R6:
                                        # R5: index 0 is c1[4], index 1 is c2[4], index 2 is c3_b[1], index 4 is c5[4], index 5 is c6[4]
                                        # R6: index 0 is c1[5], index 1 is c2[5], index 2 is c3_b[2], index 4 is c5[5], index 5 is c6[5]
                                        r5_cands = match6([(0, c1[4]), (1, c2[4]), (2, c3_b[1]), (4, c5[4]), (5, c6[4])])
                                        r6_cands = match6([(0, c1[5]), (1, c2[5]), (2, c3_b[2]), (4, c5[5]), (5, c6[5])])
                                        if not r5_cands or not r6_cands: continue
                                        
                                        for r5 in r5_cands:
                                            if r5 in {c1, c2, r1, r2, c5, c6}: continue
                                            for r6 in r6_cands:
                                                if r6 in {c1, c2, r1, r2, c5, c6, r5}: continue
                                                c4_b = r5[3] + r6[3]
                                                if c4_b not in SET_2: continue
                                                
                                                all_w = [r1, r2, r3_l, r3_r, r4_l, r4_r, r5, r6, c1, c2, c3_t, c3_b, c4_t, c4_b, c5, c6]
                                                if len(set(all_w)) == len(all_w):
                                                    sol = {
                                                        "R1": r1, "R2": r2, "R3_L": r3_l, "R3_R": r3_r,
                                                        "R4_L": r4_l, "R4_R": r4_r, "R5": r5, "R6": r6,
                                                        "C1": c1, "C2": c2, "C3_T": c3_t, "C3_B": c3_b,
                                                        "C4_T": c4_t, "C4_B": c4_b, "C5": c5, "C6": c6
                                                    }
                                                    solutions.append(sol)
                                                    print(f"PINWHEEL #{len(solutions)} in {time.time()-t0:.2f}s!")
                                                    print(f"  R1: {r1}, R2: {r2}, R5: {r5}, R6: {r6}")
                                                    print(f"  C1: {c1}, C2: {c2}, C5: {c5}, C6: {c6}")
                                                    print(f"  R3: {r3_l} / {r3_r}, R4: {r4_l} / {r4_r}")
                                                    print(f"  C3: {c3_t} / {c3_b}, C4: {c4_t} / {c4_b}")
                                                    if len(solutions) >= 10:
                                                        with open("scripts/pinwheel_solutions.json", "w", encoding="utf-8") as out:
                                                            json.dump(solutions, out, indent=2, ensure_ascii=False)
                                                        print("Saved 10 pinwheels!")
                                                        exit(0)

print(f"Done. Found: {len(solutions)}")
with open("scripts/pinwheel_solutions.json", "w", encoding="utf-8") as out:
    json.dump(solutions, out, indent=2, ensure_ascii=False)
