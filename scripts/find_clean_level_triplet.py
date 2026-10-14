import json

with open("scripts/all_expanded_sols.json", "r", encoding="utf-8") as f:
    sols = json.load(f)

# Names and unwanted words to reject:
bad_words = {
    'CLAIRE', 'ELAINE', 'AVATAR', 'TURNER', 'LARA', 'ROSE', 'MANA', 'MAMA',
    'ART', 'ALIENS', 'SA', 'ADA', 'ARI', 'ME', 'DORIAN', 'ACE', 'ST', 'EST',
    'BELMAZ', 'ZORAIA', 'RUEIRO', 'LOROSA', 'ARATUS', 'ICAPUI', 'TA', 'SI', 'TI',
    'SURTAR', 'SERENA'
}

clean_sols = []
for i, s in enumerate(sols):
    all_w = set(s.values())
    if any(bw in all_w for bw in bad_words):
        continue
    # Check that all words are strictly content or valid
    clean_sols.append((i, s))

print(f"Total clean solutions: {len(clean_sols)} out of {len(sols)}")
for idx, s in clean_sols[:15]:
    print(f"\nSolution #{idx}:")
    for k in ["R1", "R2", "R3", "R4", "R5", "R6", "C1_top", "C2_top", "C3", "C4", "C5_top", "C6_top", "C1_bot", "C2_bot", "C5_bot", "C6_bot"]:
        print(f"  {k}: {s[k]}", end=", ")
    print()
