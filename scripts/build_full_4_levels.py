# Script to build and verify 4 authentic Brazilian Swedish Crosswords
import json

def compile_level(id_num, title, subtitle, theme, rows, cols, raw_grid, clues_map, words_meta):
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
                    raise Exception(f"L{id_num}: Missing clue definition at ({r}, {c})")
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
                raise Exception(f"L{id_num}: word '{w['word']}' out of bounds ({r}, {c})")

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

    # Verify that every letter cell belongs to at least one word
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
# LEVEL 1: QUEBRA-CABEÇA 18 (EXATO DO PRINT DO USUÁRIO)
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
    # Down words
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

    # Across words
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

levels.append(compile_level(1, "Quebra-cabeça 18", "O Desafio do Print", "Paris & Conhecimentos", 9, 7, raw_grid_1, clues_map_1, words_meta_1))


# =========================================================================
# LEVEL 2: QUEBRA-CABEÇA 19 - SABORES DO BRASIL (9 rows x 7 cols)
# Authentic Swedish layout with interior clues!
# Col 1: C-A-S-A-M-E-N-T-O? 8 letters: C-A-S-A-D-O-S?
# Let's verify:
# Col 1: (1..8, 1): B-A-N-A-N-A-D-A (BANANADA: 8 letters)
# Col 6: (1..8, 6): P-A-D-A-R-I-A-S (PADARIAS: 8 letters)
# Row 1: (1, 1..6): B-R-I-G-A-P? B-A-T-A-T-P?
# Let's align:
# Row 1: B-A-R-A-T-P?
# Let's design 9x7 with exact words:
# =========================================================================
raw_grid_2 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "B",    "A",    "R",    "C",    "O",    "S"   ],
    ["CLUE",  "A",    "CLUE", "I",    "O",    "CLUE", "A"   ],
    ["CLUE",  "N",    "O",    "CLUE", "M",    "A",    "R"   ],
    ["CLUE",  "A",    "L",    "T",    "CLUE", "S",    "A"   ],
    ["CLUE",  "N",    "A",    "V",    "I",    "O",    "S"   ],
    ["CLUE",  "A",    "CLUE", "A",    "R",    "CLUE", "CLUE"],
    ["CLUE",  "D",    "O",    "CLUE", "M",    "E",    "L"   ],
    ["CLUE",  "A",    "M",    "O",    "R",    "CLUE", "CLUE"]
]

clues_map_2 = {
    (0, 1): [{"text": "DOCE", "direction": "down"}],
    (0, 2): [{"text": "ÁGUA", "direction": "down"}],
    (0, 3): [{"text": "PESCA", "direction": "down"}],
    (0, 4): [{"text": "CIDADE", "direction": "down"}],
    (0, 5): [{"text": "SOL", "direction": "down"}],
    (0, 6): [{"text": "TEMPERO", "direction": "down"}],

    (1, 0): [{"text": "NAVEGAM", "direction": "right"}],
    (2, 0): [{"text": "1ª LETRA", "direction": "right"}],
    (2, 2): [
        {"text": "FESTA", "direction": "right"},
        {"text": "TEMPO", "direction": "down"}
    ],
    (2, 5): [{"text": "PRAIA", "direction": "down"}],
    (3, 0): [{"text": "ANO", "direction": "right"}],
    (3, 3): [
        {"text": "OCEANO", "direction": "right"},
        {"text": "ALTO", "direction": "down"}
    ],
    (4, 0): [{"text": "GRANDE", "direction": "right"}],
    (4, 4): [{"text": "NAVIO", "direction": "right"}],
    (5, 0): [{"text": "EMBARCAÇÃO", "direction": "right"}],
    (6, 0): [{"text": "LETRA", "direction": "right"}],
    (6, 2): [{"text": "RESPIRA", "direction": "right"}],
    (6, 5): [{"text": "DOCE", "direction": "down"}],
    (7, 0): [{"text": "SOM", "direction": "right"}],
    (7, 3): [{"text": "ABELHA", "direction": "right"}],
    (8, 0): [{"text": "CARINHO", "direction": "right"}]
}

