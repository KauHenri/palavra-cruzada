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

levels.append(compile_level(1, "Quebra-cabeça 18", "O Desafio do Print", "Paris & Conhecimentos", 9, 7, raw_grid_18, clues_map_18, words_meta_18))


# =========================================================================
# LEVEL 2: QUEBRA-CABEÇA 19 - BRASIL & VIAGENS (9 rows x 7 cols)
# Authentic layout with interior clues and only real words:
# Col 1: B-R-A-S-I-L-I-A (8 letters down: BRASÍLIA)
# Col 6: P-O-R-T-U-G-A-L (8 letters down: PORTUGAL)
# =========================================================================
raw_grid_brasil = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "B",    "O",    "M",    "CLUE", "S",    "P"   ],
    ["CLUE",  "R",    "I",    "O",    "CLUE", "D",    "O"   ],
    ["CLUE",  "A",    "S",    "A",    "CLUE", "A",    "R"   ],
    ["CLUE",  "S",    "U",    "L",    "CLUE", "CLUE", "T"   ],
    ["CLUE",  "I",    "A",    "CLUE", "C",    "E",    "U"   ],
    ["CLUE",  "L",    "U",    "A",    "CLUE", "M",    "G"   ],
    ["CLUE",  "I",    "CLUE", "D",    "I",    "A",    "A"   ],
    ["CLUE",  "A",    "R",    "CLUE", "S",    "O",    "L"   ]
]

clues_map_brasil = {
    (0, 1): [{"text": "CAPITAL", "direction": "down"}],
    (0, 2): [{"text": "CÃO", "direction": "down"}],
    (0, 3): [{"text": "NOME", "direction": "down"}],
    (0, 4): [{"text": "SIGLA", "direction": "down"}],
    (0, 5): [{"text": "SOMA", "direction": "down"}],
    (0, 6): [{"text": "PAÍS IRMÃO", "direction": "down"}],

    (1, 0): [{"text": "AGRADÁVEL", "direction": "right"}],
    (1, 4): [{"text": "SÃO PAULO", "direction": "right"}],
    (2, 0): [{"text": "ÁGUA DOCE", "direction": "right"}],
    (2, 4): [{"text": "DE + O", "direction": "right"}],
    (3, 0): [{"text": "AVE", "direction": "right"}],
    (3, 4): [
        {"text": "OXIGÊNIO", "direction": "right"},
        {"text": "ASTRAL", "direction": "down"}
    ],
    (4, 0): [{"text": "FRIO", "direction": "right"}],
    (4, 4): [{"text": "LETRA", "direction": "right"}],
    (5, 0): [{"text": "ROBÔ", "direction": "right"}],
    (5, 3): [
        {"text": "AZUL", "direction": "right"},
        {"text": "DIA", "direction": "down"}
    ],
    (6, 0): [{"text": "NOITE", "direction": "right"}],
    (6, 4): [{"text": "MINAS", "direction": "right"}],
    (7, 0): [{"text": "VOGAL", "direction": "right"}],
    (7, 2): [{"text": "MANHÃ", "direction": "right"}],
    (8, 0): [{"text": "RESPIRA", "direction": "right"}],
    (8, 3): [{"text": "ESTRELA", "direction": "right"}]
}

