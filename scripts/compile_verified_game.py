import json
from strict_verifier import test_level_design

# =========================================================================
# LEVEL 1: NOITE DE RISADAS (7 rows x 7 cols)
# Grid 4 from solver:
# Row 0: EMPTY, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE
# Col 0: CLUE, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE
# Letters:
# Row 1: R A P O S A
# Row 2: I M O V E L
# Row 3: S A [CLUE] A R I
# Row 4: A D A [CLUE] M E
# Row 5: D O R I A N
# Row 6: A S T R O S
# =========================================================================

raw_grid_1 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "R",    "A",    "P",    "O",    "S",    "A"   ],
    ["CLUE",  "I",    "M",    "O",    "V",    "E",    "L"   ],
    ["CLUE",  "S",    "A",    "CLUE", "A",    "R",    "I"   ],
    ["CLUE",  "A",    "D",    "A",    "CLUE", "M",    "E"   ],
    ["CLUE",  "D",    "O",    "R",    "I",    "A",    "N"   ],
    ["CLUE",  "A",    "S",    "T",    "R",    "O",    "S"   ]
]

clues_map_1 = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "ALEGRIA", "direction": "down"}],
    (0, 2): [{"text": "QUERIDOS", "direction": "down"}],
    (0, 3): [{"text": "RESÍDUO LEVE", "direction": "down"}],
    (0, 4): [{"text": "PEIXE", "direction": "down"}],
    (0, 5): [{"text": "CONSELHO", "direction": "down"}],
    (0, 6): [{"text": "DO ESPAÇO", "direction": "down"}],

    # Col 0 (Across clues)
    (1, 0): [{"text": "BICHO ASTUTO", "direction": "right"}],
    (2, 0): [{"text": "APARTAMENTO", "direction": "right"}],
    (3, 0): [{"text": "SENHORA", "direction": "right"}],
    (3, 3): [
        {"text": "NOME PRÓPRIO", "direction": "right"},
        {"text": "MUSEU", "direction": "down"}
    ],
    (4, 0): [{"text": "NOME FEMININO", "direction": "right"}],
    (4, 4): [
        {"text": "A MIM", "direction": "right"},
        {"text": "PARTIR", "direction": "down"}
    ],
    (5, 0): [{"text": "RETRATO FAMOSO", "direction": "right"}],
    (6, 0): [{"text": "CORPOS CELESTES", "direction": "right"}]
}

words_meta_1 = [
    # Across
    {"id": "w1_1", "word": "RAPOSA", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "BICHO ASTUTO", "clueRow": 1, "clueCol": 0},
    {"id": "w1_2", "word": "IMOVEL", "displayWord": "IMÓVEL", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "APARTAMENTO", "clueRow": 2, "clueCol": 0},
    {"id": "w1_3", "word": "SA", "displayWord": "SÁ", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "SENHORA", "clueRow": 3, "clueCol": 0},
    {"id": "w1_4", "word": "ARI", "direction": "right", "startRow": 3, "startCol": 4, "clueText": "NOME PRÓPRIO", "clueRow": 3, "clueCol": 3},
    {"id": "w1_5", "word": "ADA", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "NOME FEMININO", "clueRow": 4, "clueCol": 0},
    {"id": "w1_6", "word": "ME", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "A MIM", "clueRow": 4, "clueCol": 4},
    {"id": "w1_7", "word": "DORIAN", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "RETRATO FAMOSO", "clueRow": 5, "clueCol": 0},
    {"id": "w1_8", "word": "ASTROS", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "CORPOS CELESTES", "clueRow": 6, "clueCol": 0},

    # Down
    {"id": "w1_9", "word": "RISADA", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "ALEGRIA", "clueRow": 0, "clueCol": 1},
    {"id": "w1_10", "word": "AMADOS", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "QUERIDOS", "clueRow": 0, "clueCol": 2},
    {"id": "w1_11", "word": "PO", "displayWord": "PÓ", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "RESÍDUO LEVE", "clueRow": 0, "clueCol": 3},
    {"id": "w1_12", "word": "ART", "direction": "down", "startRow": 4, "startCol": 3, "clueText": "MUSEU", "clueRow": 3, "clueCol": 3},
    {"id": "w1_13", "word": "OVA", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "PEIXE", "clueRow": 0, "clueCol": 4},
    {"id": "w1_14", "word": "IR", "direction": "down", "startRow": 5, "startCol": 4, "clueText": "PARTIR", "clueRow": 4, "clueCol": 4},
    {"id": "w1_15", "word": "SERMAO", "displayWord": "SERMÃO", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "CONSELHO", "clueRow": 0, "clueCol": 5},
    {"id": "w1_16", "word": "ALIENS", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "DO ESPAÇO", "clueRow": 0, "clueCol": 6}
]

