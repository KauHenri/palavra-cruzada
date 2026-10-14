import json
from strict_verifier import test_level_design
from clues_database import CLUES_DB

# Helper to build a level JSON object
def build_level(id_num, title, subtitle, theme, rows, cols, raw_grid, clues_map, words_meta):
    print(f"\n==================================================")
    print(f"COMPILING LEVEL {id_num}: {title} - {subtitle} ({rows}x{cols})")
    print(f"==================================================")

    res = test_level_design(rows, cols, raw_grid, clues_map, words_meta)
    level_obj = {
        "id": id_num,
        "title": title,
        "subtitle": subtitle,
        "theme": theme,
        "rows": rows,
        "cols": cols,
        "grid": res["grid"],
        "words": res["words"]
    }
    return level_obj

levels = []

# =========================================================================
# FASE 1: COMEÇO GOSTOSO (7 rows x 7 cols)
# Words:
# Row 1: T A M B E M (TAMBÉM - 6)
# Row 2: A B A I X O (ABAIXO - 6)
# Row 3: R A (RÃ - 2) | G I N -> wait, let's make sure GIN is replaced by a Portuguese word like RIO / LUA / SOL / GOL!
# Let's verify each cell of the grid so EVERY word is 100% Portuguese!
# =========================================================================
