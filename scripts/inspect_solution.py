import json

with open('scripts/found_authentic_solution.json', encoding='utf-8') as f:
    data = json.load(f)

print('Mask:', data['mask_name'])
print('Clues:', data['clues'])
for s in data['slots']:
    print(f"  {s['id']} ({s['dir']}): {s['word']} -> {s['display']}")

print("\nGrid:")
clue_set = set(tuple(c) for c in data['clues'])
for r in range(1, 9):
    row_chars = []
    for c in range(1, 7):
        if (r, c) in clue_set:
            row_chars.append("[ ]")
        else:
            row_chars.append(data['grid'].get(f"{r},{c}", "?"))
    print(f"R{r}: " + " ".join(row_chars))
