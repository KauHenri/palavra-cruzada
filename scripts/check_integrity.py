import json

# Script to verify Level 2 and 3 and add them to levels.ts
def check_grid(level_def):
    grid = level_def["grid"]
    rows = level_def["rows"]
    cols = level_def["cols"]
    words = level_def["words"]

    # Map of letter cell coordinates
    letter_cells = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c]["type"] == "letter":
                letter_cells.add((r, c))

    # Covered by across
    covered_across = set()
    # Covered by down
    covered_down = set()

    for w in words:
        w_len = len(w["word"])
        dir_name = w["direction"]
        sr, sc = w["startRow"], w["startCol"]

        for i in range(w_len):
            r = sr + i if dir_name == "down" else sr
            c = sc + i if dir_name == "right" else sc

            if (r, c) not in letter_cells:
                raise Exception(f"Word {w['word']} uses non-letter cell ({r}, {c})")

            actual = grid[r][c]["solution"]
            expected = w["word"][i]
            if actual != expected:
                raise Exception(f"Word {w['word']} mismatch at ({r}, {c}): expected '{expected}', got '{actual}'")

            if dir_name == "right":
                covered_across.add((r, c))
            else:
                covered_down.add((r, c))

    # Check for unassigned letter cells
    all_covered = covered_across.union(covered_down)
    if all_covered != letter_cells:
        unassigned = letter_cells - all_covered
        raise Exception(f"Unassigned cells: {unassigned}")

    print(f"Level {level_def['id']} '{level_def['title']}' is 100% VALID! ({len(words)} words, {len(letter_cells)} letters)")

# Let's verify existing levels.ts
with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "r", encoding="utf-8") as f:
    text = f.read()

# Extract JSON
json_start = text.find("= [") + 2
json_end = text.rfind("]") + 1
levels_json = json.loads(text[json_start:json_end])

for lvl in levels_json:
    check_grid(lvl)
