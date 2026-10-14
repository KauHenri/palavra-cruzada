import unicodedata
from collections import defaultdict

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

common_words = defaultdict(list)
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            disp = parts[1] if len(parts) > 1 else parts[0]
            if w.isalpha():
                common_words[len(w)].append((w, disp))

for l in sorted(common_words.keys()):
    if l <= 8:
        print(f"Common Len {l}: {len(common_words[l])} words (sample: {[w[0] for w in common_words[l][:5]]})")
