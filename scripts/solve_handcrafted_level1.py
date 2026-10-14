import unicodedata
import random

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    words_6 = set(l.split()[0] for l in f if len(l.split()[0]) == 6)
    words_3 = set(l.split()[0] for l in f if len(l.split()[0]) == 3)
    words_2 = set(l.split()[0] for l in f if len(l.split()[0]) == 2)

# Also load palavras_full
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        c = strip_accents(line.strip())
        if c.isalpha() and len(c) in [2, 3, 6]:
            if len(c) == 2: words_2.add(c)
            elif len(c) == 3: words_3.add(c)
            elif len(c) == 6: words_6.add(c)

# Allowed pure 2-letter words
valid_2 = {"AR", "IR", "VI", "JA", "HA", "SO", "NO", "NA", "DA", "DE", "EM", "UM", "SE", "OU", "LA", "LE", "PE", "PA", "PO", "DO", "RE", "MI", "FA", "SI", "TI", "EU", "AI", "OI", "RA", "MA", "VA", "TA", "VE", "CA", "TU", "NE", "TO", "FE", "LI", "AO"}
valid_3 = {"SOL", "LUA", "MAR", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI", "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR", "VER", "DAR", "SER", "VOZ", "BEM", "SIM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS", "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "VEM", "VAI", "BAR", "BOI", "TIO", "TIA", "AVO", "PAI", "MAE", "GOL", "ORA", "BOM", "TUA", "SEU", "MEU", "VOU", "SOU", "NOS", "DEU", "FOI", "ELE", "ELA", "NEM", "QUE", "FAZ", "FEZ", "VIU", "DIZ", "FUI", "FIZ", "TEM", "SAO", "MIM", "DAS", "DOS", "LHE", "VAO"}

# Let's search all combinations where:
# Col 1 in words_6
# Col 6 in words_6
# Row 1 in words_6
# Row 6 in words_6
# Row 2 in words_6
# Row 5 in words_6
# A3 in valid_2 (3, 1..2)
# A4 in valid_3 (3, 4..6)
# A5 in valid_3 (4, 1..3)
# A6 in valid_2 (4, 5..6)
# D3 in valid_2 (1..2, 3)
# D4 in valid_3 (4..6, 3)
# D5 in valid_3 (1..3, 4)
# D6 in valid_2 (5..6, 4)
# Col 2 in words_6 (1..6, 2)
# Col 5 in words_6 (1..6, 5)

print("Starting ultra-fast search for perfect 7x7 level...")

# Let's test candidate theme anchors for Row 1
theme_anchors = ["BRASIL", "VIAGEM", "PRAIAS", "CIDADE", "AMORES", "NUVENS", "FLORES", "JANTAR", "CINEMA", "TEATRO", "BELEZA", "ALEGRE", "MUSICA", "CHEIRO"]

