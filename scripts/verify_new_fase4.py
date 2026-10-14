import json
from strict_verifier import test_level_design

# Dimensions: 9 rows x 7 cols
rows = 9
cols = 7

# Raw grid definition:
# Row 0: EMPTY, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE
# Col 0: EMPTY, CLUE, CLUE, CLUE, CLUE, EMPTY, CLUE, CLUE, CLUE
# Cells (r, c):
# R1: A C A R O S
# R2: L A P E L A
# R3: E V A S A O
# R4: M A R I [CLUE] [CLUE]
# R5: [CLUE] [CLUE] E S T E
# R6: N E C T A R
# R7: E L E I T O
# R8: M O R R O S

raw_grid = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "A",    "C",    "A",    "R",    "O",    "S"   ],
    ["CLUE",  "L",    "A",    "P",    "E",    "L",    "A"   ],
    ["CLUE",  "E",    "V",    "A",    "S",    "A",    "O"   ],
    ["CLUE",  "M",    "A",    "R",    "I",    "CLUE", "CLUE"],
    ["EMPTY", "CLUE", "CLUE", "E",    "S",    "T",    "E"   ],
    ["CLUE",  "N",    "E",    "C",    "T",    "A",    "R"   ],
    ["CLUE",  "E",    "L",    "E",    "I",    "T",    "O"   ],
    ["CLUE",  "M",    "O",    "R",    "R",    "O",    "S"   ]
]

# Clues map:
clues_map = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "MAIS ADIANTE", "direction": "down"}],       # ALÉM
    (0, 2): [{"text": "ABRE BURACO", "direction": "down"}],         # CAVA
    (0, 3): [{"text": "SURGIR À VISTA", "direction": "down"}],      # APARECER
    (0, 4): [{"text": "AGUENTAR FIRME", "direction": "down"}],      # RESISTIR
    (0, 5): [{"text": "SAUDAÇÃO", "direction": "down"}],            # OLÁ
    (0, 6): [{"text": "SAUDÁVEL", "direction": "down"}],            # SÃO

    # Col 0 (Across clues)
    (1, 0): [{"text": "MICRO-ORGANISMOS", "direction": "right"}],   # ÁCAROS
    (2, 0): [{"text": "DOBRA DO PALETÓ", "direction": "right"}],    # LAPELA
    (3, 0): [{"text": "FUGA OU SAÍDA", "direction": "right"}],      # EVASÃO
    (4, 0): [{"text": "FRUTA DO NORTE", "direction": "right"}],     # MARI

    # Interior clues
    (4, 5): [{"text": "SENTIDO DA PELE", "direction": "down"}],     # TATO (rows 5..8, col 5)
    (4, 6): [{"text": "DEUS DO AMOR", "direction": "down"}],        # EROS (rows 5..8, col 6)

    (5, 1): [{"text": "TAMPOUCO", "direction": "down"}],          # NEM (rows 6..8, col 1)
    (5, 2): [
        {"text": "LADO DO ORIENTE", "direction": "right"},           # ESTE (rows 5, cols 3..6)
        {"text": "PARTE DA CORRENTE", "direction": "down"}          # ELO (rows 6..8, col 2)
    ],

    (6, 0): [{"text": "SUCO DAS FLORES", "direction": "right"}],    # NÉCTAR
    (7, 0): [{"text": "VENCEDOR DA URNA", "direction": "right"}],   # ELEITO
    (8, 0): [{"text": "MONTES PEQUENOS", "direction": "right"}]     # MORROS
}

# Words metadata
words_meta = [
    # Across
    {"id": "w4_1", "word": "ACAROS", "displayWord": "ÁCAROS", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "MICRO-ORGANISMOS", "clueRow": 1, "clueCol": 0},
    {"id": "w4_2", "word": "LAPELA", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "DOBRA DO PALETÓ", "clueRow": 2, "clueCol": 0},
    {"id": "w4_3", "word": "EVASAO", "displayWord": "EVASÃO", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "FUGA OU SAÍDA", "clueRow": 3, "clueCol": 0},
    {"id": "w4_4", "word": "MARI", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "FRUTA DO NORTE", "clueRow": 4, "clueCol": 0},
    {"id": "w4_5", "word": "ESTE", "direction": "right", "startRow": 5, "startCol": 3, "clueText": "LADO DO ORIENTE", "clueRow": 5, "clueCol": 2},
    {"id": "w4_6", "word": "NECTAR", "displayWord": "NÉCTAR", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "SUCO DAS FLORES", "clueRow": 6, "clueCol": 0},
    {"id": "w4_7", "word": "ELEITO", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "VENCEDOR DA URNA", "clueRow": 7, "clueCol": 0},
    {"id": "w4_8", "word": "MORROS", "direction": "right", "startRow": 8, "startCol": 1, "clueText": "MONTES PEQUENOS", "clueRow": 8, "clueCol": 0},

    # Down
    {"id": "w4_9", "word": "ALEM", "displayWord": "ALÉM", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "MAIS ADIANTE", "clueRow": 0, "clueCol": 1},
    {"id": "w4_10", "word": "NEM", "direction": "down", "startRow": 6, "startCol": 1, "clueText": "TAMPOUCO", "clueRow": 5, "clueCol": 1},
    {"id": "w4_11", "word": "CAVA", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "ABRE BURACO", "clueRow": 0, "clueCol": 2},
    {"id": "w4_12", "word": "ELO", "direction": "down", "startRow": 6, "startCol": 2, "clueText": "PARTE DA CORRENTE", "clueRow": 5, "clueCol": 2},
    {"id": "w4_13", "word": "APARECER", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "SURGIR À VISTA", "clueRow": 0, "clueCol": 3},
    {"id": "w4_14", "word": "RESISTIR", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "AGUENTAR FIRME", "clueRow": 0, "clueCol": 4},
    {"id": "w4_15", "word": "OLA", "displayWord": "OLÁ", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "SAUDAÇÃO", "clueRow": 0, "clueCol": 5},
    {"id": "w4_16", "word": "TATO", "direction": "down", "startRow": 5, "startCol": 5, "clueText": "SENTIDO DA PELE", "clueRow": 4, "clueCol": 5},
    {"id": "w4_17", "word": "SAO", "displayWord": "SÃO", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "SAUDÁVEL", "clueRow": 0, "clueCol": 6},
    {"id": "w4_18", "word": "EROS", "direction": "down", "startRow": 5, "startCol": 6, "clueText": "DEUS DO AMOR", "clueRow": 4, "clueCol": 6}
]

print("Running strict verifier on new Level 4...")
level_data = test_level_design(rows, cols, raw_grid, clues_map, words_meta)
print("[PASS] STRICT VERIFIER CONFIRMS: LEVEL 4 IS 100% VALID!")
print(f"Total Words: {len(level_data['words'])}, Grid: {rows}x{cols}")
