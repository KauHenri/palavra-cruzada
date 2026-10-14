import unicodedata

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

common_by_len = {}
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        clean, orig, freq = line.strip().split()
        l = len(clean)
        if l not in common_by_len: common_by_len[l] = []
        common_by_len[l].append(clean)

words_6 = common_by_len.get(6, [])

theme_words_8 = [
    "PORTUGAL", "BRASILIA", "NATUREZA", "FAMILIAR", "ESTRELAS", "HISTORIA",
    "PALAVRAS", "VIAGENS", "VIJANTE", "AMOROSOS", "CARINHOS", "ALEGRIAS",
    "ESPERADO", "BONITOS", "SENTINDO", "PENSANDO", "FALANDO", "OLHANDO"
]

for c1 in theme_words_8:
    for c6 in theme_words_8:
        if c1 == c6: continue
        r1_cands = [w for w in words_6 if w[0] == c1[0] and w[-1] == c6[0]]
        r5_cands = [w for w in words_6 if w[0] == c1[4] and w[-1] == c6[4]]
        if r1_cands and r5_cands:
            print(f"Col 1: {c1} | Col 6: {c6} | Row 1: {r1_cands[:3]} | Row 5: {r5_cands[:3]}")
