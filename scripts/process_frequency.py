import unicodedata

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Let's read pt_br_50k.txt
# Each line is "word freq"
top_words = []
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            word, freq = parts[0], int(parts[1])
            clean = strip_accents(word)
            if clean.isalpha() and 2 <= len(clean) <= 8:
                top_words.append((clean, word, freq))

print(f"Total valid candidate words in 50k list: {len(top_words)}")

# Top 8000 words
top_8k = {}
for clean, original, freq in top_words[:12000]:
    if clean not in top_8k:
        top_8k[clean] = (original, freq)

print(f"Unique words in top 12k: {len(top_8k)}")

# Let's save clean list
with open("scripts/top_common_clean.txt", "w", encoding="utf-8") as f:
    for clean, (orig, freq) in top_8k.items():
        f.write(f"{clean} {orig} {freq}\n")

print("Saved top_common_clean.txt!")
