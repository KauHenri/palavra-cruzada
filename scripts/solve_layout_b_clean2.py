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
    'MARI', 'VINTAGE', 'HALL', 'ISLAND', 'ICE', 'POP', 'RAM', 'PAT', 'BANG', 'BEST', 'HEM', 'HAN',
    'HONG', 'ROBE', 'SECTOR', 'VECTOR', 'BAR', 'PUB', 'SHOW', 'SITE', 'WEB', 'APP', 'LINK',
    'POST', 'FEED', 'CHAT', 'EMAIL', 'MAIL', 'BYTE', 'BIT', 'PIXEL', 'CHIP',
    'ROCK', 'JAZZ', 'BLUES', 'PUNK', 'RAP', 'FUNK', 'METAL', 'DISCO', 'DJ',
    'AIR', 'BIP', 'BLA', 'BUM', 'ETC', 'EUA', 'FAX', 'FOX', 'GIM', 'HIP', 'HOP',
    'HUM', 'III', 'JAN', 'JIM', 'JOE', 'KIT', 'LEX', 'LIV', 'LUX', 'MAX', 'MMM',
    'NOE', 'ONU', 'OPS', 'PEN', 'PIT', 'RAY', 'SET', 'SPA', 'STA', 'SUB', 'TAJ',
    'TIM', 'UAU', 'UTI', 'VAN', 'VIP', 'VON', 'ZEN', 'ZOE',
    'SACANA', 'ERECAO', 'PEITOS', 'MANE', 'MORE', 'MOLE', 'CACADA', 'CIGANA', 'REATOR', 'REITOR', 'EUROPA',
    'CLAIRE', 'ELAINE', 'AVATAR', 'TURNER', 'LARA', 'ROSE', 'MANA', 'MAMA',
    'IVAN', 'AMELIA', 'ISRAEL', 'OTARIO', 'LANA', 'MONA', 'NANA', 'NINA', 'ZONA', 'MEXE'
}

grid1_words = {'ABRE', 'ACEITO', 'AURORA', 'CURTIR', 'DEITAR', 'ELA', 'ERA', 'ESCALA', 'ESCAPA', 'LOUCAS', 'MAR', 'SOB', 'TIME', 'LEITOR', 'TIPO', 'POR'}
grid2_words = {'ADOTAR', 'ALEMAS', 'ALO', 'AMANTE', 'CAL', 'CASACO', 'CASADO', 'DAI', 'INDO', 'LONA', 'ORA', 'SENIOR', 'SEREIA'}
lvl4_words = {'ACAROS', 'LAPELA', 'EVASAO', 'MARI', 'ESTE', 'NECTAR', 'ELEITO', 'MORROS', 'ALEM', 'NEM', 'CAVA', 'ELO', 'APARECER', 'RESISTIR', 'OLA', 'TATO', 'SAO', 'EROS'}

forbidden = blacklist | grid1_words | grid2_words | lvl4_words

w2 = [
    'AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA', 'LE',
    'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA',
    'DE', 'EM', 'NA', 'SE', 'AO', 'OU', 'AS', 'OS'
]

w6 = [w for w in (w50 & dict_words) - forbidden if len(w) == 6 and freq.get(w, 0) >= 20 and not w.endswith('NDO') and not w.endswith('ND')]
w4 = [w for w in (w50 & dict_words) - forbidden if len(w) == 4 and freq.get(w, 0) >= 20]
w3 = [w for w in (w50 & dict_words) - forbidden if len(w) == 3 and freq.get(w, 0) >= 20]

SET_6 = set(w6)
SET_4 = set(w4)
SET_3 = set(w3)
SET_2 = set(w2)

idx6 = defaultdict(set)
for w in w6:
    for p, ch in enumerate(w): idx6[(p, ch)].add(w)

idx4 = defaultdict(set)
for w in w4:
    for p, ch in enumerate(w): idx4[(p, ch)].add(w)

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

def match4(constraints):
    res = None
    for p, ch in constraints:
        s = idx4.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return res if res is not None else set(w4)

def match3(constraints):
    res = None
    for p, ch in constraints:
        s = idx3.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return res if res is not None else set(w3)

