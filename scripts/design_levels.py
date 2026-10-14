# Python script to design, validate and format crossword levels
import unicodedata
import json

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

def make_level(level_id, title, subtitle, theme, rows, cols, clues_data, words_data):
    # Initialize grid
    grid = [[{"type": "empty"} for _ in range(cols)] for _ in range(rows)]
    
    # Place clues
    for c in clues_data:
        r, col = c["row"], c["col"]
        grid[r][col] = {
            "type": "clue",
            "clues": c["clues"]
        }
        
    # Place words
    words_list = []
    for idx, w in enumerate(words_data):
        w_clean = strip_accents(w["word"])
        w_len = len(w_clean)
        w_id = f"w_{level_id}_{idx+1}"
        
        dir_name = w["direction"]
        sr, sc = w["startRow"], w["startCol"]
        
        for i in range(w_len):
            r = sr + i if dir_name == "down" else sr
            c = sc + i if dir_name == "right" else sc
            
            if r >= rows or c >= cols or r < 0 or c < 0:
                raise Exception(f"Word {w['word']} out of bounds at ({r}, {c})")
                
            cell = grid[r][c]
            if cell["type"] == "clue":
                raise Exception(f"Word {w['word']} collides with clue at ({r}, {c})")
                
            char = w_clean[i]
            disp = w["word"][i].upper()
            
            if cell["type"] == "letter":
                if cell["solution"] != char:
                    raise Exception(f"Collision in level {level_id} at ({r}, {c}): cell has '{cell['solution']}', '{w['word']}' has '{char}'")
                cell["wordIds"].append(w_id)
            else:
                grid[r][c] = {
                    "type": "letter",
                    "solution": char,
                    "displayChar": disp,
                    "currentLetter": None,
                    "isLocked": False,
                    "confirmedBy": None,
                    "wordIds": [w_id]
                }
                
        words_list.append({
            "id": w_id,
            "word": w_clean,
            "displayWord": w["word"].upper(),
            "direction": dir_name,
            "startRow": sr,
            "startCol": sc,
            "clueText": w["clueText"],
            "clueRow": w["clueRow"],
            "clueCol": w["clueCol"]
        })
        
    # Count letters
    letter_count = sum(1 for r in range(rows) for c in range(cols) if grid[r][c]["type"] == "letter")
    clue_count = sum(1 for r in range(rows) for c in range(cols) if grid[r][c]["type"] == "clue")
    
    print(f"Level {level_id}: {title} - {subtitle} ({rows}x{cols}) | Words: {len(words_list)} | Letters: {letter_count} | Clues: {clue_count}")
    
    # Print ASCII grid
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            cell = grid[r][c]
            if cell["type"] == "clue":
                row_str += "[C] "
            elif cell["type"] == "letter":
                row_str += f" {cell['solution']}  "
            else:
                row_str += " .  "
        print(row_str)
    print()
    
    return {
        "id": level_id,
        "title": title,
        "subtitle": subtitle,
        "theme": theme,
        "rows": rows,
        "cols": cols,
        "grid": grid,
        "words": words_list
    }

# ----------------- DESIGNING LEVELS -----------------

# LEVEL 1: Aquecimento Doce (5 x 5)
# Words:
# Across:
# AMOR (row 0, col 1..4)
# RIO (row 2, col 1..3)
# SOL (row 4, col 1..3)
# Down:
# AR (col 1, row 1..2) -> wait:
# Let's align:
# Grid:
# Row 0: [Clue right: AMOR] A  M  O  R
# Row 1: [Clue right: PÉ]   P  É  [Clue down: OURO] [Clue down: RIR]
# Row 2: [Clue right: LEI]  L  E  I  .
# Let's check down words:
# col 1: A P L -> APL? Not a common word.
# Let's design mathematically:

# Let's build a clean 5x5:
# Words across:
# (0,1): AMOR (4) -> A M O R. Clue at (0,0) [right: Sentimento maior]
# (2,1): LUA (3) -> L U A. Clue at (2,0) [right: Satélite da Terra]
# (4,1): PAZ (3) -> P A Z. Clue at (4,0) [right: Ausência de guerra]
# Down words crossing them:
# (1,1): A.. row 0 is A, row 1 is L, row 2 is L? No, row 0 is A, row 2 is L, row 4 is P:
# col 1 has: r0=A, r2=L, r4=P.
# If word down is ALPE (col 1, r0..4): A L P E (4) -> (0,1)=A, (1,1)=L, (2,1)=P...
# Then row 2 starts with P!

# Let's test a simple well-known interlocking grid:
# Horizontal:
# Row 1: CASA (c1..c4) -> C A S A (clue at (1,0) "Lar doce lar")
# Row 2: AMOR (c1..c4) -> A M O R (clue at (2,0) "Grande afeto")
# Row 3: RISO (c1..c4) -> R I S O (clue at (3,0) "Gargalhada")
# Down:
# Col 1: C A R (r1..r3) -> CAR? Or COR (r1..r3 with CASA, O..., RISO) -> (1,1)=C, (2,1)=O, (3,1)=R.
# If (2,1) is O, word is OURO!
# Let's check:
# Row 1: C A S A
# Row 2: O U R O
# Row 3: R I S O
# Down:
# Col 1: C O R (Cor)
# Col 2: A U I ? Not a word.

# Let's do a standard crossword intersection with clues in between:
# Row 0: [Clue 0,0 right: SOL, down: SOMA]
# (0,1)=S, (0,2)=O, (0,3)=L, (0,4)=[Clue down: LUA]
# Row 1: (1,0)=O, (1,1)=[Clue right: OVO], (1,2)=V, (1,3)=O, (1,4)=U
# Row 2: (2,0)=M, (2,1)=A, (2,2)=R, (2,3)=[Clue right: AR], (2,4)=A
# Row 3: (3,0)=A, (3,1)=[Clue right: BEIJO] -> wait!

print("Testing python script setup")
