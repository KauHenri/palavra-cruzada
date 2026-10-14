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

base_blacklist = {
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
    'MORE', 'MOLE', 'CACADA', 'CIGANA', 'REATOR', 'MAMILO', 'REITOR', 'EUROPA'
}

# Level 1 words chosen:
lvl1 = {
    'R1': 'DECADA', 'R2': 'ACUCAR', 'R3': 'ROSE', 'R4': 'PIPA', 'R5': 'FEITAS', 'R6': 'AURORA',
    'C1_top': 'DAR', 'C2_top': 'ECO', 'C3': 'CUSPIR', 'C4': 'ACEITO',
    'C5_top': 'DA', 'C6_top': 'AR', 'C1_bot': 'FA', 'C2_bot': 'EU', 'C5_bot': 'PAR', 'C6_bot': 'ASA'
}
lvl1_words = set(lvl1.values())

def find_level(excluded_words, target_count=1):
    # Only exclude words of length >= 3 across levels!
    len3_excluded = {w for w in excluded_words if len(w) >= 3}
    blacklist = base_blacklist | len3_excluded
    
    w6 = [w for w in (w50 & dict_words) - blacklist if len(w) == 6 and freq.get(w, 0) >= 35 and not w.endswith("ND")]
    w4 = [w for w in (w50 & dict_words) - blacklist if len(w) == 4 and freq.get(w, 0) >= 35]
    w3 = [w for w in (w50 & dict_words) - blacklist if len(w) == 3 and freq.get(w, 0) >= 35]
    w2 = [w for w in ['AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA', 'LE',
                      'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA',
                      'DE', 'EM', 'NA', 'SE', 'AO'] if w not in excluded_words]

    idx6 = defaultdict(set)
    for w in w6:
        for p, ch in enumerate(w):
            idx6[(p, ch)].add(w)

    idx4 = defaultdict(set)
    for w in w4:
        for p, ch in enumerate(w):
            idx4[(p, ch)].add(w)

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

    SET_2 = set(w2)
    sols = []
    
    w4_shuffled = list(w4)
    random.shuffle(w4_shuffled)
    
    for r3 in w4_shuffled:
        c1_cands = match3([(2, r3[0])])
        c2_cands = match3([(2, r3[1])])
        if not c1_cands or not c2_cands: continue
        
        for c1_top in c1_cands:
            for c2_top in c2_cands:
                if c1_top == c2_top: continue
                r1_cands = match6([(0, c1_top[0]), (1, c2_top[0])])
                r2_cands = match6([(0, c1_top[1]), (1, c2_top[1])])
                if not r1_cands or not r2_cands: continue
                
                for r1 in r1_cands:
                    for r2 in r2_cands:
                        if r1 == r2: continue
                        c5_top = r1[4] + r2[4]
                        if c5_top not in SET_2: continue
                        c6_top = r1[5] + r2[5]
                        if c6_top not in SET_2 or c6_top == c5_top: continue
                        
                        c3_cands = match6([(0, r1[2]), (1, r2[2]), (2, r3[2])])
                        c4_cands = match6([(0, r1[3]), (1, r2[3]), (2, r3[3])])
                        if not c3_cands or not c4_cands: continue
                        
                        top_words = {r1, r2, r3, c1_top, c2_top, c5_top, c6_top}
                        if len(top_words) < 7: continue
                        
                        for c3 in c3_cands:
                            for c4 in c4_cands:
                                if c3 == c4 or c3 in top_words or c4 in top_words: continue
                                
                                r4_cands = match4([(0, c3[3]), (1, c4[3])])
                                if not r4_cands: continue
                                
                                for r4 in r4_cands:
                                    c5_cands = match3([(0, r4[2])])
                                    c6_cands = match3([(0, r4[3])])
                                    if not c5_cands or not c6_cands: continue
                                    
                                    for c5_bot in c5_cands:
                                        for c6_bot in c6_cands:
                                            if c5_bot == c6_bot: continue
                                            r5_cands = match6([(2, c3[4]), (3, c4[4]), (4, c5_bot[1]), (5, c6_bot[1])])
                                            r6_cands = match6([(2, c3[5]), (3, c4[5]), (4, c5_bot[2]), (5, c6_bot[2])])
                                            if not r5_cands or not r6_cands: continue
                                            
                                            for r5 in r5_cands:
                                                for r6 in r6_cands:
                                                    if r5 == r6: continue
                                                    c1_bot = r5[0] + r6[0]
                                                    if c1_bot not in SET_2 or c1_bot in top_words: continue
                                                    c2_bot = r5[1] + r6[1]
                                                    if c2_bot not in SET_2 or c2_bot in top_words or c2_bot == c1_bot: continue
                                                    
                                                    all_words = [r1, r2, r3, r4, r5, r6, c1_top, c2_top, c3, c4, c5_top, c6_top, c1_bot, c2_bot, c5_bot, c6_bot]
                                                    if len(set(all_words)) == len(all_words):
                                                        sol = {
                                                            "R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6,
                                                            "C1_top": c1_top, "C2_top": c2_top, "C3": c3, "C4": c4,
                                                            "C5_top": c5_top, "C6_top": c6_top,
                                                            "C1_bot": c1_bot, "C2_bot": c2_bot, "C5_bot": c5_bot, "C6_bot": c6_bot
                                                        }
                                                        sols.append(sol)
                                                        if len(sols) >= target_count:
                                                            return sols
    return sols

print("Searching Level 2 excluding Level 1...")
t0 = time.time()
lvl2_list = find_level(lvl1_words, target_count=1)
if not lvl2_list:
    print("Failed finding Level 2")
    exit(1)

lvl2 = lvl2_list[0]
lvl2_words = set(lvl2.values())
print(f"Level 2 found in {time.time()-t0:.2f}s!")
for k, v in lvl2.items():
    print(f"  {k}: {v} ({dict_display.get(v, v)})")

print("\nSearching Level 3 excluding Level 1 and Level 2...")
t0 = time.time()
lvl3_list = find_level(lvl1_words | lvl2_words, target_count=1)
if not lvl3_list:
    print("Failed finding Level 3")
    exit(1)

lvl3 = lvl3_list[0]
lvl3_words = set(lvl3.values())
print(f"Level 3 found in {time.time()-t0:.2f}s!")
for k, v in lvl3.items():
    print(f"  {k}: {v} ({dict_display.get(v, v)})")

with open("scripts/levels_1_2_3.json", "w", encoding="utf-8") as out:
    json.dump({"level1": lvl1, "level2": lvl2, "level3": lvl3}, out, indent=2, ensure_ascii=False)
print("\nSAVED LEVELS 1, 2, 3 TO scripts/levels_1_2_3.json!")
