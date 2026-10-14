import json
import sys
import unicodedata

from strict_verifier import test_level_design

# =========================================================================
# LEVEL 1: NOITE DE RISADAS (7x7, Layout A)
# Palavras 100% brasileiras, zero repetição, zero termos em inglês
# Across: ESCALA, LOUCAS, ABRE, TIME, DEITAR, AURORA
# Down: ELA, SOB, CURTIR, ACEITO, LA, AS, DA, EU, MAR, ERA
# =========================================================================

raw_grid_1 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "E",    "S",    "C",    "A",    "L",    "A"   ],
    ["CLUE",  "L",    "O",    "U",    "C",    "A",    "S"   ],
    ["CLUE",  "A",    "B",    "R",    "E",    "CLUE", "CLUE"],
    ["EMPTY", "CLUE", "CLUE", "T",    "I",    "M",    "E"   ],
    ["CLUE",  "D",    "E",    "I",    "T",    "A",    "R"   ],
    ["CLUE",  "A",    "U",    "R",    "O",    "R",    "A"   ]
]

clues_map_1 = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "AQUELA MULHER", "direction": "down"}],
    (0, 2): [{"text": "EMBAIXO DE", "direction": "down"}],
    (0, 3): [{"text": "APROVEITAR", "direction": "down"}],
    (0, 4): [{"text": "CONCORDO", "direction": "down"}],
    (0, 5): [{"text": "NAQUELE LUGAR", "direction": "down"}],
    (0, 6): [{"text": "ARTIGO FEM.", "direction": "down"}],

    # Col 0 (Across clues)
    (1, 0): [{"text": "PARADA DE VOO", "direction": "right"}],
    (2, 0): [{"text": "SEM JUÍZO", "direction": "right"}],
    (3, 0): [{"text": "DESTRANCA", "direction": "right"}],
    (5, 0): [{"text": "IR DORMIR", "direction": "right"}],
    (6, 0): [{"text": "ALVORECER", "direction": "right"}],

    # Interior clues
    (3, 5): [{"text": "ÁGUA SALGADA", "direction": "down"}],
    (3, 6): [{"text": "TEMPO ANTIGO", "direction": "down"}],
    (4, 1): [{"text": "DE + A", "direction": "down"}],
    (4, 2): [
        {"text": "EQUIPE", "direction": "right"},
        {"text": "1ª PESSOA", "direction": "down"}
    ]
}

words_meta_1 = [
    # Across
    {"id": "w1_1", "word": "ESCALA", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "PARADA DE VOO", "clueRow": 1, "clueCol": 0},
    {"id": "w1_2", "word": "LOUCAS", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "SEM JUÍZO", "clueRow": 2, "clueCol": 0},
    {"id": "w1_3", "word": "ABRE", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "DESTRANCA", "clueRow": 3, "clueCol": 0},
    {"id": "w1_4", "word": "TIME", "direction": "right", "startRow": 4, "startCol": 3, "clueText": "EQUIPE", "clueRow": 4, "clueCol": 2},
    {"id": "w1_5", "word": "DEITAR", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "IR DORMIR", "clueRow": 5, "clueCol": 0},
    {"id": "w1_6", "word": "AURORA", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "ALVORECER", "clueRow": 6, "clueCol": 0},

    # Down
    {"id": "w1_7", "word": "ELA", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "AQUELA MULHER", "clueRow": 0, "clueCol": 1},
    {"id": "w1_8", "word": "SOB", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "EMBAIXO DE", "clueRow": 0, "clueCol": 2},
    {"id": "w1_9", "word": "CURTIR", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "APROVEITAR", "clueRow": 0, "clueCol": 3},
    {"id": "w1_10", "word": "ACEITO", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "CONCORDO", "clueRow": 0, "clueCol": 4},
    {"id": "w1_11", "word": "LA", "displayWord": "LÁ", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "NAQUELE LUGAR", "clueRow": 0, "clueCol": 5},
    {"id": "w1_12", "word": "AS", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "ARTIGO FEM.", "clueRow": 0, "clueCol": 6},
    {"id": "w1_13", "word": "DA", "direction": "down", "startRow": 5, "startCol": 1, "clueText": "DE + A", "clueRow": 4, "clueCol": 1},
    {"id": "w1_14", "word": "EU", "direction": "down", "startRow": 5, "startCol": 2, "clueText": "1ª PESSOA", "clueRow": 4, "clueCol": 2},
    {"id": "w1_15", "word": "MAR", "direction": "down", "startRow": 4, "startCol": 5, "clueText": "ÁGUA SALGADA", "clueRow": 3, "clueCol": 5},
    {"id": "w1_16", "word": "ERA", "direction": "down", "startRow": 4, "startCol": 6, "clueText": "TEMPO ANTIGO", "clueRow": 3, "clueCol": 6}
]

