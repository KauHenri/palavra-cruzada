import sys
import os
import re
import unicodedata
from collections import defaultdict

# Load vocabulary
with open("c:/ProjetosIA/Palavra_Cruzada/scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    vocab_raw = [line.strip().upper() for line in f if line.strip()]

# Clean accents
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper()

vocab = set()
word_to_display = {}
for w in vocab_raw:
    w_clean = strip_accents(w)
    if w_clean.isalpha():
        vocab.add(w_clean)
        if w_clean not in word_to_display:
            word_to_display[w_clean] = w

# Exclude words already used in levels 1, 2, 3
USED_WORDS = {
    'RAPOSA', 'IMOVEL', 'SA', 'ARI', 'ADA', 'ME', 'DORIAN', 'ASTROS',
    'RISADA', 'AMADOS', 'PO', 'ART', 'OVA', 'IR', 'SERMAO', 'ALIENS',
    'CUSTAS', 'ANTIGA', 'SI', 'ACE', 'AM', 'CASADO', 'OSTRAS',
    'CASACO', 'UNICAS', 'ST', 'EST', 'TIA', 'AR', 'AGRADA', 'SAIMOS',
    'BRASIL', 'EURICO', 'LE', 'MAR', 'MIM', 'ARATUS', 'ZORAIA',
    'BELMAZ', 'RUEIRO', 'SIM', 'TA', 'ICAPUI', 'LOROSA'
}

for uw in USED_WORDS:
    vocab.discard(uw)

words_by_len = defaultdict(list)
for w in vocab:
    words_by_len[len(w)].append(w)

print(f"Loaded {len(vocab)} clean unique words.")
for l in sorted(words_by_len.keys()):
    if l <= 8:
        print(f"Len {l}: {len(words_by_len[l])} words")
