import unicodedata
import re

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Let's inspect words in palavras_full.txt
# Most obscure words end in -asse, -assem, -armo, -ardes, -ico, -ina, -ite, etc. or contain rare sequences.
# Good common words are typical Portuguese roots!
# Also, let's look at the 1000 common words:
with open("scripts/common_words.txt", "r", encoding="utf-8", errors="ignore") as f:
    common = set(strip_accents(l.strip()) for l in f if l.strip().isalpha())

print(f"Loaded {len(common)} base common words.")

# Let's also check if we can fetch a larger frequency list or create a rich vocabulary