lvl1_data = test_level_design(7, 7, raw_grid_1, clues_map_1, words_meta_1)
lvl1 = {
    "id": 1,
    "title": "Fase 1: Noite de Risadas",
    "subtitle": "Amor & Descontração",
    "theme": "Alegria & Cotidiano",
    "rows": 7,
    "cols": 7,
    "grid": lvl1_data["grid"],
    "words": lvl1_data["words"]
}


# =========================================================================
# LEVEL 2: VIDA A DOIS (7x7, Layout A)
# Palavras 100% brasileiras, zero repetição com outras fases
# Across: CASACO, ALEMAS, LONA, INDO, ADOTAR, SEREIA
# Down: CAL, ALO, SENIOR, AMANTE, CA, OS, AS, DE, DAI, ORA
# =========================================================================

raw_grid_2 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "C",    "A",    "S",    "A",    "C",    "O"   ],
    ["CLUE",  "A",    "L",    "E",    "M",    "A",    "S"   ],
    ["CLUE",  "L",    "O",    "N",    "A",    "CLUE", "CLUE"],
    ["EMPTY", "CLUE", "CLUE", "I",    "N",    "D",    "O"   ],
    ["CLUE",  "A",    "D",    "O",    "T",    "A",    "R"   ],
    ["CLUE",  "S",    "E",    "R",    "E",    "I",    "A"   ]
]

clues_map_2 = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "PÓ BRANCO", "direction": "down"}],
    (0, 2): [{"text": "AO TELEFONE", "direction": "down"}],
    (0, 3): [{"text": "MAIS VELHO", "direction": "down"}],
    (0, 4): [{"text": "QUEM TEM AMOR", "direction": "down"}],
    (0, 5): [{"text": "NESTE LUGAR", "direction": "down"}],
    (0, 6): [{"text": "ARTIGO MASC.", "direction": "down"}],

    # Col 0 (Across clues)
    (1, 0): [{"text": "PEÇA DE FRIO", "direction": "right"}],
    (2, 0): [{"text": "DE BERLIM", "direction": "right"}],
    (3, 0): [{"text": "TECIDO FORTE", "direction": "right"}],
    (5, 0): [{"text": "ACOLHER FILHO", "direction": "right"}],
    (6, 0): [{"text": "MULHER-PEIXE", "direction": "right"}],

    # Interior clues
    (3, 5): [{"text": "DESSE LUGAR", "direction": "down"}],
    (3, 6): [{"text": "FAZ PRECE", "direction": "down"}],
    (4, 1): [{"text": "INDICA HORAS", "direction": "down"}],
    (4, 2): [
        {"text": "A CAMINHO", "direction": "right"},
        {"text": "PREPOSIÇÃO", "direction": "down"}
    ]
}

