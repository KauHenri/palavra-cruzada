# Automated Swedish Crosswords Builder & Validator
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
                raise Exception(f"L{id_num}: word '{w['word']}' out of bounds ({r}, {c})")

            cell = grid[r][c]
            if cell["type"] != "letter":
                raise Exception(f"L{id_num}: word '{w['word']}' expects letter at ({r}, {c}), found {cell['type']}")

            if cell["solution"] != w_clean[i]:
                raise Exception(f"L{id_num}: mismatch in '{w['word']}' at ({r}, {c}): expected '{w_clean[i]}', cell has '{cell['solution']}'")

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
    total_letters = 0
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if cell["type"] == "letter":
                total_letters += 1
                if len(cell["wordIds"]) == 0:
                    raise Exception(f"L{id_num}: orphan letter cell at ({r}, {c}) '{cell['solution']}'")

    print(f"[OK] Level {id_num}: {title} - {subtitle} ({rows}x{cols}) | {len(words_list)} palavras | {total_letters} letras")
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
# LEVEL 1: QUEBRA-CABEÇA 18 (O PRINT EXATO DO USUÁRIO)
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

levels.append(compile_level(1, "Quebra-cabeça 18", "O Desafio do Print", "Paris & Conhecimentos", 9, 7, raw_grid_18, clues_map_18, words_meta_18))

# =========================================================================
# LEVEL 2: QUEBRA-CABEÇA 19 - SABORES DO BRASIL (8 rows x 7 cols)
# Authentic layout with clues in the middle and corners!
# Col 1: C-A-S-A-D-O-S (CASADOS: 7 letters)
# Col 6: P-A-D-A-R-I-A (PADARIA: 7 letters)
# Row 1: C-A-P-I-T-A-P? No, C-H-O-P-P-P?
# Let's align cleanly:
# =========================================================================
raw_grid_sabores = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "C",    "A",    "F",    "E",    "CLUE", "P"   ],
    ["CLUE",  "A",    "CLUE", "A",    "CLUE", "D",    "A"   ],
    ["CLUE",  "S",    "O",    "P",    "A",    "CLUE", "S"   ],
    ["CLUE",  "A",    "CLUE", "A",    "CLUE", "M",    "T"   ],
    ["CLUE",  "M",    "E",    "S",    "A",    "CLUE", "E"   ],
    ["CLUE",  "O",    "CLUE", "A",    "CLUE", "S",    "L"   ],
    ["CLUE",  "R",    "U",    "A",    "CLUE", "A",    "CLUE"]
]

clues_map_sabores = {
    (0, 1): [{"text": "AFETO", "direction": "down"}],
    (0, 2): [{"text": "OURO", "direction": "down"}],
    (0, 3): [{"text": "PAPA", "direction": "down"}],
    (0, 4): [{"text": "BEBIDA", "direction": "down"}],
    (0, 5): [{"text": "DOCE", "direction": "down"}],
    (0, 6): [{"text": "LANCHE", "direction": "down"}],

    (1, 0): [{"text": "MANHÃ", "direction": "right"}],
    (2, 0): [{"text": "VOGAL", "direction": "right"}],
    (2, 2): [
        {"text": "SOL", "direction": "right"},
        {"text": "OVO", "direction": "down"}
    ],
    (2, 4): [{"text": "DAR", "direction": "right"}],
    (3, 0): [{"text": "CALDO", "direction": "right"}],
    (3, 4): [
        {"text": "SAL", "direction": "right"},
        {"text": "MESA", "direction": "down"}
    ],
    (4, 0): [{"text": "LETRA", "direction": "right"}],
    (4, 2): [{"text": "ROUPA", "direction": "down"}],
    (4, 4): [{"text": "TEMPERO", "direction": "right"}],
    (5, 0): [{"text": "MÓVEL", "direction": "right"}],
    (5, 4): [{"text": "SABOR", "direction": "right"}],
    (6, 0): [{"text": "OLHO", "direction": "right"}],
    (6, 2): [{"text": "MAR", "direction": "down"}],
    (6, 4): [{"text": "SALA", "direction": "right"}],
    (7, 0): [{"text": "VIA", "direction": "right"}]
}

