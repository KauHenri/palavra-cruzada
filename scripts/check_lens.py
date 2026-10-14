import unicodedata
from collections import defaultdict

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

words = defaultdict(set)
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            if w.isalpha():
                words[len(w)].add(w)

with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        w = strip_accents(line.strip())
        if w.isalpha():
            words[len(w)].add(w)

for l in sorted(words.keys()):
    if l <= 10:
        print(f"Len {l}: {len(words[l])} words")