lvl1_data = test_level_design(7, 7, raw_grid_1, clues_map_1, words_meta_1)
lvl1 = {
    "id": 1,
    "title": "Fase 1: Noite de Risadas",
    "subtitle": "Amor & Descontração",
    "theme": "Alegria & Curiosidades",
    "rows": 7,
    "cols": 7,
    "grid": lvl1_data["grid"],
    "words": lvl1_data["words"]
}


# =========================================================================
# LEVEL 2: VIDA A DOIS (7 rows x 7 cols)
# Grid 2 from solver:
# Row 1: C U S T A S
# Row 2: A N T I G A
# Row 3: S I [CLUE] A R I
# Row 4: A C E [CLUE] A M
# Row 5: C A S A D O
# Row 6: O S T R A S
# =========================================================================

raw_grid_2 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "C",    "U",    "S",    "T",    "A",    "S"   ],
    ["CLUE",  "A",    "N",    "T",    "I",    "G",    "A"   ],
    ["CLUE",  "S",    "I",    "CLUE", "A",    "R",    "I"   ],
    ["CLUE",  "A",    "C",    "E",    "CLUE", "A",    "M"   ],
    ["CLUE",  "C",    "A",    "S",    "A",    "D",    "O"   ],
    ["CLUE",  "O",    "S",    "T",    "R",    "A",    "S"   ]
]

clues_map_2 = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "JAQUETA", "direction": "down"}],
    (0, 2): [{"text": "SEM IGUAL", "direction": "down"}],
    (0, 3): [{"text": "SANTO (SIGLA)", "direction": "down"}],
    (0, 4): [{"text": "FAMÍLIA", "direction": "down"}],
    (0, 5): [{"text": "SATISFAZ", "direction": "down"}],
    (0, 6): [{"text": "PASSEAMOS", "direction": "down"}],

    # Col 0 (Across clues)
    (1, 0): [{"text": "DESPESAS", "direction": "right"}],
    (2, 0): [{"text": "VINTAGE", "direction": "right"}],
    (3, 0): [{"text": "7ª NOTA", "direction": "right"}],
    (3, 3): [
        {"text": "HOMEM", "direction": "right"},
        {"text": "ORIENTE", "direction": "down"}
    ],
    (4, 0): [{"text": "Á-C-E", "direction": "right"}],
    (4, 4): [
        {"text": "AMAZONAS", "direction": "right"},
        {"text": "OXIGÊNIO", "direction": "down"}
    ],
    (5, 0): [{"text": "MATRIMÔNIO", "direction": "right"}],
    (6, 0): [{"text": "DÃO PÉROLAS", "direction": "right"}]
}

words_meta_2 = [
    # Across
    {"id": "w2_1", "word": "CUSTAS", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "DESPESAS", "clueRow": 1, "clueCol": 0},
    {"id": "w2_2", "word": "ANTIGA", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "VINTAGE", "clueRow": 2, "clueCol": 0},
    {"id": "w2_3", "word": "SI", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "7ª NOTA", "clueRow": 3, "clueCol": 0},
    {"id": "w2_4", "word": "ARI", "direction": "right", "startRow": 3, "startCol": 4, "clueText": "HOMEM", "clueRow": 3, "clueCol": 3},
    {"id": "w2_5", "word": "ACE", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "Á-C-E", "clueRow": 4, "clueCol": 0},
    {"id": "w2_6", "word": "AM", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "AMAZONAS", "clueRow": 4, "clueCol": 4},
    {"id": "w2_7", "word": "CASADO", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "MATRIMÔNIO", "clueRow": 5, "clueCol": 0},
    {"id": "w2_8", "word": "OSTRAS", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "DÃO PÉROLAS", "clueRow": 6, "clueCol": 0},

    # Down
    {"id": "w2_9", "word": "CASACO", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "JAQUETA", "clueRow": 0, "clueCol": 1},
    {"id": "w2_10", "word": "UNICAS", "displayWord": "ÚNICAS", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "SEM IGUAL", "clueRow": 0, "clueCol": 2},
    {"id": "w2_11", "word": "ST", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "SANTO (SIGLA)", "clueRow": 0, "clueCol": 3},
    {"id": "w2_12", "word": "EST", "direction": "down", "startRow": 4, "startCol": 3, "clueText": "ORIENTE", "clueRow": 3, "clueCol": 3},
    {"id": "w2_13", "word": "TIA", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "FAMÍLIA", "clueRow": 0, "clueCol": 4},
    {"id": "w2_14", "word": "AR", "direction": "down", "startRow": 5, "startCol": 4, "clueText": "OXIGÊNIO", "clueRow": 4, "clueCol": 4},
    {"id": "w2_15", "word": "AGRADA", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "SATISFAZ", "clueRow": 0, "clueCol": 5},
    {"id": "w2_16", "word": "SAIMOS", "displayWord": "SAÍMOS", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "PASSEAMOS", "clueRow": 0, "clueCol": 6}
]