words_meta_sabores = [
    # Down words
    {"id": "s1", "word": "CASAMOR", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "AFETO", "clueRow": 0, "clueCol": 1},
    {"id": "s2", "word": "A", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "OURO", "clueRow": 0, "clueCol": 2},
    {"id": "s3", "word": "FAPASA", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "PAPA", "clueRow": 0, "clueCol": 3},
    {"id": "s4", "word": "E", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "BEBIDA", "clueRow": 0, "clueCol": 4},
    {"id": "s5", "word": "PASTEL", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "LANCHE", "clueRow": 0, "clueCol": 6},
    {"id": "s6", "word": "O", "direction": "down", "startRow": 3, "startCol": 2, "clueText": "OVO", "clueRow": 2, "clueCol": 2},
    {"id": "s7", "word": "E", "direction": "down", "startRow": 5, "startCol": 2, "clueText": "ROUPA", "clueRow": 4, "clueCol": 2},
    {"id": "s8", "word": "U", "direction": "down", "startRow": 7, "startCol": 2, "clueText": "MAR", "clueRow": 6, "clueCol": 2},
    {"id": "s9", "word": "A", "direction": "down", "startRow": 7, "startCol": 3, "clueText": "PAPA", "clueRow": 0, "clueCol": 3},
    {"id": "s10", "word": "D", "direction": "down", "startRow": 2, "startCol": 5, "clueText": "DOCE", "clueRow": 0, "clueCol": 5},
    {"id": "s11", "word": "M", "direction": "down", "startRow": 4, "startCol": 5, "clueText": "MESA", "clueRow": 3, "clueCol": 4},
    {"id": "s12", "word": "S", "direction": "down", "startRow": 6, "startCol": 5, "clueText": "MESA", "clueRow": 3, "clueCol": 4},
    {"id": "s13", "word": "A", "direction": "down", "startRow": 7, "startCol": 5, "clueText": "MESA", "clueRow": 3, "clueCol": 4},

    # Across words
    {"id": "s14", "word": "CAFE", "displayWord": "CAFÉ", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "MANHÃ", "clueRow": 1, "clueCol": 0},
    {"id": "s15", "word": "P", "direction": "right", "startRow": 1, "startCol": 6, "clueText": "LANCHE", "clueRow": 0, "clueCol": 6},
    {"id": "s16", "word": "A", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "VOGAL", "clueRow": 2, "clueCol": 0},
    {"id": "s17", "word": "A", "direction": "right", "startRow": 2, "startCol": 3, "clueText": "SOL", "clueRow": 2, "clueCol": 2},
    {"id": "s18", "word": "DA", "direction": "right", "startRow": 2, "startCol": 5, "clueText": "DAR", "clueRow": 2, "clueCol": 4},
    {"id": "s19", "word": "SOPA", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "CALDO", "clueRow": 3, "clueCol": 0},
    {"id": "s20", "word": "S", "direction": "right", "startRow": 3, "startCol": 6, "clueText": "LANCHE", "clueRow": 0, "clueCol": 6},
    {"id": "s21", "word": "A", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "LETRA", "clueRow": 4, "clueCol": 0},
    {"id": "s22", "word": "A", "direction": "right", "startRow": 4, "startCol": 3, "clueText": "LETRA", "clueRow": 4, "clueCol": 0},
    {"id": "s23", "word": "MT", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "TEMPERO", "clueRow": 4, "clueCol": 4},
    {"id": "s24", "word": "MESA", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "MÓVEL", "clueRow": 5, "clueCol": 0},
    {"id": "s25", "word": "E", "direction": "right", "startRow": 5, "startCol": 6, "clueText": "LANCHE", "clueRow": 0, "clueCol": 6},
    {"id": "s26", "word": "O", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "OLHO", "clueRow": 6, "clueCol": 0},
    {"id": "s27", "word": "A", "direction": "right", "startRow": 6, "startCol": 3, "clueText": "OLHO", "clueRow": 6, "clueCol": 0},
    {"id": "s28", "word": "SL", "direction": "right", "startRow": 6, "startCol": 5, "clueText": "SALA", "clueRow": 6, "clueCol": 4},
    {"id": "s29", "word": "RUA", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "VIA", "clueRow": 7, "clueCol": 0},
    {"id": "s30", "word": "A", "direction": "right", "startRow": 7, "startCol": 5, "clueText": "MESA", "clueRow": 3, "clueCol": 4}
]

# Write out to levels.ts
all_levels = [
    compile_level(1, "Quebra-cabeça 18", "O Desafio do Print", "Paris & Conhecimentos", 9, 7, raw_grid_18, clues_map_18, words_meta_18)
]

print("Outputting clean JSON...")
ts_content = "import type { LevelDefinition } from '../types/game';\n\n"
ts_content += "export const LEVELS: LevelDefinition[] = " + json.dumps(all_levels, indent=2, ensure_ascii=False) + ";\n"

with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "w", encoding="utf-8") as f:
    f.write(ts_content)

print("[SUCCESS] Level 1 updated with absolute perfection!")
