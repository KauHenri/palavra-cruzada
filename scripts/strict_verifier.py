import json

# Let's write a script to test and build a completely verified Swedish Crossword level
from check_integrity import check_grid

def test_level_design(rows, cols, raw_grid, clues_map, words_meta):
    # Verify bounds and types
    grid = []
    for r in range(rows):
        grid_row = []
        for c in range(cols):
            val = raw_grid[r][c]
            if val == "EMPTY":
                grid_row.append({"type": "empty"})
            elif val == "CLUE":
                key = (r, c)
                if key not in clues_map:
                    raise Exception(f"Missing clue at ({r}, {c})")
                grid_row.append({"type": "clue", "clues": clues_map[key]})
            else:
                grid_row.append({
                    "type": "letter",
                    "solution": val,
                    "displayChar": val,
                    "currentLetter": None,
                    "isLocked": False,
                    "confirmedBy": None,
                    "wordIds": []
                })
        grid.append(grid_row)

    words_list = []
    for w in words_meta:
        w_clean = w["word"].upper()
        w_len = len(w_clean)
        w_id = w["id"]
        sr, sc = w["startRow"], w["startCol"]
        direction = w["direction"]

        for i in range(w_len):
            r = sr + i if direction == "down" else sr
            c = sc + i if direction == "right" else sc

            if r >= rows or c >= cols:
                raise Exception(f"Word '{w['word']}' goes out of bounds ({r}, {c})")

            cell = grid[r][c]
            if cell["type"] != "letter":
                raise Exception(f"Word '{w['word']}' letter {i} expects letter at ({r}, {c}), found {cell['type']}")

            if cell["solution"] != w_clean[i]:
                raise Exception(f"Word '{w['word']}' mismatch at ({r}, {c}): expected '{w_clean[i]}', cell has '{cell['solution']}'")

            cell["wordIds"].append(w_id)

        # Clue check: clue must not contain the target word! (e.g., "VARA" in "VARA DE PESCA")
        import re
        import unicodedata
        clue_text = w["clueText"]
        # Remove accents for fair comparison
        clue_text_clean = ''.join(c for c in unicodedata.normalize('NFD', clue_text) if unicodedata.category(c) != 'Mn').upper()
        # Word boundary match (e.g., VARA in VARA DE PESCA, or PESCA if PESCA is the word)
        if re.search(r'\b' + re.escape(w_clean) + r'\b', clue_text_clean):
            raise Exception(f"SPOILER ALERT! Word '{w_clean}' is contained as a word inside clue '{clue_text}'!")
        if len(w_clean) >= 4 and w_clean in clue_text_clean:
            raise Exception(f"SPOILER ALERT! Word '{w_clean}' substring is inside clue '{clue_text}'!")

        words_list.append({
            "id": w_id,
            "word": w_clean,
            "displayWord": w.get("displayWord", w_clean),
            "direction": direction,
            "startRow": sr,
            "startCol": sc,
            "clueText": w["clueText"],
            "clueRow": w["clueRow"],
            "clueCol": w["clueCol"],
            "icon": None
        })

    # Verify no orphan letters
    for r in range(rows):
        for c in range(cols):
            cell = grid[r][c]
            if cell["type"] == "letter" and len(cell["wordIds"]) == 0:
                raise Exception(f"Orphan letter at ({r}, {c})")

    # Now verify: does EVERY contiguous sequence of letters in the grid correspond to a registered word?
    # This prevents the "BOML" or "MARA" bug!
    # Check every horizontal contiguous block:
    for r in range(rows):
        c = 0
        while c < cols:
            if grid[r][c]["type"] == "letter":
                c_start = c
                letters = []
                while c < cols and grid[r][c]["type"] == "letter":
                    letters.append(grid[r][c]["solution"])
                    c += 1
                word_str = "".join(letters)
                # Check if this word exists in words_list
                matches = [w for w in words_list if w["direction"] == "right" and w["startRow"] == r and w["startCol"] == c_start]
                if not matches:
                    raise Exception(f"Unaccounted horizontal word '{word_str}' at row {r}, col {c_start} to {c-1}")
                if matches[0]["word"] != word_str:
                    raise Exception(f"Horizontal word mismatch at row {r}, col {c_start}: expected '{matches[0]['word']}', grid has '{word_str}'")
            else:
                c += 1

    # Check every vertical contiguous block:
    for c in range(cols):
        r = 0
        while r < rows:
            if grid[r][c]["type"] == "letter":
                r_start = r
                letters = []
                while r < rows and grid[r][c]["type"] == "letter":
                    letters.append(grid[r][c]["solution"])
                    r += 1
                word_str = "".join(letters)
                matches = [w for w in words_list if w["direction"] == "down" and w["startRow"] == r_start and w["startCol"] == c]
                if not matches:
                    raise Exception(f"Unaccounted vertical word '{word_str}' at row {r_start} to {r-1}, col {c}")
                if matches[0]["word"] != word_str:
                    raise Exception(f"Vertical word mismatch at col {c}, row {r_start}: expected '{matches[0]['word']}', grid has '{word_str}'")
            else:
                r += 1

    print(f"[PERFECTION CONFIRMED] Grid {rows}x{cols} has {len(words_list)} words, 0 spoilers, 0 pseudo-words!")
    return {
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "words": words_list
    }
