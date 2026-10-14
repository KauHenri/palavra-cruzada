import unicodedata

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load common words
common_by_len = {}
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        l = len(clean)
        if l not in common_by_len: common_by_len[l] = []
        common_by_len[l].append(clean)

words_8 = common_by_len.get(8, [])
words_6 = common_by_len.get(6, [])

print(f"Loaded {len(words_8)} 8-letter common words and {len(words_6)} 6-letter common words.")

# Find pairs (W_col1, W_col6) in words_8 such that:
# Row 1: starts with W_col1[0], ends with W_col6[0] (in words_6)
# Row 5: starts with W_col1[4], ends with W_col6[4] (in words_6)
# Row 8: starts with W_col1[7], ends with W_col6[7] (in words_6)

matches = []
for c1 in words_8[:200]:
    for c6 in words_8[:200]:
        if c1 == c6: continue

        # Check row 1
        r1_cands = [w for w in words_6 if w[0] == c1[0] and w[-1] == c6[0]]
        if not r1_cands: continue

        # Check row 5
        r5_cands = [w for w in words_6 if w[0] == c1[4] and w[-1] == c6[4]]
        if not r5_cands: continue

        matches.append((c1, c6, r1_cands[0], r5_cands[0]))
        if len(matches) > 30: break
    if len(matches) > 30: break

print(f"Found {len(matches)} spine pairs!")
for c1, c6, r1, r5 in matches[:15]:
    print(f"Col 1: {c1} | Col 6: {c6} | Row 1: {r1} | Row 5: {r5}")
