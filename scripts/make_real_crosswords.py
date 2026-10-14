import json

def make_crossword(id_num, title, subtitle, theme, rows, cols, raw_grid, clues_map, words_meta):
    grid = []
    for r in range(rows):
        grid_row = []
        for c in range(cols):
            cell_val = raw_grid[r][c]
            if cell_val == "EMPTY":
                grid_row.append({"type": "empty"})
            elif cell_val == "CLUE":
                key = (r, c)
                if key not in clues_map:
                    raise Exception(f"Missing clue definition for ({r}, {c}) in Level {id_num}")
                grid_row.append({
                    "type": "clue",
                    "clues": clues_map[key]
                })
            else:
                grid_row.append({
                    "type": "letter",
                    "solution": cell_val,
                    "displayChar": cell_val,
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
        dir_name = w["direction"]

        for i in range(w_len):
            r = sr + i if dir_name == "down" else sr
            c = sc + i if dir_name == "right" else sc

            if r >= rows or c >= cols:
                raise Exception(f"L{id_num}: word {w['word']} out of bounds at ({r}, {c})")

            cell = grid[r][c]
            if cell["type"] != "letter":
                raise Exception(f"L{id_num}: word {w['word']} expects letter at ({r}, {c}), got {cell['type']}")

            if cell["solution"] != w_clean[i]:
                raise Exception(f"L{id_num}: mismatch for {w['word']} at ({r}, {c}): expected '{w_clean[i]}', cell has '{cell['solution']}'")

            cell["wordIds"].append(w_id)

        words_list.append({
            "id": w_id,
            "word": w_clean,
            "displayWord": w.get("displayWord", w_clean),
            "direction": dir_name,
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
                    raise Exception(f"L{id_num}: orphan letter cell at ({r}, {c}) with letter '{cell['solution']}'")

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

# =========================================================================
# LEVEL 1: O QUEBRA-CABEÇA 18 DO PRINT
# =========================================================================
raw_grid_18 = [
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

clues_map_18 = {
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

words_meta_18 = [
    # Down words
    {"id": "w1", "word": "ADORAVEL", "displayWord": "ADORÁVEL", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "AGRADÁVEL", "clueRow": 0, "clueCol": 1},
    {"id": "w2", "word": "D", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "DISTRITO", "clueRow": 0, "clueCol": 2},
    {"id": "w3", "word": "EP", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "cr-🥞-e", "clueRow": 0, "clueCol": 3},
    {"id": "w4", "word": "PRO", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "PROFISSIONAL", "clueRow": 0, "clueCol": 4},
    {"id": "w5", "word": "TOPAR", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "DAR DE CARA", "clueRow": 0, "clueCol": 5},
    {"id": "w6", "word": "OLIVEIRA", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "ÁRVORE AZEITONA", "clueRow": 0, "clueCol": 6},
    {"id": "w7", "word": "COLADA", "direction": "down", "startRow": 3, "startCol": 2, "clueText": "GRUDADA", "clueRow": 2, "clueCol": 2},
    {"id": "w8", "word": "PERU", "direction": "down", "startRow": 4, "startCol": 3, "clueText": "AVE NATALINA", "clueRow": 3, "clueCol": 3},
    {"id": "w9", "word": "GA", "direction": "down", "startRow": 5, "startCol": 4, "clueText": "SÍMBOLO GÁLIO", "clueRow": 4, "clueCol": 4},
    {"id": "w10", "word": "R", "direction": "down", "startRow": 8, "startCol": 4, "clueText": "18ª LETRA", "clueRow": 7, "clueCol": 4},
    {"id": "w11", "word": "AU", "direction": "down", "startRow": 7, "startCol": 5, "clueText": "SOM DO LATIDO", "clueRow": 6, "clueCol": 5},

    # Across words
    {"id": "w12", "word": "ADEPTO", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "SEGUE DOUTRINA", "clueRow": 1, "clueCol": 0},
    {"id": "w13", "word": "D", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "APÓS LETRA C", "clueRow": 2, "clueCol": 0},
    {"id": "w14", "word": "PROL", "direction": "right", "startRow": 2, "startCol": 3, "clueText": "EM BENEFÍCIO", "clueRow": 2, "clueCol": 2},
    {"id": "w15", "word": "OC", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "c-🪶-ar", "clueRow": 3, "clueCol": 0},
    {"id": "w16", "word": "OPI", "direction": "right", "startRow": 3, "startCol": 4, "clueText": "__NIÃO", "clueRow": 3, "clueCol": 3},
    {"id": "w17", "word": "ROP", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "AP__RIAR", "clueRow": 4, "clueCol": 0},
    {"id": "w18", "word": "AV", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "AVIAÇÃO", "clueRow": 4, "clueCol": 4},
    {"id": "w19", "word": "ALEGRE", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "FELIZ", "clueRow": 5, "clueCol": 0},
    {"id": "w20", "word": "VARA", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "🎣", "clueRow": 6, "clueCol": 0},
    {"id": "w21", "word": "I", "direction": "right", "startRow": 6, "startCol": 6, "clueText": "3ª LETRA VOGAL", "clueRow": 6, "clueCol": 5},
    {"id": "w22", "word": "EDU", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "EDUCAÇÃO", "clueRow": 7, "clueCol": 0},
    {"id": "w23", "word": "AR", "direction": "right", "startRow": 7, "startCol": 5, "clueText": "ARGÔNIO", "clueRow": 7, "clueCol": 4},
    {"id": "w24", "word": "LA", "displayWord": "LÁ", "direction": "right", "startRow": 8, "startCol": 1, "clueText": "ALI", "clueRow": 8, "clueCol": 0},
    {"id": "w25", "word": "RUA", "direction": "right", "startRow": 8, "startCol": 4, "clueText": "VIA URBANA", "clueRow": 8, "clueCol": 3}
]

lvl1 = make_crossword(1, "Quebra-cabeça 18", "O Desafio do Print", "Paris & Conhecimentos", 9, 7, raw_grid_18, clues_map_18, words_meta_18)

# =========================================================================
# LEVEL 2: QUEBRA-CABEÇA 19 - VIAGEM & MUNDO (7x8)
# Authentic Cruzadas Diretas with interior clues!
# =========================================================================
# Rows: 8, Cols: 7
# Col 6 down: PORTUGAL (8 letters, r0..r7 or r1..r7: 7 letters: FRANCA? B-R-A-S-I-L (6))
# Let's design 8 rows x 7 cols:
raw_grid_19 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"], # Row 0
    ["CLUE",  "P",    "A",    "R",    "I",    "S",    "B"   ], # Row 1: PARIS, B
    ["CLUE",  "A",    "CLUE", "O",    "L",    "A",    "R"   ], # Row 2: A, OLA, R
    ["CLUE",  "S",    "O",    "CLUE", "H",    "A",    "A"   ], # Row 3: SO, HA, A
    ["CLUE",  "S",    "U",    "L",    "CLUE", "M",    "S"   ], # Row 4: SUL, M, S
    ["CLUE",  "E",    "R",    "A",    "M",    "O",    "I"   ], # Row 5: ERAM, O, I
    ["CLUE",  "I",    "O",    "CLUE", "A",    "R",    "L"   ], # Row 6: IO, AR, L
    ["CLUE",  "O",    "CLUE", "M",    "A",    "R",    "CLUE"]  # Row 7: O, MAR
]

# Let's check words in 19:
# Col 1: (1..7, 1): P-A-S-S-E-I-O -> PASSEIO! ("Caminhada turística")
# Col 2: (3..6, 2): O-U-R-O -> OURO! ("Metal precioso")
# Col 3: (1..2, 3): R-O -> RO? Or (4..5, 3): L-A -> LÁ!
# Col 4: (1..2, 4): I-L -> IL? (5..7, 4): M-A-A?
# Let's design another mathematically verified grid in a second script so it's 100% sound.
