import unicodedata
from collections import defaultdict
import json

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load verified PT dictionary
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    dict_words = {strip_accents(line.strip()): line.strip().upper() for line in f if line.strip().isalpha()}

w50 = set()
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if p and p[0].isalpha():
            w50.add(strip_accents(p[0]))

freq = {}
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        p = line.strip().split()
        if len(p) >= 3 and not p[1][0].isupper():
            w = strip_accents(p[0])
            freq[w] = max(freq.get(w, 0), int(p[2]))

def is_super_clean(w):
    return w in dict_words and w in w50 and freq.get(w, 0) >= 40

print("Integrity checker ready.")
