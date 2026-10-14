import json

# Compile and validate 3 authentic Brazilian Swedish Crosswords (Cruzadas Diretas)
# Grid: 9 rows x 7 cols each

def build_level(id_num, title, subtitle, theme, rows, cols, raw_grid, clues_map, words_meta):
    grid = []
    for r in range(rows):
        grid_row = []
        for c in range(cols):
            val = raw_grid[r][c]
            if val == "EMPTY":
                grid_row.append({"type": "empty"})
            elif val == "CLUE":
                key = (r, c)
                if key not in clues_map:
                    raise Exception(f"L{id_num}: Missing clue at ({r}, {c})")
                grid_row.append({
                    "type": "clue",
                    "clues": clues_map[key]
                })
            else:
                grid_row.append({
                    "type": "letter",
                    "solution": val,
                    "displayChar": val,
                    "currentLetter": None,
                    "isLocked": False,
                    "confirmedBy": None,
                    "wordIds": []
                })
        grid.append(grid_row)

    words_list = []
    for w in words_meta:
        w_clean = w["word"].upper()
        w_len = len(w_clean)
        w_id = w["id"]
        sr, sc = w["startRow"], w["startCol"]
        direction = w["direction"]

        for i in range(w_len):
            r = sr + i if direction == "down" else sr
            c = sc + i if direction == "right" else sc

            if r >= rows or c >= cols:
                raise Exception(f"L{id_num}: word '{w['word']}' goes out of bounds ({r}, {c})")

            cell = grid[r][c]
            if cell["type"] != "letter":
                raise Exception(f"L{id_num}: word '{w['word']}' letter {i} expects letter at ({r}, {c}), found {cell['type']}")

            if cell["solution"] != w_clean[i]:
                raise Exception(f"L{id_num}: collision in '{w['word']}' at ({r}, {c}): expected '{w_clean[i]}', cell has '{cell['solution']}'")

            cell["wordIds"].append(w_id)

        words_list.append({
            "id": w_id,
            "word": w_clean,
            "displayWord": w.get("displayWord", w_clean),
            "direction": direction,
            "startRow": sr,
            "startCol": sc,
            "clueText": w["clueText"],
            "clueRow": w["clueRow"],
            "clueCol": w["clueCol"],
            "icon": w.get("icon")
        })

    # Verify letter coverage
    letter_count = 0
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if cell["type"] == "letter":
                letter_count += 1
                if len(cell["wordIds"]) == 0:
                    raise Exception(f"L{id_num}: orphan letter cell at ({r}, {c}) with '{cell['solution']}'")

    print(f"[OK] Level {id_num}: {title} - {subtitle} ({rows}x{cols}) | {len(words_list)} palavras | {letter_count} letras")
    return {
        "id": id_num,
        "title": title,
        "subtitle": subtitle,
        "theme": theme,
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "words": words_list
    }

levels = []

# =========================================================================
# LEVEL 1: QUEBRA-CABEÇA 18 (DO PRINT DO USUÁRIO)
# =========================================================================
raw_grid_1 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "A",    "D",    "E",    "P",    "T",    "O"   ],
    ["CLUE",  "D",    "CLUE", "P",    "R",    "O",    "L"   ],
    ["CLUE",  "O",    "C",    "CLUE", "O",    "P",    "I"   ],
    ["CLUE",  "R",    "O",    "P",    "CLUE", "A",    "V"   ],
    ["CLUE",  "A",    "L",    "E",    "G",    "R",    "E"   ],
    ["CLUE",  "V",    "A",    "R",    "A",    "CLUE", "I"   ],
    ["CLUE",  "E",    "D",    "U",    "CLUE", "A",    "R"   ],
    ["CLUE",  "L",    "A",    "CLUE", "R",    "U",    "A"   ]
]

clues_map_1 = {
    (0, 1): [{"text": "AGRADÁVEL", "direction": "down"}],
    (0, 2): [{"text": "DISTRITO", "direction": "down"}],
    (0, 3): [{"text": "cr-🥞-e", "direction": "down"}],
    (0, 4): [{"text": "PROFISSIONAL", "direction": "down"}],
    (0, 5): [{"text": "DAR DE CARA", "direction": "down"}],
    (0, 6): [{"text": "ÁRVORE AZEITONA", "direction": "down"}],

    (1, 0): [{"text": "SEGUE DOUTRINA", "direction": "right"}],
    (2, 0): [{"text": "APÓS LETRA C", "direction": "right"}],
    (2, 2): [
        {"text": "EM BENEFÍCIO", "direction": "right"},
        {"text": "GRUDADA", "direction": "down"}
    ],
    (3, 0): [{"text": "c-🪶-ar", "direction": "right"}],
    (3, 3): [
        {"text": "__NIÃO", "direction": "right"},
        {"text": "AVE NATALINA", "direction": "down"}
    ],
    (4, 0): [{"text": "AP__RIAR", "direction": "right"}],
    (4, 4): [
        {"text": "AVIAÇÃO", "direction": "right"},
        {"text": "SÍMBOLO GÁLIO", "direction": "down"}
    ],
    (5, 0): [{"text": "FELIZ", "direction": "right"}],
    (6, 0): [{"text": "🎣", "direction": "right"}],
    (6, 5): [
        {"text": "3ª LETRA VOGAL", "direction": "right"},
        {"text": "SOM DO LATIDO", "direction": "down"}
    ],
    (7, 0): [{"text": "EDUCAÇÃO", "direction": "right"}],
    (7, 4): [
        {"text": "ARGÔNIO", "direction": "right"},
        {"text": "18ª LETRA", "direction": "down"}
    ],
    (8, 0): [{"text": "ALI", "direction": "right"}],
    (8, 3): [{"text": "VIA URBANA", "direction": "right"}]
}