words_meta_brasil = [
    # Down words
    {"id": "b1", "word": "BRASILIA", "displayWord": "BRASÍLIA", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "CAPITAL", "clueRow": 0, "clueCol": 1},
    {"id": "b2", "word": "OISUAU", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "CÃO", "clueRow": 0, "clueCol": 2},
    {"id": "b3", "word": "R", "direction": "down", "startRow": 8, "startCol": 2, "clueText": "CÃO", "clueRow": 0, "clueCol": 2},
    {"id": "b4", "word": "MOAL", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "NOME", "clueRow": 0, "clueCol": 3},
    {"id": "b5", "word": "A", "direction": "down", "startRow": 6, "startCol": 3, "clueText": "NOME", "clueRow": 0, "clueCol": 3},
    {"id": "b6", "word": "C", "direction": "down", "startRow": 5, "startCol": 4, "clueText": "SIGLA", "clueRow": 0, "clueCol": 4},
    {"id": "b7", "word": "IS", "direction": "down", "startRow": 7, "startCol": 4, "clueText": "DIA", "clueRow": 5, "clueCol": 3},
    {"id": "b8", "word": "SDA", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "SOMA", "clueRow": 0, "clueCol": 5},
    {"id": "b9", "word": "EMO", "direction": "down", "startRow": 5, "startCol": 5, "clueText": "ASTRAL", "clueRow": 3, "clueCol": 4},
    {"id": "b10", "word": "PORTUGAL", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "PAÍS IRMÃO", "clueRow": 0, "clueCol": 6},

    # Across words
    {"id": "b11", "word": "BOM", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "AGRADÁVEL", "clueRow": 1, "clueCol": 0},
    {"id": "b12", "word": "SP", "direction": "right", "startRow": 1, "startCol": 5, "clueText": "SÃO PAULO", "clueRow": 1, "clueCol": 4},
    {"id": "b13", "word": "RIO", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "ÁGUA DOCE", "clueRow": 2, "clueCol": 0},
    {"id": "b14", "word": "DO", "direction": "right", "startRow": 2, "startCol": 5, "clueText": "DE + O", "clueRow": 2, "clueCol": 4},
    {"id": "b15", "word": "ASA", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "AVE", "clueRow": 3, "clueCol": 0},
    {"id": "b16", "word": "AR", "direction": "right", "startRow": 3, "startCol": 5, "clueText": "OXIGÊNIO", "clueRow": 3, "clueCol": 4},
    {"id": "b17", "word": "SUL", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "FRIO", "clueRow": 4, "clueCol": 0},
    {"id": "b18", "word": "T", "direction": "right", "startRow": 4, "startCol": 6, "clueText": "LETRA", "clueRow": 4, "clueCol": 4},
    {"id": "b19", "word": "IA", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "ROBÔ", "clueRow": 5, "clueCol": 0},
    {"id": "b20", "word": "CEU", "displayWord": "CÉU", "direction": "right", "startRow": 5, "startCol": 4, "clueText": "AZUL", "clueRow": 5, "clueCol": 3},
    {"id": "b21", "word": "LUA", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "NOITE", "clueRow": 6, "clueCol": 0},
    {"id": "b22", "word": "MG", "direction": "right", "startRow": 6, "startCol": 5, "clueText": "MINAS", "clueRow": 6, "clueCol": 4},
    {"id": "b23", "word": "I", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "VOGAL", "clueRow": 7, "clueCol": 0},
    {"id": "b24", "word": "DIA", "direction": "right", "startRow": 7, "startCol": 4, "clueText": "MANHÃ", "clueRow": 7, "clueCol": 2},
    {"id": "b25", "word": "AR", "direction": "right", "startRow": 8, "startCol": 1, "clueText": "RESPIRA", "clueRow": 8, "clueCol": 0},
    {"id": "b26", "word": "SOL", "direction": "right", "startRow": 8, "startCol": 4, "clueText": "ESTRELA", "clueRow": 8, "clueCol": 3}
]

# Write to levels.ts
all_levels = [
    compile_level(1, "Quebra-cabeça 18", "O Desafio Original", "Paris & Conhecimentos", 9, 7, raw_grid_18, clues_map_18, words_meta_18)
]

print("Writing levels.ts with Quebra-cabeça 18 as Level 1...")
ts_content = "import type { LevelDefinition } from '../types/game';\n\n"
ts_content += "export const LEVELS: LevelDefinition[] = " + json.dumps(all_levels, indent=2, ensure_ascii=False) + ";\n"

with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "w", encoding="utf-8") as f:
    f.write(ts_content)

print("[SUCCESS] Level 1 updated with Quebra-cabeça 18!")