for r1 in theme_anchors:
    if r1 not in words_6: continue
    # Col 1 must start with r1[0]
    c1_cands = [w for w in words_6 if w[0] == r1[0]]
    # Col 6 must start with r1[5]
    c6_cands = [w for w in words_6 if w[0] == r1[5]]

    random.shuffle(c1_cands)
    random.shuffle(c6_cands)

    for c1 in c1_cands[:40]:
        for c6 in c6_cands[:40]:
            # Row 6 must start with c1[5] and end with c6[5]
            r6_cands = [w for w in words_6 if w[0] == c1[5] and w[5] == c6[5]]
            if not r6_cands: continue

            # A3 must start with c1[2]
            a3_cands = [w for w in valid_2 if w[0] == c1[2]]
            if not a3_cands: continue

            # A5 must start with c1[3]
            a5_cands = [w for w in valid_3 if w[0] == c1[3]]
            if not a5_cands: continue

            # A4 must end with c6[2]
            a4_cands = [w for w in valid_3 if w[2] == c6[2]]
            if not a4_cands: continue

            # A6 must end with c6[3]
            a6_cands = [w for w in valid_2 if w[1] == c6[3]]
            if not a6_cands: continue

            for r6 in r6_cands[:10]:
                for a3 in a3_cands:
                    for a5 in a5_cands:
                        # Check Col 2: (1..6, 2): starts with r1[1], row2[1], a3[1], a5[1], row5[1], r6[1]
                        # Col 2 has char at row 3 = a3[1], row 4 = a5[1]
                        c2_cands = [w for w in words_6 if w[0] == r1[1] and w[2] == a3[1] and w[3] == a5[1] and w[5] == r6[1]]
                        if not c2_cands: continue

                        for a4 in a4_cands:
                            for a6 in a6_cands:
                                # Check Col 5: (1..6, 5): starts with r1[4], row2[4], a4[1], a6[0], row5[4], r6[4]
                                c5_cands = [w for w in words_6 if w[0] == r1[4] and w[2] == a4[1] and w[3] == a6[0] and w[5] == r6[4]]
                                if not c5_cands: continue

                                for c2 in c2_cands[:3]:
                                    for c5 in c5_cands[:3]:
                                        # Check Row 2: starts with c1[1], c2[1], ?, ?, c5[1], c6[1]
                                        # Row 5: starts with c1[4], c2[4], ?, ?, c5[4], c6[4]
                                        # D3: (1..2, 3): r1[2] + row2[2] (must be in valid_2)
                                        # D5: (1..3, 4): r1[3] + row2[3] + a4[0] (must be in valid_3)
                                        # D4: (4..6, 3): a5[2] + row5[2] + r6[2] (must be in valid_3)
                                        # D6: (5..6, 4): row5[3] + r6[3] (must be in valid_2)

                                        # Try D3
                                        d3_cands = [w for w in valid_2 if w[0] == r1[2]]
                                        # Try D5
                                        d5_cands = [w for w in valid_3 if w[0] == r1[3] and w[2] == a4[0]]
                                        if not d3_cands or not d5_cands: continue

                                        for d3 in d3_cands:
                                            r2_char2 = d3[1]
                                            for d5 in d5_cands:
                                                r2_char3 = d5[1]
                                                # Now Row 2 is completely determined!
                                                cand_r2 = c1[1] + c2[1] + r2_char2 + r2_char3 + c5[1] + c6[1]
                                                if cand_r2 not in words_6: continue

                                                # Try D4
                                                d4_cands = [w for w in valid_3 if w[0] == a5[2] and w[2] == r6[2]]
                                                # Try D6
                                                d6_cands = [w for w in valid_2 if w[1] == r6[3]]
                                                if not d4_cands or not d6_cands: continue

                                                for d4 in d4_cands:
                                                    r5_char2 = d4[1]
                                                    for d6 in d6_cands:
                                                        r5_char3 = d6[0]
                                                        # Now Row 5 is completely determined!
                                                        cand_r5 = c1[4] + c2[4] + r5_char2 + r5_char3 + c5[4] + c6[4]
                                                        if cand_r5 not in words_6: continue

                                                        # WE FOUND A COMPLETE FLAWLESS SOLUTION!
                                                        print(f"\n==========================================")
                                                        print(f"FOUND 100% PURE PORTUGUESE SOLUTION!")
                                                        print(f"==========================================")
                                                        print(f"Row 1: {' '.join(r1)}")
                                                        print(f"Row 2: {' '.join(cand_r2)}")
                                                        print(f"Row 3: {c1[2]} {a3[1]} [] {a4[0]} {a4[1]} {c6[2]}")
                                                        print(f"Row 4: {c1[3]} {c2[3]} {a5[2]} [] {a6[0]} {c6[3]}")
                                                        print(f"Row 5: {' '.join(cand_r5)}")
                                                        print(f"Row 6: {' '.join(r6)}")
                                                        print(f"\nWords:")
                                                        print(f"  Across: {r1}, {cand_r2}, {a3}, {a4}, {a5}, {a6}, {cand_r5}, {r6}")
                                                        print(f"  Down: {c1}, {c2}, {d3}, {d4}, {d5}, {d6}, {c5}, {c6}")
                                                        import sys; sys.exit(0)
