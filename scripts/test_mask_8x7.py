import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
print("Loading words...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

words_by_len = {}
raw_by_clean = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha():
        continue
    l = len(clean)
    if 2 <= l <= 8:
        if l not in words_by_len:
            words_by_len[l] = set()
        words_by_len[l].add(clean)
        if clean not in raw_by_clean:
            raw_by_clean[clean] = w

print("Done loading words.")

# Let's inspect Quebra-cabeça 18 mask:
# Rows: 9, Cols: 7
# Clues at:
# Row 0: (0, 1..6)
# Col 0: (1..8, 0)
# Interior: (2, 2), (3, 3), (4, 4), (6, 5), (7, 4), (8, 3)
# In Quebra-cabeça 18, row 2 col 1 was 'D' (1 letter) and row 6 col 6 was 'I' (1 letter).
# What if we design masks that have NO 1-letter words at all?
# Let's see: in 8x7, if interior clues are at:
# [(2, 3), (4, 4), (6, 3)] or [(3, 3), (5, 4)]
# Let's test [(3, 3), (5, 4)] in 8x7:
# Slots in 8x7 with [(3, 3), (5, 4)]:
# Across:
# A1: (1, 1..6) len 6
# A2: (2, 1..6) len 6
# A3: (3, 1..2) len 2
# A4: (3, 4..6) len 3
# A5: (4, 1..6) len 6
# A6: (5, 1..3) len 3
# A7: (5, 5..6) len 2
# A8: (6, 1..6) len 6
# A9: (7, 1..6) len 6
# Down:
# D1: (1..7, 1) len 7
# D2: (1..7, 2) len 7
# D3: (1..2, 3) len 2
# D4: (4..7, 3) len 4
# D5: (1..4, 4) len 4
# D6: (6..7, 4) len 2
# D7: (1..7, 5) len 7
# D8: (1..7, 6) len 7

# Total slots: 17 slots!
# Look at the lengths:
# Length 2: 4 words
# Length 3: 2 words
# Length 4: 2 words
# Length 6: 5 words
# Length 7: 4 words
# ZERO 1-letter words! Every word is an exact sequence of 2, 3, 4, 6, or 7 letters!

# Let's run a solver on this mask and print solutions!
mask_8x7_A = [
    ("A1", "right", 1, 1, 6),
    ("A2", "right", 2, 1, 6),
    ("A3", "right", 3, 1, 2),
    ("A4", "right", 3, 4, 3),
    ("A5", "right", 4, 1, 6),
    ("A6", "right", 5, 1, 3),
    ("A7", "right", 5, 5, 2),
    ("A8", "right", 6, 1, 6),
    ("A9", "right", 7, 1, 6),
    ("D1", "down", 1, 1, 7),
    ("D2", "down", 1, 2, 7),
    ("D3", "down", 1, 3, 2),
    ("D4", "down", 4, 3, 4),
    ("D5", "down", 1, 4, 4),
    ("D6", "down", 6, 4, 2),
    ("D7", "down", 1, 5, 7),
    ("D8", "down", 1, 6, 7),
]

print(f"Mask has {len(mask_8x7_A)} slots.")
