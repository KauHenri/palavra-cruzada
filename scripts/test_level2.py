# Python generator for Level 2 (Quebra-cabeça 19)
import json

raw_grid_2 = [
    ["EMPTY", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE", "CLUE"],
    ["CLUE",  "C",    "A",    "F",    "E",    "CLUE", "P"   ],
    ["CLUE",  "A",    "CLUE", "O",    "CLUE", "D",    "A"   ],
    ["CLUE",  "M",    "A",    "CLUE", "L",    "U",    "S"   ],
    ["CLUE",  "I",    "S",    "O",    "CLUE", "A",    "S"   ],
    ["CLUE",  "N",    "A",    "V",    "I",    "O",    "E"   ],
    ["CLUE",  "H",    "CLUE", "O",    "R",    "CLUE", "I"   ],
    ["CLUE",  "A",    "R",    "CLUE", "M",    "E",    "O"   ],
    ["CLUE",  "R",    "U",    "A",    "CLUE", "U",    "S"   ]
]

# Let's check words in raw_grid_2:
# Col 1 Down (r1..r8): C-A-M-I-N-H-A-R = CAMINHAR (8 letters down)
# Col 6 Down (r1..r8): P-A-S-S-E-I-O-S = PASSEIOS (8 letters down)
# Col 2: (1, 2)=A. (3..5, 2): A-S-A = ASA! (3 letters down)
# (7..8, 2): R-U = RU (Rua / Ruanda)
# Col 3: (1..2, 3): F-O = FÓ! (Foco)
# (4..6, 3): O-V-O = OVO! (3 letters down)
# (8, 3) = A (from RUA)
# Col 4: (1, 4)=E. (3, 4)=L. (5..7, 4): I-R-M = IRM (Irmão / Irmã)
# Col 5: (2..5, 5): D-U-A-O?
# Let's write a python checker:
print("Testing grid...")
