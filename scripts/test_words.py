import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
print("Loading word list...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

words_by_len = {}
raw_by_clean = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha():
        continue
    l = len(clean)
    if l not in words_by_len:
        words_by_len[l] = set()
    words_by_len[l].add(clean)
    if clean not in raw_by_clean:
        raw_by_clean[clean] = w

print(f"Loaded {sum(len(v) for v in words_by_len.values())} clean words.")

# Let's see words of length 2..8
for k in range(2, 9):
    print(f"Len {k}: {len(words_by_len.get(k, []))} words")
