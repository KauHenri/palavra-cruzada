import json

with open("scripts/found_top50k_candidates.json", "r", encoding="utf-8") as f:
    cands = json.load(f)

c = cands[4]
print("Mask:", c["mask_name"])
for s in c["slots"]:
    print(f"  {s['id']} ({s['dir']}): {s['word']} -> {s['display']}")

print("\nGrid:")
clue_set = set(tuple(x) for x in c["clues"])
for r in range(1, 9):
    chars = []
    for col in range(1, 7):
        if (r, col) in clue_set:
            chars.append("[ ]")
        else:
            chars.append(c["grid"].get(f"{r},{col}", "?"))
    print(f"R{r}: " + " ".join(chars))
