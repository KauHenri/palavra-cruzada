import unicodedata
from collections import defaultdict
import time
import json
import random

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# 1. Load dictionary
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

# Master strict blacklist
forbidden = {
    # English / foreign
    'ART', 'ALIENS', 'DORIAN', 'ACE', 'ST', 'EST', 'AM', 'HOME', 'CHAD', 'HORACE',
    'CHET', 'STAN', 'CORNO', 'BITCH', 'COCK', 'PENIS', 'VAGINA', 'SHIT', 'FUCK',
    'DICK', 'DIE', 'MIN', 'DOC', 'TOP', 'DNA', 'DVD', 'CDS', 'CSI', 'HIV', 'GPS',
    'FBI', 'KGB', 'CIA', 'BBC', 'BMW', 'BIG', 'BOX', 'GAY', 'SEX', 'HOT', 'RED',
    'BUS', 'MEN', 'BOY', 'GIRL', 'MAN', 'WAR', 'END', 'CAR', 'CAT', 'DOG', 'SUN',
    'BAD', 'GET', 'RUN', 'LET', 'SAY', 'PUT', 'NEW', 'OLD', 'ONE', 'TWO', 'TEN',
    'FAR', 'HER', 'HIS', 'HIM', 'SHE', 'WHO', 'WHY', 'HOW', 'ALL', 'ANY', 'MAY',
    'WAY', 'DAY', 'OUR', 'NOW', 'OUT', 'OFF', 'PER', 'VINTAGE', 'HALL', 'ISLAND',
    'ICE', 'POP', 'RAM', 'PAT', 'BANG', 'BEST', 'HEM', 'HAN', 'HONG', 'ROBE',
    'SECTOR', 'VECTOR', 'BAR', 'PUB', 'SHOW', 'SITE', 'WEB', 'APP', 'LINK',
    'POST', 'FEED', 'CHAT', 'EMAIL', 'MAIL', 'BYTE', 'BIT', 'PIXEL', 'CHIP',
    'ROCK', 'JAZZ', 'BLUES', 'PUNK', 'RAP', 'FUNK', 'METAL', 'DISCO', 'DJ',
    # Weird / archaic / slang / names
    'SA', 'ADA', 'ARI', 'ME', 'BELMAZ', 'ZORAIA', 'RUEIRO', 'LOROSA', 'ARATUS',
    'ICAPUI', 'TA', 'SI', 'TI', 'DUMA', 'LIONEL', 'DALE', 'ESTEREIS', 'ALOMORFO',
    'BENJAMIN', 'CAMARA', 'OURESCER', 'IGDLOITA', 'ARARAI', 'MATESE', 'AMICAL',
    'MADRIA', 'ERGUER', 'SOIOTO', 'MAMILO', 'ANAS', 'JIRO', 'OTAN', 'RAMONA',
    'ARGO', 'TOTO', 'ASIM', 'NAOS', 'LOIRAS', 'LOIROS', 'ZELOSO', 'ARSENICO',
    'UNOS', 'MICADO', 'AMADAS', 'CAMADA', 'TAMA', 'AMAL', 'MEBOSA', 'OLOFRO',
    'MARIACHI', 'MARISA', 'ELISSA', 'LAOS', 'IVES', 'ALAN', 'DAMIEN', 'ERIC',
    'NERO', 'MARI', 'ARIA', 'ALF', 'ABI', 'ABU', 'AHN', 'ARE', 'DEA', 'DUM',
    'ECA', 'ELI', 'GIL', 'GOA', 'LEO', 'PAU', 'PUS', 'RAI', 'RUM', 'SOS', 'UNA',
    'VAL', 'VOS', 'CAM', 'CLA', 'SACANA', 'ERECAO', 'PEITOS', 'MANE', 'MORE',
    'MOLE', 'CACADA', 'CIGANA', 'REATOR', 'REITOR', 'EUROPA', 'ELAINE', 'ROUPAO',
    'APACHE', 'GIBI', 'PIVE', 'GAFE', 'SEITA', 'TETA', 'ZUREA', 'ABADE',
    # Obscure 3-letter combos
    'ATO', 'UTA', 'APU', 'ETA', 'OTO', 'UFO', 'AXE', 'BAU', 'BIA',
    'BOI', 'BUA', 'CIA', 'DOM', 'DON', 'DUO', 'EIA', 'EMA',
    'EPA', 'ETA', 'EVA', 'GEO', 'GIA', 'GUA', 'HEI', 'IAO',
    'IDA', 'IMO', 'INA', 'IRA', 'ITA', 'ITU', 'IUA', 'IVA', 'IZA', 'JUS', 'LAO',
    'LIA', 'MEO', 'MIA', 'MIO', 'MOA', 'MOI', 'MUA', 'NEO', 'NIA',
    'NOA', 'NOI', 'NUA', 'OBA', 'OCA', 'ODA', 'ODE', 'OIA', 'OLE', 'OPA',
    'ORO', 'OSA', 'OTO', 'OVA', 'PAN', 'PIA', 'PIO',
    'POA', 'POI', 'PUM', 'QUA', 'RAD', 'RAI', 'RAO', 'ROA',
    'ROU', 'RUI', 'SED', 'SEI', 'SEN', 'SIA', 'SIO',
    'SOA', 'SOB', 'SOI', 'TAI', 'TAO', 'TEO',
    'TOA', 'TRI', 'TUI', 'UBA', 'UIA', 'UIS', 'UJA',
    'UMA', 'UNI', 'URA', 'URI', 'USA', 'USO', 'VEE',
    'VEO', 'VIO', 'VIS', 'VIU', 'ZUM',
    'AGI', 'AGU', 'AIA', 'ALU', 'ANI', 'ANU', 'APO', 'ARI', 'ARU',
    'ATI', 'AVO', 'AZA', 'AZI', 'BAL', 'BEI', 'BEL', 'BES', 'BIM',
    'BIS', 'BOA', 'BOB', 'BOI', 'BOM', 'BON', 'BOR', 'BOU', 'BRA',
    'BRE', 'BRI', 'BRO', 'BRU', 'BUA', 'BUE', 'BUI', 'BUL', 'BUR'
}