words_meta_2 = [
    # Across
    {"id": "w2_1", "word": "CASACO", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "PEÇA DE FRIO", "clueRow": 1, "clueCol": 0},
    {"id": "w2_2", "word": "ALEMAS", "displayWord": "ALEMÃS", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "DE BERLIM", "clueRow": 2, "clueCol": 0},
    {"id": "w2_3", "word": "LONA", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "TECIDO FORTE", "clueRow": 3, "clueCol": 0},
    {"id": "w2_4", "word": "INDO", "direction": "right", "startRow": 4, "startCol": 3, "clueText": "A CAMINHO", "clueRow": 4, "clueCol": 2},
    {"id": "w2_5", "word": "ADOTAR", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "ACOLHER FILHO", "clueRow": 5, "clueCol": 0},
    {"id": "w2_6", "word": "SEREIA", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "MULHER-PEIXE", "clueRow": 6, "clueCol": 0},

    # Down
    {"id": "w2_7", "word": "CAL", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "PÓ BRANCO", "clueRow": 0, "clueCol": 1},
    {"id": "w2_8", "word": "ALO", "displayWord": "ALÔ", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "AO TELEFONE", "clueRow": 0, "clueCol": 2},
    {"id": "w2_9", "word": "SENIOR", "displayWord": "SÊNIOR", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "MAIS VELHO", "clueRow": 0, "clueCol": 3},
    {"id": "w2_10", "word": "AMANTE", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "QUEM TEM AMOR", "clueRow": 0, "clueCol": 4},
    {"id": "w2_11", "word": "CA", "displayWord": "CÁ", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "NESTE LUGAR", "clueRow": 0, "clueCol": 5},
    {"id": "w2_12", "word": "OS", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "ARTIGO MASC.", "clueRow": 0, "clueCol": 6},
    {"id": "w2_13", "word": "AS", "displayWord": "ÀS", "direction": "down", "startRow": 5, "startCol": 1, "clueText": "INDICA HORAS", "clueRow": 4, "clueCol": 1},
    {"id": "w2_14", "word": "DE", "direction": "down", "startRow": 5, "startCol": 2, "clueText": "PREPOSIÇÃO", "clueRow": 4, "clueCol": 2},
    {"id": "w2_15", "word": "DAI", "displayWord": "DAÍ", "direction": "down", "startRow": 4, "startCol": 5, "clueText": "DESSE LUGAR", "clueRow": 3, "clueCol": 5},
    {"id": "w2_16", "word": "ORA", "direction": "down", "startRow": 4, "startCol": 6, "clueText": "FAZ PRECE", "clueRow": 3, "clueCol": 6}
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
# LEVEL 3: VIAGEM & DESCOBERTAS (7x7, Layout B)
# Inédito! Layout espelhado, zero palavras repetidas com fases 1, 2, 4
# Across: ESTACA, MOINHO, TIAS, ATUM, SELADO, AMORES
# Down: EM, SO, TITULO, ANIMAR, CHA, AOS, ASA, TEM, DE, OS
# =========================================================================

raw_grid_3 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "E",    "S",    "T",    "A",    "C",    "A"   ],
    ["CLUE",  "M",    "O",    "I",    "N",    "H",    "O"   ],
    ["EMPTY", "CLUE", "CLUE", "T",    "I",    "A",    "S"   ],
    ["CLUE",  "A",    "T",    "U",    "M",    "CLUE", "CLUE"],
    ["CLUE",  "S",    "E",    "L",    "A",    "D",    "O"   ],
    ["CLUE",  "A",    "M",    "O",    "R",    "E",    "S"   ]
]

clues_map_3 = {
    # Row 0 (Down clues)
    (0, 1): [{"text": "NO INTERIOR", "direction": "down"}],
    (0, 2): [{"text": "SEM OUTROS", "direction": "down"}],
    (0, 3): [{"text": "DO CAMPEÃO", "direction": "down"}],
    (0, 4): [{"text": "DAR ÂNIMO", "direction": "down"}],
    (0, 5): [{"text": "INFUSÃO", "direction": "down"}],
    (0, 6): [{"text": "A + OS", "direction": "down"}],

    # Col 0 (Across clues)
    (1, 0): [{"text": "POSTE DE CERCA", "direction": "right"}],
    (2, 0): [{"text": "MOEDOR DE TRIGO", "direction": "right"}],
    (4, 0): [{"text": "PEIXE EM LATA", "direction": "right"}],
    (5, 0): [{"text": "COM CARIMBO", "direction": "right"}],
    (6, 0): [{"text": "PAIXÕES", "direction": "right"}],

    # Interior clues
    (3, 1): [{"text": "MEMBRO DE AVE", "direction": "down"}],
    (3, 2): [
        {"text": "IRMÃS DA MÃE", "direction": "right"},
        {"text": "POSSUI", "direction": "down"}
    ],
    (4, 5): [{"text": "PREPOSIÇÃO", "direction": "down"}],
    (4, 6): [{"text": "ARTIGO", "direction": "down"}]
}

