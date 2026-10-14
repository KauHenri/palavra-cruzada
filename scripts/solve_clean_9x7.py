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

w8 = [w for w in (w50 & dict_words) - blacklist if len(w) == 8 and freq.get(w, 0) >= 30 and not w.endswith("ND")]
w6 = [w for w in (w50 & dict_words) - blacklist if len(w) == 6 and freq.get(w, 0) >= 30 and not w.endswith("ND")]
w4 = [w for w in (w50 & dict_words) - blacklist if len(w) == 4 and freq.get(w, 0) >= 30]
w3 = [w for w in (w50 & dict_words) - blacklist if len(w) == 3 and freq.get(w, 0) >= 40]

SET_8 = set(w8)
SET_6 = set(w6)
SET_4 = set(w4)
SET_3 = set(w3)

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

print(f"Loaded pools: w8={len(w8)}, w6={len(w6)}, w4={len(w4)}, w3={len(w3)}")

t0 = time.time()
solutions_9x7 = []
print("Searching clean 9x7 solutions...")

random.seed(42)
w8_pool = list(w8)
random.shuffle(w8_pool)

for c3 in w8_pool[:100]:
    for c4 in w8_pool[:100]:
        if c3 == c4: continue
        
        # r4: (0, ?), (1, ?), (2, c3[3]), (3, c4[3])
        r4_cands = match4([(2, c3[3]), (3, c4[3])])
        if not r4_cands: continue
        
        # r5: (0, c3[4]), (1, c4[4]), (2, ?), (3, ?)
        r5_cands = match4([(0, c3[4]), (1, c4[4])])
        if not r5_cands: continue
        
        for r4 in r4_cands:
            for r5 in r5_cands:
                # Top half:
                # col1_top: ends with r4[0]
                # col2_top: ends with r4[1]
                c1_top_cands = match4([(3, r4[0])])
                c2_top_cands = match4([(3, r4[1])])
                if not c1_top_cands or not c2_top_cands: continue
                
                top_found = []
                for col1_top in c1_top_cands:
                    for col2_top in c2_top_cands:
                        if col1_top == col2_top: continue
                        # Row 1: (0, col1_top[0]), (1, col2_top[0]), (2, c3[0]), (3, c4[0])
                        # Row 2: (0, col1_top[1]), (1, col2_top[1]), (2, c3[1]), (3, c4[1])
                        # Row 3: (0, col1_top[2]), (1, col2_top[2]), (2, c3[2]), (3, c4[2])
                        r1_cands = match6([(0, col1_top[0]), (1, col2_top[0]), (2, c3[0]), (3, c4[0])])
                        r2_cands = match6([(0, col1_top[1]), (1, col2_top[1]), (2, c3[1]), (3, c4[1])])
                        r3_cands = match6([(0, col1_top[2]), (1, col2_top[2]), (2, c3[2]), (3, c4[2])])
                        if not r1_cands or not r2_cands or not r3_cands: continue
                        
                        for r1 in r1_cands:
                            for r2 in r2_cands:
                                for r3 in r3_cands:
                                    if len({r1, r2, r3, col1_top, col2_top}) < 5: continue
                                    col5_top = r1[4] + r2[4] + r3[4]
                                    if col5_top not in SET_3: continue
                                    col6_top = r1[5] + r2[5] + r3[5]
                                    if col6_top not in SET_3 or col6_top == col5_top: continue
                                    
                                    top_words = {r1, r2, r3, r4, col1_top, col2_top, col5_top, col6_top}
                                    if len(top_words) == 8:
                                        top_found.append((r1, r2, r3, col1_top, col2_top, col5_top, col6_top))
                                        break
                                if top_found: break
                            if top_found: break
                        if top_found: break
                    if top_found: break
                    
                if not top_found: continue
                
                # Bottom half:
                # col5_bot: starts with r5[2]
                # col6_bot: starts with r5[3]
                c5_bot_cands = match4([(0, r5[2])])
                c6_bot_cands = match4([(0, r5[3])])
                if not c5_bot_cands or not c6_bot_cands: continue
                
                bot_found = []
                for col5_bot in c5_bot_cands:
                    for col6_bot in c6_bot_cands:
                        if col5_bot == col6_bot: continue
                        # Row 6: (2, c3[5]), (3, c4[5]), (4, col5_bot[1]), (5, col6_bot[1])
                        # Row 7: (2, c3[6]), (3, c4[6]), (4, col5_bot[2]), (5, col6_bot[2])
                        # Row 8: (2, c3[7]), (3, c4[7]), (4, col5_bot[3]), (5, col6_bot[3])
                        r6_cands = match6([(2, c3[5]), (3, c4[5]), (4, col5_bot[1]), (5, col6_bot[1])])
                        r7_cands = match6([(2, c3[6]), (3, c4[6]), (4, col5_bot[2]), (5, col6_bot[2])])
                        r8_cands = match6([(2, c3[7]), (3, c4[7]), (4, col5_bot[3]), (5, col6_bot[3])])
                        if not r6_cands or not r7_cands or not r8_cands: continue
                        
                        for r6 in r6_cands:
                            for r7 in r7_cands:
                                for r8 in r8_cands:
                                    if len({r6, r7, r8, col5_bot, col6_bot}) < 5: continue
                                    col1_bot = r6[0] + r7[0] + r8[0]
                                    if col1_bot not in SET_3: continue
                                    col2_bot = r6[1] + r7[1] + r8[1]
                                    if col2_bot not in SET_3 or col2_bot == col1_bot: continue
                                    
                                    bot_words = {r5, r6, r7, r8, col5_bot, col6_bot, col1_bot, col2_bot}
                                    if len(bot_words) == 8:
                                        bot_found.append((r6, r7, r8, col5_bot, col6_bot, col1_bot, col2_bot))
                                        break
                                if bot_found: break
                            if bot_found: break
                        if bot_found: break
                    if bot_found: break
                    
                if not bot_found: continue
                
                # Combine!
                for top in top_found:
                    for bot in bot_found:
                        r1, r2, r3, col1_top, col2_top, col5_top, col6_top = top
                        r6, r7, r8, col5_bot, col6_bot, col1_bot, col2_bot = bot
                        all_words = [r1, r2, r3, r4, r5, r6, r7, r8, col1_top, col2_top, c3, c4, col5_top, col6_top, col1_bot, col2_bot, col5_bot, col6_bot]
                        if len(set(all_words)) == len(all_words):
                            sol = {
                                "R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6, "R7": r7, "R8": r8,
                                "C1_top": col1_top, "C2_top": col2_top, "C3": c3, "C4": c4,
                                "C5_top": col5_top, "C6_top": col6_top,
                                "C1_bot": col1_bot, "C2_bot": col2_bot, "C5_bot": col5_bot, "C6_bot": col6_bot
                            }
                            solutions_9x7.append(sol)
                            print(f"FOUND 9x7 SOLUTION [{len(solutions_9x7)}] in {time.time()-t0:.2f}s!")
                            for k, v in sol.items():
                                print(f"  {k}: {v} ({dict_display.get(v, v)})")
                            if len(solutions_9x7) >= 5:
                                with open("scripts/clean_9x7_solutions.json", "w", encoding="utf-8") as out:
                                    json.dump(solutions_9x7, out, indent=2, ensure_ascii=False)
                                print("Saved 5 9x7 solutions!")
                                exit(0)

print(f"Done. Found: {len(solutions_9x7)}")
