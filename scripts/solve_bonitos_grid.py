import unicodedata
from strict_verifier import test_level_design

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
clean_words = {}
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        w = line.strip()
        c = strip_accents(w)
        if c.isalpha() and 2 <= len(c) <= 7:
            if len(c) not in clean_words: clean_words[len(c)] = set()
            clean_words[len(c)].add(c)

# Grid 8x7
# Row 0: empty, clue*6
# Col 0: clue*7
# Internal clues at (3, 3) and (4, 4)
# Let's fix our known anchors:
# Col 1: BONITOS
# Col 6: AMOROSO
# Row 1: BELEZA
# Row 2: ORIGEM
# Row 5: TEATRO

# Remaining cells:
# (3, 2), (3, 4), (3, 5)
# (4, 2), (4, 3), (4, 5)
# (6, 2), (6, 3), (6, 4), (6, 5)
# (7, 2), (7, 3), (7, 4), (7, 5)

# Words:
# A3: (3, 1..2) -> 'N' + c(3,2)  (len 2)
# A4: (3, 4..6) -> c(3,4) + c(3,5) + 'O'  (len 3)
# A5: (4, 1..3) -> 'I' + c(4,2) + c(4,3)  (len 3)
# A6: (4, 5..6) -> c(4,5) + 'R'  (len 2)
# A8: (6, 1..6) -> 'O' + c(6,2) + c(6,3) + c(6,4) + c(6,5) + 'S'  (len 6)
# A9: (7, 1..6) -> 'S' + c(7,2) + c(7,3) + c(7,4) + c(7,5) + 'O'  (len 6)

# Down words:
# D2: (1..7, 2) -> 'E' + 'R' + c(3,2) + c(4,2) + 'E' + c(6,2) + c(7,2)  (len 7)
# D3: (1..2, 3) -> 'L' + 'I' = LI! ('LI' is valid: ler no passado: eu li o livro!)
# D4: (4..7, 3) -> c(4,3) + 'A' + c(6,3) + c(7,3)  (len 4)
# D5: (1..3, 4) -> 'E' + 'G' + c(3,4)  (len 3)
# D6: (5..7, 4) -> 'T' + c(6,4) + c(7,4)  (len 3)
# D7: (1..7, 5) -> 'Z' + 'E' + c(3,5) + c(4,5) + 'R' + c(6,5) + c(7,5)  (len 7)

# Look at D5: 'E' + 'G' + c(3,4).
# 3-letter word starting with EG:
# E - G - O (EGO)!
# E - G - A
# EGO is an everyday common word! So c(3,4) = 'O'!
# Then A4 is: c(3,4) + c(3,5) + 'O' = 'O' + c(3,5) + 'O'.
# 3-letter word starting and ending with O:
# O - V - O (OVO)!
# LOOK AT THAT: c(3,5) = 'V'!
# Then A4 is O - V - O (OVO)!
# And D7: starts with Z - E - V:
# Wait, are there 7-letter words starting with Z - E - V?
# Let's check words in clean_words[7] starting with Z!
z_words = [w for w in clean_words.get(7, []) if w.startswith('Z')]
print("7-letter words starting with Z:", z_words[:10])