# Clean, familiar 3-letter words only
ALLOWED_3 = {
    'DAR', 'VER', 'PAZ', 'LUZ', 'SOL', 'MAR', 'CEU', 'LUA', 'SOM', 'COR', 'VOZ',
    'RUA', 'RIO', 'REI', 'LEI', 'MEL', 'DIA', 'PAI', 'MAE', 'TIO', 'TIA', 'OVO',
    'UVA', 'PAR', 'ASA', 'ECO', 'BEM', 'MAL', 'SIM', 'NAO', 'NEM', 'ATE', 'ORA',
    'BOA', 'VAI', 'VEM', 'OLA', 'SAO', 'FIM', 'SER', 'TER', 'TEM', 'VAI', 'FOI',
    'DEU', 'DOU', 'VIU', 'LEU', 'CRU', 'ATO', 'ANO', 'CEM', 'MIL', 'DEZ', 'SEU',
    'SUA', 'TEU', 'TUA', 'MEU', 'MIA', 'NOS', 'VOS', 'ELE', 'ELA'
} - forbidden

# Clean, familiar 2-letter words only (grammatical function words)
ALLOWED_2 = {
    'AR', 'IR', 'PO', 'PE', 'PA', 'FE', 'LA', 'NO', 'DO', 'RE', 'FA',
    'OI', 'EU', 'TU', 'UM', 'JA', 'HA', 'SO', 'AI', 'VA', 'VE', 'CA', 'DA',
    'DE', 'EM', 'NA', 'SE', 'AO'
}

# 6-letter pool: highly frequent, no gerunds (NDO), clean
w6 = [w for w in (w50 & dict_words) - forbidden if len(w) == 6 and freq.get(w, 0) >= 60 and not w.endswith("NDO") and not w.endswith("ND")]
# 4-letter pool: highly frequent, clean
w4 = [w for w in (w50 & dict_words) - forbidden if len(w) == 4 and freq.get(w, 0) >= 60]
# 3-letter pool:
w3 = [w for w in ALLOWED_3 if w in dict_words]

print(f"Pool sizes: w6={len(w6)}, w4={len(w4)}, w3={len(w3)}, w2={len(ALLOWED_2)}")

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

t0 = time.time()
found_grids = []

# Search
for r3 in sorted(w4, key=lambda w: -freq.get(w, 0)):
    c1_cands = match3([(2, r3[0])])
    c2_cands = match3([(2, r3[1])])
    if not c1_cands or not c2_cands: continue
    
    for c1_top in c1_cands:
        for c2_top in c2_cands:
            r1_cands = match6([(0, c1_top[0]), (1, c2_top[0])])
            r2_cands = match6([(0, c1_top[1]), (1, c2_top[1])])
            if not r1_cands or not r2_cands: continue
            
            for r1 in r1_cands:
                for r2 in r2_cands:
                    c5_top = r1[4] + r2[4]
                    if c5_top not in ALLOWED_2: continue
                    c6_top = r1[5] + r2[5]
                    if c6_top not in ALLOWED_2: continue
                    
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
                                        r5_cands = match6([(2, c3[4]), (3, c4[4]), (4, c5_bot[1]), (5, c6_bot[1])])
                                        r6_cands = match6([(2, c3[5]), (3, c4[5]), (4, c5_bot[2]), (5, c6_bot[2])])
                                        if not r5_cands or not r6_cands: continue
                                        
                                        for r5 in r5_cands:
                                            for r6 in r6_cands:
                                                c1_bot = r5[0] + r6[0]
                                                if c1_bot not in ALLOWED_2: continue
                                                c2_bot = r5[1] + r6[1]
                                                if c2_bot not in ALLOWED_2: continue
                                                
                                                all_words = [r1, r2, r3, r4, r5, r6, c1_top, c2_top, c3, c4, c5_top, c6_top, c1_bot, c2_bot, c5_bot, c6_bot]
                                                if len(set(all_words)) == len(all_words):
                                                    grid_sol = {
                                                        "R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6,
                                                        "C1_top": c1_top, "C2_top": c2_top, "C3": c3, "C4": c4,
                                                        "C5_top": c5_top, "C6_top": c6_top,
                                                        "C1_bot": c1_bot, "C2_bot": c2_bot, "C5_bot": c5_bot, "C6_bot": c6_bot
                                                    }
                                                    found_grids.append(grid_sol)
                                                    print(f"Found grid #{len(found_grids)}: R1={r1}, R2={r2}, R3={r3}, R4={r4}, R5={r5}, R6={r6}")
                                                    if len(found_grids) >= 50:
                                                        with open("scripts/pure_staggered_50.json", "w", encoding="utf-8") as out:
                                                            json.dump(found_grids, out, indent=2, ensure_ascii=False)
                                                        print(f"Saved 50 pure solutions in {time.time()-t0:.2f}s!")
                                                        exit(0)

print(f"Finished search. Found: {len(found_grids)}")
with open("scripts/pure_staggered_50.json", "w", encoding="utf-8") as out:
    json.dump(found_grids, out, indent=2, ensure_ascii=False)