words_meta_1 = [
    {"id": "w1_1", "word": "ADORAVEL", "displayWord": "ADORÁVEL", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "AGRADÁVEL", "clueRow": 0, "clueCol": 1},
    {"id": "w1_2", "word": "D", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "DISTRITO", "clueRow": 0, "clueCol": 2},
    {"id": "w1_3", "word": "EP", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "cr-🥞-e", "clueRow": 0, "clueCol": 3},
    {"id": "w1_4", "word": "PRO", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "PROFISSIONAL", "clueRow": 0, "clueCol": 4},
    {"id": "w1_5", "word": "TOPAR", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "DAR DE CARA", "clueRow": 0, "clueCol": 5},
    {"id": "w1_6", "word": "OLIVEIRA", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "ÁRVORE AZEITONA", "clueRow": 0, "clueCol": 6},
    {"id": "w1_7", "word": "COLADA", "direction": "down", "startRow": 3, "startCol": 2, "clueText": "GRUDADA", "clueRow": 2, "clueCol": 2},
    {"id": "w1_8", "word": "PERU", "direction": "down", "startRow": 4, "startCol": 3, "clueText": "AVE NATALINA", "clueRow": 3, "clueCol": 3},
    {"id": "w1_9", "word": "GA", "direction": "down", "startRow": 5, "startCol": 4, "clueText": "SÍMBOLO GÁLIO", "clueRow": 4, "clueCol": 4},
    {"id": "w1_10", "word": "R", "direction": "down", "startRow": 8, "startCol": 4, "clueText": "18ª LETRA", "clueRow": 7, "clueCol": 4},
    {"id": "w1_11", "word": "AU", "direction": "down", "startRow": 7, "startCol": 5, "clueText": "SOM DO LATIDO", "clueRow": 6, "clueCol": 5},
    {"id": "w1_12", "word": "ADEPTO", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "SEGUE DOUTRINA", "clueRow": 1, "clueCol": 0},
    {"id": "w1_13", "word": "D", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "APÓS LETRA C", "clueRow": 2, "clueCol": 0},
    {"id": "w1_14", "word": "PROL", "direction": "right", "startRow": 2, "startCol": 3, "clueText": "EM BENEFÍCIO", "clueRow": 2, "clueCol": 2},
    {"id": "w1_15", "word": "OC", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "c-🪶-ar", "clueRow": 3, "clueCol": 0},
    {"id": "w1_16", "word": "OPI", "direction": "right", "startRow": 3, "startCol": 4, "clueText": "__NIÃO", "clueRow": 3, "clueCol": 3},
    {"id": "w1_17", "word": "ROP", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "AP__RIAR", "clueRow": 4, "clueCol": 0},
    {"id": "w1_18", "word": "AV", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "AVIAÇÃO", "clueRow": 4, "clueCol": 4},
    {"id": "w1_19", "word": "ALEGRE", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "FELIZ", "clueRow": 5, "clueCol": 0},
    {"id": "w1_20", "word": "VARA", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "🎣", "clueRow": 6, "clueCol": 0},
    {"id": "w1_21", "word": "I", "direction": "right", "startRow": 6, "startCol": 6, "clueText": "3ª LETRA VOGAL", "clueRow": 6, "clueCol": 5},
    {"id": "w1_22", "word": "EDU", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "EDUCAÇÃO", "clueRow": 7, "clueCol": 0},
    {"id": "w1_23", "word": "AR", "direction": "right", "startRow": 7, "startCol": 5, "clueText": "ARGÔNIO", "clueRow": 7, "clueCol": 4},
    {"id": "w1_24", "word": "LA", "displayWord": "LÁ", "direction": "right", "startRow": 8, "startCol": 1, "clueText": "ALI", "clueRow": 8, "clueCol": 0},
    {"id": "w1_25", "word": "RUA", "direction": "right", "startRow": 8, "startCol": 4, "clueText": "VIA URBANA", "clueRow": 8, "clueCol": 3}
]