words_meta_3 = [
    # Across
    {"id": "w3_1", "word": "ESTACA", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "POSTE DE CERCA", "clueRow": 1, "clueCol": 0},
    {"id": "w3_2", "word": "MOINHO", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "MOEDOR DE TRIGO", "clueRow": 2, "clueCol": 0},
    {"id": "w3_3", "word": "TIAS", "direction": "right", "startRow": 3, "startCol": 3, "clueText": "IRMÃS DA MÃE", "clueRow": 3, "clueCol": 2},
    {"id": "w3_4", "word": "ATUM", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "PEIXE EM LATA", "clueRow": 4, "clueCol": 0},
    {"id": "w3_5", "word": "SELADO", "direction": "right", "startRow": 5, "startCol": 1, "clueText": "COM CARIMBO", "clueRow": 5, "clueCol": 0},
    {"id": "w3_6", "word": "AMORES", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "PAIXÕES", "clueRow": 6, "clueCol": 0},

    # Down
    {"id": "w3_7", "word": "EM", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "NO INTERIOR", "clueRow": 0, "clueCol": 1},
    {"id": "w3_8", "word": "SO", "displayWord": "SÓ", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "SEM OUTROS", "clueRow": 0, "clueCol": 2},
    {"id": "w3_9", "word": "TITULO", "displayWord": "TÍTULO", "direction": "down", "startRow": 1, "startCol": 3, "clueText": "DO CAMPEÃO", "clueRow": 0, "clueCol": 3},
    {"id": "w3_10", "word": "ANIMAR", "direction": "down", "startRow": 1, "startCol": 4, "clueText": "DAR ÂNIMO", "clueRow": 0, "clueCol": 4},
    {"id": "w3_11", "word": "CHA", "displayWord": "CHÁ", "direction": "down", "startRow": 1, "startCol": 5, "clueText": "INFUSÃO", "clueRow": 0, "clueCol": 5},
    {"id": "w3_12", "word": "AOS", "direction": "down", "startRow": 1, "startCol": 6, "clueText": "A + OS", "clueRow": 0, "clueCol": 6},
    {"id": "w3_13", "word": "ASA", "direction": "down", "startRow": 4, "startCol": 1, "clueText": "MEMBRO DE AVE", "clueRow": 3, "clueCol": 1},
    {"id": "w3_14", "word": "TEM", "direction": "down", "startRow": 4, "startCol": 2, "clueText": "POSSUI", "clueRow": 3, "clueCol": 2},
    {"id": "w3_15", "word": "DE", "direction": "down", "startRow": 5, "startCol": 5, "clueText": "PREPOSIÇÃO", "clueRow": 4, "clueCol": 5},
    {"id": "w3_16", "word": "OS", "direction": "down", "startRow": 5, "startCol": 6, "clueText": "ARTIGO", "clueRow": 4, "clueCol": 6}
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
# Across: ACAROS, LAPELA, EVASAO, MARI, ESTE, NECTAR, ELEITO, MORROS
# Down: ALEM, NEM, CAVA, ELO, APARECER, RESISTIR, OLA, TATO, SAO, EROS
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
    (0, 3): [{"text": "SURGIR", "direction": "down"}],              # APARECER
    (0, 4): [{"text": "AGUENTAR FIRME", "direction": "down"}],      # RESISTIR
    (0, 5): [{"text": "SAUDAÇÃO", "direction": "down"}],            # OLÁ
    (0, 6): [{"text": "SAUDÁVEL", "direction": "down"}],            # SÃO

    # Col 0 (Across clues)
    (1, 0): [{"text": "DA POEIRA", "direction": "right"}],          # ÁCAROS
    (2, 0): [{"text": "DOBRA DO TERNO", "direction": "right"}],     # LAPELA
    (3, 0): [{"text": "FUGA OU SAÍDA", "direction": "right"}],      # EVASÃO
    (4, 0): [{"text": "CIDADE DA PB", "direction": "right"}],       # MARI

    # Interior clues
    (4, 5): [{"text": "PELO TOQUE", "direction": "down"}],          # TATO (rows 5..8, col 5)
    (4, 6): [{"text": "DEUS DO AMOR", "direction": "down"}],        # EROS (rows 5..8, col 6)

    (5, 1): [{"text": "TAMPOUCO", "direction": "down"}],            # NEM (rows 6..8, col 1)
    (5, 2): [
        {"text": "DO ORIENTE", "direction": "right"},                # ESTE (rows 5, cols 3..6)
        {"text": "DA CORRENTE", "direction": "down"}                # ELO (rows 6..8, col 2)
    ],

    (6, 0): [{"text": "SUCO DA FLOR", "direction": "right"}],       # NÉCTAR
    (7, 0): [{"text": "VENCEU NA URNA", "direction": "right"}],     # ELEITO
    (8, 0): [{"text": "MONTES BAIXOS", "direction": "right"}]       # MORROS
}

