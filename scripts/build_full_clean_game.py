import unicodedata
from collections import defaultdict
import time
import json
import random
import re

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

# Comprehensive blacklist
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
    'VAL', 'VOS', 'CAM', 'CLA', 'POP', 'RAM', 'PAT', 'SACANA', 'ERECAO', 'PEITOS'
}

w8 = [w for w in (w50 & dict_words) - blacklist if len(w) == 8 and freq.get(w, 0) >= 30]
w6 = [w for w in (w50 & dict_words) - blacklist if len(w) == 6 and freq.get(w, 0) >= 40 and not w.endswith("ND")]
w4 = [w for w in (w50 & dict_words) - blacklist if len(w) == 4 and freq.get(w, 0) >= 40]
w3 = [
    'SOL', 'LUA', 'MAR', 'RIO', 'RUA', 'CEU', 'MEL', 'PAO', 'PAZ', 'LUZ', 'COR', 'SOM',
    'REI', 'MAO', 'FIM', 'ANO', 'ATO', 'ELO', 'ERA', 'SAL', 'ASA', 'UVA', 'OVO', 'ACO',
    'BOA', 'RIR', 'VER', 'DAR', 'SER', 'VOZ', 'BEM', 'CHA', 'DIA', 'DOM', 'LEI', 'PIA',
    'GEL', 'GAS', 'LAR', 'FIO', 'OLA', 'CAO', 'BAU', 'GOL', 'BOI', 'PAI', 'MAE', 'TIO',
    'TIA', 'BOM', 'SIM', 'NAO', 'VOU', 'SOU', 'ELE', 'ELA', 'NEM', 'FAZ', 'FEZ', 'VIU',
    'DIZ', 'FUI', 'FIZ', 'TEM', 'SAO', 'VAI', 'VEM', 'UMA', 'DEZ', 'DOR', 'RIM', 'TOM',
    'TEU', 'MEU', 'SEU', 'AVE', 'BAR', 'VIL', 'VEZ', 'VIA', 'CAL', 'ECO', 'AMA', 'AMO',
    'CEM', 'DOM', 'IDO', 'IDA', 'IRA', 'PAR', 'POR', 'ORA'
]
w2 = [
    'AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA', 'LE',
    'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA',
    'DE', 'EM', 'NA', 'SE', 'AO'
]

SET_8 = set(w8)
SET_6 = set(w6)
SET_4 = set(w4)
SET_3 = set(w3)
SET_2 = set(w2)

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

def match6(constraints, exclude):
    res = None
    for p, ch in constraints:
        s = idx6.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return (res - exclude) if res is not None else (SET_6 - exclude)

def match4(constraints, exclude):
    res = None
    for p, ch in constraints:
        s = idx4.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return (res - exclude) if res is not None else (SET_4 - exclude)

def match3(constraints, exclude):
    res = None
    for p, ch in constraints:
        s = idx3.get((p, ch), set())
        if res is None: res = set(s)
        else: res &= s
        if not res: return set()
    return (res - exclude) if res is not None else (SET_3 - exclude)