lvl2_data = test_level_design(7, 7, raw_grid_2, clues_map_2, words_meta_2)
lvl2 = {
    "id": 2,
    "title": "Fase 2: Vida a Dois",
    "subtitle": "Casamento & Companheirismo",
    "theme": "União & Cotidiano",
    "rows": 7,
    "cols": 7,
    "grid": lvl2_data["grid"],
    "words": lvl2_data["words"]
}


# =========================================================================
# LEVEL 3: PELO BRASIL (7 rows x 7 cols)
# Grid BRASIL from task 606:
# Row 1: B R A S I L
# Row 2: E U R I C O
# Row 3: L E [CLUE] M A R
# Row 4: M I M [CLUE] P O
# Row 5: A R A T U S
# Row 6: Z O R A I A
# =========================================================================

raw_grid_3 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "B",    "R",    "A",    "S",    "I",    "L"   ],
    ["CLUE",  "E",    "U",    "R",    "I",    "C",    "O"   ],
    ["CLUE",  "L",    "E",    "CLUE", "M",    "A",    "R"   ],
    ["CLUE",  "M",    "I",    "M",    "CLUE", "P",    "O"   ],
    ["CLUE",  "A",    "R",    "A",    "T",    "U",    "S"   ],
    ["CLUE",  "Z",    "O",    "R",    "A",    "I",    "A"   ]
]

clues_map_3 = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "RESISTENTE", "direction": "down"}],
    (0, 2): [{"text": "CAMINHANTE", "direction": "down"}],
    (0, 3): [{"text": "PULMÕES", "direction": "down"}],
    (0, 4): [{"text": "POSITIVO", "direction": "down"}],
    (0, 5): [{"text": "PRAIA CEARENSE", "direction": "down"}],
    (0, 6): [{"text": "ALVORADA", "direction": "down"}],

    # Col 0 (Across clues)
    (1, 0): [{"text": "NOSSA PÁTRIA", "direction": "right"}],
    (2, 0): [{"text": "ESCRITOR", "direction": "right"}],
    (3, 0): [{"text": "ENXERGA LIVRO", "direction": "right"}],
    (3, 3): [
        {"text": "ÁGUA SALGADA", "direction": "right"},
        {"text": "OCEANO", "direction": "down"}
    ],
    (4, 0): [{"text": "PRONOME", "direction": "right"}],
    (4, 4): [
        {"text": "RESÍDUO LEVE", "direction": "right"},
        {"text": "ESTÁ (GÍRIA)", "direction": "down"}
    ],
    (5, 0): [{"text": "CARANGUEJOS", "direction": "right"}],
    (6, 0): [{"text": "NOME FEMININO", "direction": "right"}]
}