levels.append(build_level(1, "Quebra-cabeça 18", "O Desafio do Print", "Paris & Conhecimentos", 9, 7, raw_grid_1, clues_map_1, words_meta_1))


# =========================================================================
# LEVEL 2: QUEBRA-CABEÇA 19 - NATUREZA & ANIMAIS (9 rows x 7 cols)
# Authentic Swedish layout with interior clues!
# Col 1: P-A-S-S-A-R-O-S (8 letters: PÁSSAROS)
# Col 6: F-L-O-R-E-S-T-A (8 letters: FLORESTA)
# Row 1: P-A-R-Q-U-F? (1,6 is F from FLORESTA!)
# If (1, 5) is CLUE: (1, 1..4): P-E-I-X (4)? P-A-T-O (PATO: c1..c4: (1,1)=P, (1,2)=A, (1,3)=T, (1,4)=O)!
# (1, 5) = CLUE!
# (1, 6) = F!
# =========================================================================
raw_grid_2 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "P",    "A",    "T",    "O",    "CLUE", "F"   ],
    ["CLUE",  "A",    "CLUE", "O",    "R",    "A",    "L"   ],
    ["CLUE",  "S",    "O",    "CLUE", "C",    "A",    "O"   ],
    ["CLUE",  "S",    "V",    "A",    "CLUE", "U",    "R"   ],
    ["CLUE",  "A",    "O",    "M",    "E",    "L",    "E"   ],
    ["CLUE",  "R",    "CLUE", "O",    "L",    "CLUE", "S"   ],
    ["CLUE",  "O",    "S",    "R",    "CLUE", "S",    "T"   ],
    ["CLUE",  "S",    "E",    "CLUE", "L",    "U",    "A"   ]
]

# Let's verify every letter in raw_grid_2:
# Col 1: (1..8, 1): P-A-S-S-A-R-O-S = PASSAROS (8 letters down)
# Col 6: (1..8, 6): F-L-O-R-E-S-T-A = FLORESTA (8 letters down)
# Col 2:
# (1, 2) = A (from PATO)
# (3..5, 2): O-V-O = OVO! (3 letters down)
# (7..8, 2): S-E = SE! (2 letters down)
# Col 3:
# (1..2, 3): T-O = TÓ! (To)
# (4..7, 3): A-M-O-R = AMOR! (4 letters down)
# Col 4:
# (2..3, 4): R-C? No.
# Let's adjust col 4 and 5 so all down and across words are 100% dictionary words:
# Look at Col 4:
# (2, 4) = R, (3, 4) = O -> R - O = RÓ (Letra grega)!
# (5..8, 4): E - L - ? - L?
# What if (2, 4)=U, (3, 4)=M -> U - M (UM, numeral 1)?
# What if (5..8, 4) = E - L - O - S (ELOS, ligações de corrente)?
# Then (5,4)=E, (6,4)=L, (7,4)=O, (8,4)=S!
# Look at that: E - L - O - S = ELOS!
# And Row 8 across: (8, 4)=S, (8, 5)=O, (8, 6)=L -> S - O - L = SOL!
# And (8, 1)=S, (8, 2)=E -> S - E = SE!
# And Col 5: (2, 5)=A, (3, 5)=A, (4, 5)=U, (5, 5)=L, (7, 5)=S, (8, 5)=O:
# If Col 5 (2..5, 5) = A - U - L - A = AULA! (4 letters down)
# Look at that: A - U - L - A = AULA!
# (2, 5) = A
# (3, 5) = U
# (4, 5) = L
# (5, 5) = A
# A - U - L - A = AULA!
# And Row 5 across: (5, 1)=A, (5, 2)=O, (5, 3)=M, (5, 4)=E, (5, 5)=A, (5, 6)=E?
# What if Row 5 is: (5, 1)=A, (5, 2)=L, (5, 3)=E, (5, 4)=G, (5, 5)=R, (5, 6)=E -> ALEGRE!
# Then (5, 4)=G, (5, 5)=R, (5, 6)=E (matches FLORESTA's 'E' at row 5!)
# And Col 4 down: (5, 4)=G, (6, 4)=A, (7, 4)=T, (8, 4)=O -> G - A - T - O = GATO!
# GATO down! (4 letters down)
# And Col 5 down: (5, 5)=R, (6, 5)=U, (7, 5)=A -> R - U - A = RUA!
# RUA down! (3 letters down)
# And Col 2 down: (1, 2)=A, (2, 2)=CLUE, (3..5, 2)=O-L-A = OLÁ! (3 letters down)
# And Col 3 down: (1..2, 3)=T-E = TE, (3, 3)=CLUE, (4..7, 3)=M-E-L-O = MELO! Or M-E-L (MEL)!

print("Validating refined matrix...")