def solve_staggered_level(used_words, seed=42):
    random.seed(seed)
    w4_shuffled = list(SET_4 - used_words)
    random.shuffle(w4_shuffled)
    
    for r3 in w4_shuffled:
        c1_cands = match3([(2, r3[0])], used_words)
        c2_cands = match3([(2, r3[1])], used_words)
        if not c1_cands or not c2_cands: continue
        
        for c1_top in c1_cands:
            for c2_top in c2_cands:
                if c1_top == c2_top: continue
                r1_cands = match6([(0, c1_top[0]), (1, c2_top[0])], used_words)
                r2_cands = match6([(0, c1_top[1]), (1, c2_top[1])], used_words)
                if not r1_cands or not r2_cands: continue
                
                for r1 in r1_cands:
                    for r2 in r2_cands:
                        if r1 == r2: continue
                        c5_top = r1[4] + r2[4]
                        if c5_top not in SET_2 or c5_top in used_words: continue
                        c6_top = r1[5] + r2[5]
                        if c6_top not in SET_2 or c6_top in used_words or c6_top == c5_top: continue
                        
                        c3_cands = match6([(0, r1[2]), (1, r2[2]), (2, r3[2])], used_words | {r1, r2})
                        c4_cands = match6([(0, r1[3]), (1, r2[3]), (2, r3[3])], used_words | {r1, r2})
                        if not c3_cands or not c4_cands: continue
                        
                        top_words = {r1, r2, r3, c1_top, c2_top, c5_top, c6_top}
                        if len(top_words) < 7: continue
                        
                        for c3 in c3_cands:
                            for c4 in c4_cands:
                                if c3 == c4 or c3 in top_words or c4 in top_words: continue
                                
                                r4_cands = match4([(0, c3[3]), (1, c4[3])], used_words | top_words | {c3, c4})
                                if not r4_cands: continue
                                
                                for r4 in r4_cands:
                                    c5_cands = match3([(0, r4[2])], used_words | top_words | {c3, c4, r4})
                                    c6_cands = match3([(0, r4[3])], used_words | top_words | {c3, c4, r4})
                                    if not c5_cands or not c6_cands: continue
                                    
                                    for c5_bot in c5_cands:
                                        for c6_bot in c6_cands:
                                            if c5_bot == c6_bot: continue
                                            r5_cands = match6([(2, c3[4]), (3, c4[4]), (4, c5_bot[1]), (5, c6_bot[1])], used_words | top_words | {c3, c4, r4, c5_bot, c6_bot})
                                            r6_cands = match6([(2, c3[5]), (3, c4[5]), (4, c5_bot[2]), (5, c6_bot[2])], used_words | top_words | {c3, c4, r4, c5_bot, c6_bot})
                                            if not r5_cands or not r6_cands: continue
                                            
                                            for r5 in r5_cands:
                                                for r6 in r6_cands:
                                                    if r5 == r6: continue
                                                    c1_bot = r5[0] + r6[0]
                                                    if c1_bot not in SET_2 or c1_bot in used_words or c1_bot in top_words: continue
                                                    c2_bot = r5[1] + r6[1]
                                                    if c2_bot not in SET_2 or c2_bot in used_words or c2_bot in top_words or c2_bot == c1_bot: continue
                                                    
                                                    all_words = [r1, r2, r3, r4, r5, r6, c1_top, c2_top, c3, c4, c5_top, c6_top, c1_bot, c2_bot, c5_bot, c6_bot]
                                                    if len(set(all_words)) == len(all_words):
                                                        return {
                                                            "R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6,
                                                            "C1_top": c1_top, "C2_top": c2_top, "C3": c3, "C4": c4,
                                                            "C5_top": c5_top, "C6_top": c6_top,
                                                            "C1_bot": c1_bot, "C2_bot": c2_bot, "C5_bot": c5_bot, "C6_bot": c6_bot
                                                        }
    return None

def solve_with_retry(used_words, max_attempts=50):
    for attempt in range(max_attempts):
        sol = solve_staggered_level(used_words, seed=attempt * 37 + 13)
        if sol:
            return sol
    return None

print("Solving 3 disjoint 7x7 levels...")
global_used = set()

lvl1_sol = solve_with_retry(global_used)
if not lvl1_sol:
    print("Failed level 1")
    exit(1)
words_1 = set(lvl1_sol.values())
global_used |= {w for w in words_1 if len(w) >= 3}
print("Level 1 solved with words:", sorted(words_1))

lvl2_sol = solve_with_retry(global_used)
if not lvl2_sol:
    print("Failed level 2")
    exit(1)
words_2 = set(lvl2_sol.values())
global_used |= {w for w in words_2 if len(w) >= 3}
print("Level 2 solved with words:", sorted(words_2))

lvl3_sol = solve_with_retry(global_used)
if not lvl3_sol:
    print("Failed level 3")
    exit(1)
words_3 = set(lvl3_sol.values())
global_used |= {w for w in words_3 if len(w) >= 3}
print("Level 3 solved with words:", sorted(words_3))

print("Total words used in 3 levels:", len(global_used))
assert len(global_used) == 48, "Expected 48 unique words!"
print("SUCCESS: 48 completely unique words across Levels 1, 2, and 3!")