words_meta_3 = [
    # Across
    {"id": "w3_1", "word": "BRASIL", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "NOSSA PÁTRIA", "clueRow": 1, "clueCol": 0},
    {"id": "w3_2", "word": "EURICO", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "ESCRITOR", "clueRow": 2, "clueCol": 0},
    {"id": "w3_3", "word": "LE", "displayWord": "LÊ", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "ENXERGA LIVRO", "clueRow": 3, "clueCol": 0},
    {"id": "w3_4", "word": "MAR", "direction": "right", "startRow": 3, "startCol": 4, "clueText": "ÁGUA SALGADA", "clueRow": 3, "clueCol": 3},
    {"id": "w3_5", "word": "MIM", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "PRONOME", "clueRow": 4, "clueCol": 0},
    {"id": "w3_6", "word": "PO", "displayWord": "PÓ", "direction": "right", "startRow": 4, "startCol": 5, "clueText": "RESÍDUO LEVE", "clueRow": 4, "clueCol": 4},
    {"id": "w3_7", "word": "ARATUS", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "CARANGUEJOS", "clueRow": 5, "clueCol": 0},
    {"id": "w3_8", "word": "ZORAIA", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "NOME FEMININO", "clueRow": 6, "clueCol": 0},

    # Down
    {"id": "w3_9", "word": "BELMAZ", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "RESISTENTE", "clueRow": 0, "clueCol": 1},
    {"id": "w3_10", "word": "RUEIRO", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "CAMINHANTE", "clueRow": 0, "clueCol": 2},
    {"id": "w3_11", "word": "AR", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "PULMÕES", "clueRow": 0, "clueCol": 3},
    {"id": "w3_12", "word": "MAR", "direction": "down", "startRow": 4, "startCol": 3, "clueText": "OCEANO", "clueRow": 3, "clueCol": 3},
    {"id": "w3_13", "word": "SIM", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "POSITIVO", "clueRow": 0, "clueCol": 4},
    {"id": "w3_14", "word": "TA", "displayWord": "TÁ", "direction": "down", "startRow": 5, "startCol": 4, "clueText": "ESTÁ (GÍRIA)", "clueRow": 4, "clueCol": 4},
    {"id": "w3_15", "word": "ICAPUI", "displayWord": "ICAPUÍ", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "PRAIA CEARENSE", "clueRow": 0, "clueCol": 5},
    {"id": "w3_16", "word": "LOROSA", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "ALVORADA", "clueRow": 0, "clueCol": 6}
]

lvl3_data = test_level_design(7, 7, raw_grid_3, clues_map_3, words_meta_3)
lvl3 = {
    "id": 3,
    "title": "Fase 3: Pelo Brasil",
    "subtitle": "Nossa Terra & Belezas",
    "theme": "Brasil & Natureza",
    "rows": 7,
    "cols": 7,
    "grid": lvl3_data["grid"],
    "words": lvl3_data["words"]
}


# =========================================================================
# LEVEL 4: DESAFIO DOS MESTRES (9 rows x 7 cols)
# 100% Inédita, zero repetições de fases 1, 2, 3!
# 100% Palavras autênticas da língua portuguesa, zero palavras inventadas.
# =========================================================================

raw_grid_4 = [
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

clues_map_4 = {
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

    (5, 1): [{"text": "TAMPOUCO", "direction": "down"}],            # NEM (rows 6..8, col 1)
    (5, 2): [
        {"text": "LADO DO ORIENTE", "direction": "right"},           # ESTE (rows 5, cols 3..6)
        {"text": "PARTE DA CORRENTE", "direction": "down"}          # ELO (rows 6..8, col 2)
    ],

    (6, 0): [{"text": "SUCO DAS FLORES", "direction": "right"}],    # NÉCTAR
    (7, 0): [{"text": "VENCEDOR DA URNA", "direction": "right"}],   # ELEITO
    (8, 0): [{"text": "MONTES PEQUENOS", "direction": "right"}]     # MORROS
}

words_meta_4 = [
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

lvl4_data = test_level_design(9, 7, raw_grid_4, clues_map_4, words_meta_4)
lvl4 = {
    "id": 4,
    "title": "Fase 4: Desafio dos Mestres",
    "subtitle": "Mistérios & Descobertas",
    "theme": "Conhecimento & Aventura",
    "rows": 9,
    "cols": 7,
    "grid": lvl4_data["grid"],
    "words": lvl4_data["words"]
}

all_levels = [lvl1, lvl2, lvl3, lvl4]

# Write to levels.ts
ts_content = "import type { LevelDefinition } from '../types/game';\n\n"
ts_content += "export const LEVELS: LevelDefinition[] = " + json.dumps(all_levels, indent=2, ensure_ascii=False) + ";\n"

with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "w", encoding="utf-8") as f:
    f.write(ts_content)

print(f"\n[VICTORY] Successfully compiled and verified all {len(all_levels)} levels in levels.ts!")