words_meta_4 = [
    # Across
    {"id": "w4_1", "word": "ACAROS", "displayWord": "ÁCAROS", "direction": "right", "startRow": 1, "startCol": 1, "clueText": "DA POEIRA", "clueRow": 1, "clueCol": 0},
    {"id": "w4_2", "word": "LAPELA", "direction": "right", "startRow": 2, "startCol": 1, "clueText": "DOBRA DO TERNO", "clueRow": 2, "clueCol": 0},
    {"id": "w4_3", "word": "EVASAO", "displayWord": "EVASÃO", "direction": "right", "startRow": 3, "startCol": 1, "clueText": "FUGA OU SAÍDA", "clueRow": 3, "clueCol": 0},
    {"id": "w4_4", "word": "MARI", "direction": "right", "startRow": 4, "startCol": 1, "clueText": "CIDADE DA PB", "clueRow": 4, "clueCol": 0},
    {"id": "w4_5", "word": "ESTE", "direction": "right", "startRow": 5, "startCol": 3, "clueText": "DO ORIENTE", "clueRow": 5, "clueCol": 2},
    {"id": "w4_6", "word": "NECTAR", "displayWord": "NÉCTAR", "direction": "right", "startRow": 6, "startCol": 1, "clueText": "SUCO DA FLOR", "clueRow": 6, "clueCol": 0},
    {"id": "w4_7", "word": "ELEITO", "direction": "right", "startRow": 7, "startCol": 1, "clueText": "VENCEU NA URNA", "clueRow": 7, "clueCol": 0},
    {"id": "w4_8", "word": "MORROS", "direction": "right", "startRow": 8, "startCol": 1, "clueText": "MONTES BAIXOS", "clueRow": 8, "clueCol": 0},

    # Down
    {"id": "w4_9", "word": "ALEM", "displayWord": "ALÉM", "direction": "down", "startRow": 1, "startCol": 1, "clueText": "MAIS ADIANTE", "clueRow": 0, "clueCol": 1},
    {"id": "w4_10", "word": "NEM", "direction": "down", "startRow": 6, "startCol": 1, "clueText": "TAMPOUCO", "clueRow": 5, "clueCol": 1},
    {"id": "w4_11", "word": "CAVA", "direction": "down", "startRow": 1, "startCol": 2, "clueText": "ABRE BURACO", "clueRow": 0, "clueCol": 2},
    {"id": "w4_12", "word": "ELO", "direction": "down", "startRow": 6, "startCol": 2, "clueText": "DA CORRENTE", "clueRow": 5, "clueCol": 2},
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

# Verification of content word disjointness across levels
level_content_words = []
for idx, lvl in enumerate(all_levels):
    c_words = {w["word"] for w in lvl["words"] if len(w["word"]) >= 3}
    level_content_words.append(c_words)
    print(f"Level {idx+1} Content Words ({len(c_words)}): {sorted(c_words)}")

for i in range(len(all_levels)):
    for j in range(i + 1, len(all_levels)):
        overlap = level_content_words[i] & level_content_words[j]
        if overlap:
            raise Exception(f"OVERLAP DETECTED between Level {i+1} and Level {j+1}: {overlap}")

print("\n[SUCCESS] Pairwise disjoint check PASSED! 0 word repeats among content words across all levels!")

# Write to levels.ts
ts_content = "import type { LevelDefinition } from '../types/game';\n\n"
ts_content += "export const LEVELS: LevelDefinition[] = " + json.dumps(all_levels, indent=2, ensure_ascii=False) + ";\n"

with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "w", encoding="utf-8") as f:
    f.write(ts_content)

print(f"[VICTORY] Successfully compiled and verified all {len(all_levels)} levels in src/data/levels.ts!")
