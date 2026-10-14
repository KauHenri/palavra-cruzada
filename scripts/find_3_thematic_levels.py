import unicodedata
import random
import sys

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    words_6 = set(l.split()[0] for l in f if len(l.split()[0]) == 6)

with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        c = strip_accents(line.strip())
        if c.isalpha() and len(c) == 6:
            words_6.add(c)

valid_2 = {"AR", "IR", "VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "LE", "PE", "PA", "PO", "DO", "RE", "MI", "FA", "SI", "TI", "EU", "AI", "OI", "RA", "MA", "VA", "TA", "VE", "CA", "TU", "NE", "TO", "FE", "LI", "AO"}
valid_3 = {"SOL", "LUA", "MAR", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "SIM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "TIA", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "MIM", "DAS", "DOS", "LHE", "VAO"}

def find_level_for_theme(theme_word):
    r1 = theme_word
    c1_cands = [w for w in words_6 if w[0] == r1[0]]
    c6_cands = [w for w in words_6 if w[0] == r1[5]]

    random.shuffle(c1_cands)
    random.shuffle(c6_cands)

    for c1 in c1_cands[:50]:
        for c6 in c6_cands[:50]:
            r6_cands = [w for w in words_6 if w[0] == c1[5] and w[5] == c6[5]]
            if not r6_cands: continue

            a3_cands = [w for w in valid_2 if w[0] == c1[2]]
            if not a3_cands: continue

            a5_cands = [w for w in valid_3 if w[0] == c1[3]]
            if not a5_cands: continue

            a4_cands = [w for w in valid_3 if w[2] == c6[2]]
            if not a4_cands: continue

            a6_cands = [w for w in valid_2 if w[1] == c6[3]]
            if not a6_cands: continue

            for r6 in r6_cands[:8]:
                for a3 in a3_cands:
                    for a5 in a5_cands:
                        c2_cands = [w for w in words_6 if w[0] == r1[1] and w[2] == a3[1] and w[3] == a5[1] and w[5] == r6[1]]
                        if not c2_cands: continue

                        for a4 in a4_cands:
                            for a6 in a6_cands:
                                c5_cands = [w for w in words_6 if w[0] == r1[4] and w[2] == a4[1] and w[3] == a6[0] and w[5] == r6[4]]
                                if not c5_cands: continue

                                for c2 in c2_cands[:3]:
                                    for c5 in c5_cands[:3]:
                                        d3_cands = [w for w in valid_2 if w[0] == r1[2]]
                                        d5_cands = [w for w in valid_3 if w[0] == r1[3] and w[2] == a4[0]]
                                        if not d3_cands or not d5_cands: continue

                                        for d3 in d3_cands:
                                            r2_char2 = d3[1]
                                            for d5 in d5_cands:
                                                r2_char3 = d5[1]
                                                cand_r2 = c1[1] + c2[1] + r2_char2 + r2_char3 + c5[1] + c6[1]
                                                if cand_r2 not in words_6: continue

                                                d4_cands = [w for w in valid_3 if w[0] == a5[2] and w[2] == r6[2]]
                                                d6_cands = [w for w in valid_2 if w[1] == r6[3]]
                                                if not d4_cands or not d6_cands: continue

                                                for d4 in d4_cands:
                                                    r5_char2 = d4[1]
                                                    for d6 in d6_cands:
                                                        r5_char3 = d6[0]
                                                        cand_r5 = c1[4] + c2[4] + r5_char2 + r5_char3 + c5[4] + c6[4]
                                                        if cand_r5 not in words_6: continue

                                                        # Success!
                                                        return {
                                                            "theme": r1,
                                                            "rows": [
                                                                r1,
                                                                cand_r2,
                                                                f"{c1[2]}{a3[1]}[]{a4[0]}{a4[1]}{c6[2]}",
                                                                f"{c1[3]}{c2[3]}{a5[2]}[]{a6[0]}{c6[3]}",
                                                                cand_r5,
                                                                r6
                                                            ],
                                                            "across": [r1, cand_r2, a3, a4, a5, a6, cand_r5, r6],
                                                            "down": [c1, c2, d3, d4, d5, d6, c5, c6]
                                                        }
    return None

themes = ["PRAIAS", "AMORES", "CINEMA", "COMIDA", "NUVENS"]
for t in themes:
    print(f"Searching for level anchored at '{t}'...")
    res = find_level_for_theme(t)
    if res:
        print(f"--> FOUND LEVEL FOR {t}!")
        for row in res["rows"]:
            print(f"    {row}")
        print(f"    Across: {res['across']}")
        print(f"    Down: {res['down']}\n")
    else:
        print(f"--> No level found for {t} in subset.")