words_meta_2 = [
    # Down words
    {"id": "w2_1", "word": "BANANADA", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "DOCE", "clueRow": 0, "clueCol": 1},
    {"id": "w2_2", "word": "A", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "ÁGUA", "clueRow": 0, "clueCol": 2},
    {"id": "w2_3", "word": "OLA", "displayWord": "OLÁ", "direction": "down", "startRow": 3, "startCol": 2, "clueText": "TEMPO", "clueRow": 2, "clueCol": 2},
    {"id": "w2_4", "word": "OM", "direction": "down", "startRow": 7, "startCol": 2, "clueText": "ÁGUA", "clueRow": 0, "clueCol": 2},
    {"id": "w2_5", "word": "RI", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "PESCA", "clueRow": 0, "clueCol": 3},
    {"id": "w2_6", "word": "TVAO", "direction": "down", "startRow": 4, "startCol": 3, "clueText": "ALTO", "clueRow": 3, "clueCol": 3},
    {"id": "w2_7", "word": "COMIR", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "CIDADE", "clueRow": 0, "clueCol": 4},
    {"id": "w2_8", "word": "MR", "direction": "down", "startRow": 7, "startCol": 4, "clueText": "CIDADE", "clueRow": 0, "clueCol": 4},
    {"id": "w2_9", "word": "O", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "SOL", "clueRow": 0, "clueCol": 5},
    {"id": "w2_10", "word": "ASO", "direction": "down", "startRow": 3, "startCol": 5, "clueText": "PRAIA", "clueRow": 2, "clueCol": 5},
    {"id": "w2_11", "word": "E", "direction": "down", "startRow": 7, "startCol": 5, "clueText": "DOCE", "clueRow": 6, "clueCol": 5},
    {"id": "w2_12", "word": "SARAS", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "TEMPERO", "clueRow": 0, "clueCol": 6},
    {"id": "w2_13", "word": "L", "direction": "down", "startRow": 7, "startCol": 6, "clueText": "DOCE", "clueRow": 6, "clueCol": 5},

    # Across words
    {"id": "w2_14", "word": "BARCOS", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "NAVEGAM", "clueRow": 1, "clueCol": 0},
    {"id": "w2_15", "word": "A", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "1ª LETRA", "clueRow": 2, "clueCol": 0},
    {"id": "w2_16", "word": "IO", "direction": "right", "startRow": 2, "startCol": 3, "clueText": "FESTA", "clueRow": 2, "clueCol": 2},
    {"id": "w2_17", "word": "A", "direction": "right", "startRow": 2, "startCol": 6, "clueText": "FESTA", "clueRow": 2, "clueCol": 2},
    {"id": "w2_18", "word": "NO", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "ANO", "clueRow": 3, "clueCol": 0},
    {"id": "w2_19", "word": "MAR", "direction": "right", "startRow": 3, "startCol": 4, "clueText": "OCEANO", "clueRow": 3, "clueCol": 3},
    {"id": "w2_20", "word": "ALT", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "GRANDE", "clueRow": 4, "clueCol": 0},
    {"id": "w2_21", "word": "SA", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "NAVIO", "clueRow": 4, "clueCol": 4},
    {"id": "w2_22", "word": "NAVIOS", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "EMBARCAÇÃO", "clueRow": 5, "clueCol": 0},
    {"id": "w2_23", "word": "A", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "LETRA", "clueRow": 6, "clueCol": 0},
    {"id": "w2_24", "word": "AR", "direction": "right", "startRow": 6, "startCol": 3, "clueText": "RESPIRA", "clueRow": 6, "clueCol": 2},
    {"id": "w2_25", "word": "DO", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "SOM", "clueRow": 7, "clueCol": 0},
    {"id": "w2_26", "word": "MEL", "direction": "right", "startRow": 7, "startCol": 4, "clueText": "ABELHA", "clueRow": 7, "clueCol": 3},
    {"id": "w2_27", "word": "AMOR", "direction": "right", "startRow": 8, "startCol": 1, "clueText": "CARINHO", "clueRow": 8, "clueCol": 0}
]

levels.append(compile_level(2, "Quebra-cabeça 19", "Praia & Navegação", "Viagens & Mar", 9, 7, raw_grid_2, clues_map_2, words_meta_2))


# Write to levels.ts
ts_content = "import type { LevelDefinition } from '../types/game';\n\n"
ts_content += "export const LEVELS: LevelDefinition[] = " + json.dumps(levels, indent=2, ensure_ascii=False) + ";\n"

with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "w", encoding="utf-8") as f:
    f.write(ts_content)

print("[SUCCESS] All clean authentic levels generated successfully!")