# Layout B Structure:
# R1: cols 1..6 (len 6)
# R2: cols 1..6 (len 6)
# R3: cols 3..6 (len 4) -> clues at (3,1) and (3,2)
# R4: cols 1..4 (len 4) -> clues at (4,5) and (4,6)
# R5: cols 1..6 (len 6)
# R6: cols 1..6 (len 6)
#
# C1_top: rows 1..2 (len 2: R1[0], R2[0])
# C2_top: rows 1..2 (len 2: R1[1], R2[1])
# C3: rows 1..6 (len 6: R1[2], R2[2], R3[0], R4[2], R5[2], R6[2])
# C4: rows 1..6 (len 6: R1[3], R2[3], R3[1], R4[3], R5[3], R6[3])
# C5_top: rows 1..3 (len 3: R1[4], R2[4], R3[2])
# C6_top: rows 1..3 (len 3: R1[5], R2[5], R3[3])
#
# C1_bot: rows 4..6 (len 3: R4[0], R5[0], R6[0])
# C2_bot: rows 4..6 (len 3: R4[1], R5[1], R6[1])
# C5_bot: rows 5..6 (len 2: R5[4], R6[4])
# C6_bot: rows 5..6 (len 2: R5[5], R6[5])

t0 = time.time()
found_b = []
random.seed(42)
w4_shuf = list(w4)
random.shuffle(w4_shuf)

print(f"Searching Layout B... w6={len(w6)}, w4={len(w4)}, w3={len(w3)}")
for r3 in w4_shuf:
    # C5_top ends in r3[2], C6_top ends in r3[3]
    c5_cands = match3([(2, r3[2])])
    c6_cands = match3([(2, r3[3])])
    if not c5_cands or not c6_cands: continue
    
    for c5_top in c5_cands:
        for c6_top in c6_cands:
            r1_cands = match6([(4, c5_top[0]), (5, c6_top[0])])
            r2_cands = match6([(4, c5_top[1]), (5, c6_top[1])])
            if not r1_cands or not r2_cands: continue
            
            for r1 in r1_cands:
                for r2 in r2_cands:
                    c1_top = r1[0] + r2[0]
                    if c1_top not in SET_2: continue
                    c2_top = r1[1] + r2[1]
                    if c2_top not in SET_2: continue
                    
                    c3_cands = match6([(0, r1[2]), (1, r2[2]), (2, r3[0])])
                    c4_cands = match6([(0, r1[3]), (1, r2[3]), (2, r3[1])])
                    if not c3_cands or not c4_cands: continue
                    
                    top_words = {r1, r2, r3, c1_top, c2_top, c5_top, c6_top}
                    if len(top_words) < 7: continue
                    
                    for c3 in c3_cands:
                        for c4 in c4_cands:
                            if c3 == c4 or c3 in top_words or c4 in top_words: continue
                            
                            r4_cands = match4([(2, c3[3]), (3, c4[3])])
                            if not r4_cands: continue
                            
                            for r4 in r4_cands:
                                c1_cands = match3([(0, r4[0])])
                                c2_cands = match3([(0, r4[1])])
                                if not c1_cands or not c2_cands: continue
                                
                                for c1_bot in c1_cands:
                                    for c2_bot in c2_cands:
                                        r5_cands = match6([(0, c1_bot[1]), (1, c2_bot[1]), (2, c3[4]), (3, c4[4])])
                                        r6_cands = match6([(0, c1_bot[2]), (1, c2_bot[2]), (2, c3[5]), (3, c4[5])])
                                        if not r5_cands or not r6_cands: continue
                                        
                                        for r5 in r5_cands:
                                            for r6 in r6_cands:
                                                c5_bot = r5[4] + r6[4]
                                                if c5_bot not in SET_2: continue
                                                c6_bot = r5[5] + r6[5]
                                                if c6_bot not in SET_2: continue
                                                
                                                all_words = [r1, r2, r3, r4, r5, r6, c1_top, c2_top, c3, c4, c5_top, c6_top, c1_bot, c2_bot, c5_bot, c6_bot]
                                                if len(set(all_words)) == len(all_words):
                                                    sol = {
                                                        "layout": "B",
                                                        "R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6,
                                                        "C1_top": c1_top, "C2_top": c2_top, "C3": c3, "C4": c4,
                                                        "C5_top": c5_top, "C6_top": c6_top,
                                                        "C1_bot": c1_bot, "C2_bot": c2_bot, "C5_bot": c5_bot, "C6_bot": c6_bot
                                                    }
                                                    found_b.append(sol)
                                                    print(f"FOUND LAYOUT B #{len(found_b)} in {time.time()-t0:.2f}s!")
                                                    for k, v in sol.items():
                                                        print(f"  {k}: {v}")
                                                    if len(found_b) >= 10:
                                                        with open("scripts/layout_b_sols.json", "w", encoding="utf-8") as out:
                                                            json.dump(found_b, out, indent=2, ensure_ascii=False)
                                                        print("Saved 10 Layout B solutions!")
                                                        exit(0)

print(f"Layout B Finished. Found: {len(found_b)}")
with open("scripts/layout_b_sols.json", "w", encoding="utf-8") as out:
    json.dump(found_b, out, indent=2, ensure_ascii=False)
