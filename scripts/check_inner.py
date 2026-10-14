import unicodedata
from strict_verifier import test_level_design

# Let's search inside words for boundary:
# Row 1: B E L E Z A (BELEZA)
# Col 1: B R A S I L (BRASIL)
# Col 6: A M O R E S (AMORES)
# Row 6: L I N D O S (LINDOS)

# Let's check words in top_common_clean.txt for:
# Row 2: R _ _ _ _ M
# Row 3: A _ _ _ _ O
# Row 4: S _ _ _ _ R
# Row 5: I _ _ _ _ E

with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    words_6 = [l.split()[0] for l in f if len(l.split()[0]) == 6]

r2 = [w for w in words_6 if w[0] == 'R' and w[-1] == 'M']
r3 = [w for w in words_6 if w[0] == 'A' and w[-1] == 'O']
r4 = [w for w in words_6 if w[0] == 'S' and w[-1] == 'R']
r5 = [w for w in words_6 if w[0] == 'I' and w[-1] == 'E']

print(f"Row 2 cands (R...M): {r2}")
print(f"Row 3 cands (A...O): {r3[:10]}")
print(f"Row 4 cands (S...R): {r4[:10]}")
print(f"Row 5 cands (I...E): {r5[:10]}")
