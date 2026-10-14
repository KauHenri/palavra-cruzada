import json
import unicodedata

def clean_str(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper()

class CrosswordLevel:
    def __init__(self, level_id, title, subtitle, theme, rows, cols):
        self.id = level_id
        self.title = title
        self.subtitle = subtitle
        self.theme = theme
        self.rows = rows
        self.cols = cols
        self.clues = {} # (r, c) -> list of clue objects
        self.words = []
        self.grid = [[{"type": "empty"} for _ in range(cols)] for _ in range(rows)]

    def add_clue(self, r, c, text, direction, icon=None):
        key = (r, c)
        if key not in self.clues:
            self.clues[key] = []
        self.clues[key].append({
            "text": text,
            "direction": direction,
            "icon": icon
        })

    def add_word(self, word, direction, start_r, start_c, clue_text, clue_r, clue_c, icon=None):
        w_clean = clean_str(word)
        w_len = len(w_clean)
        w_id = f"w_{self.id}_{len(self.words)+1}"

        # Register clue
        self.add_clue(clue_r, clue_c, clue_text, direction, icon)

        # Register word
        self.words.append({
            "id": w_id,
            "word": w_clean,
            "displayWord": word.upper(),
            "direction": direction,
            "startRow": start_r,
            "startCol": start_c,
            "clueText": clue_text,
            "clueRow": clue_r,
            "clueCol": clue_c
        })

        for i in range(w_len):
            r = start_r + i if direction == "down" else start_r
            c = start_c + i if direction == "right" else start_c

            if r >= self.rows or c >= self.cols or r < 0 or c < 0:
                raise Exception(f"Level {self.id}: '{word}' at index {i} out of bounds ({r}, {c})")

            char = w_clean[i]
            disp = word[i].upper()

            cell = self.grid[r][c]
            if cell["type"] == "clue":
                raise Exception(f"Level {self.id}: '{word}' collides with clue at ({r}, {c})")

            if cell["type"] == "letter":
                if cell["solution"] != char:
                    raise Exception(f"Collision in Level {self.id} '{self.title}' at ({r},{c}): existing '{cell['solution']}' vs '{word}' '{char}'")
                cell["wordIds"].append(w_id)
            else:
                self.grid[r][c] = {
                    "type": "letter",
                    "solution": char,
                    "displayChar": disp,
                    "currentLetter": None,
                    "isLocked": False,
                    "confirmedBy": None,
                    "wordIds": [w_id]
                }

    def compile(self):
        # Place clues into grid
        for (r, c), clue_list in self.clues.items():
            cell = self.grid[r][c]
            if cell["type"] == "letter":
                raise Exception(f"Clue placed on letter cell at ({r}, {c}) in Level {self.id}")
            self.grid[r][c] = {
                "type": "clue",
                "clues": clue_list
            }

        letter_cells = sum(1 for r in range(self.rows) for c in range(self.cols) if self.grid[r][c]["type"] == "letter")
        print(f"[OK] Level {self.id}: {self.title} - {self.subtitle} ({self.rows}x{self.cols}) -> {len(self.words)} palavras, {letter_cells} letras")
        
        return {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "theme": self.theme,
            "rows": self.rows,
            "cols": self.cols,
            "grid": self.grid,
            "words": self.words
        }

levels = []

# ========================================================
# LEVEL 1: Aquecimento (5 rows x 5 cols)
# Grid:
# Row 0: (0,0) Empty, (0,1) Clue D: CAFÉ, (0,2) Clue D: AMOR, (0,3) Clue D: RIO, (0,4) Clue D: SOL
# Row 1: (1,0) Clue R: CARS -> CARS? Or CASA? (c1=C, c2=A, c3=S, c4=A? But c3 down is RIO so c3=R! So CARA: c1=C, c2=A, c3=R, c4=A? But c4 is SOL so c4=S! So CARS? Not pt.
# Let's align:
# Row 1: C A R O (c1=C, c2=A, c3=R, c4=O)
# Row 2: A M I S ?
# Let's find words:
# Down:
# Col 1: C A M A (CAMA: r1=C, r2=A, r3=M, r4=A)
# Col 2: A M O R (AMOR: r1=A, r2=M, r3=O, r4=R)
# Col 3: F I M   (FIM:  r1=F, r2=I, r3=M)
# Col 4: E L E   (ELE:  r1=E, r2=L, r3=E)
# Let's check Row 1 (c1..c4): C A F E -> CAFÉ! Perfect! (C-A-F-E)
# Let's check Row 2 (c1..c4): A M I L -> AMIL? Or A M I G O?
# If col 4 is E L A (r1=E, r2=L, r3=A):
# Row 2 (c1..c4): A M I L?
# What if col 3 is R I O (r1=R, r2=I, r3=O) -> Row 1 is C A R E (CARE? CARO?):
# If Row 1 is C A R O (c1=C, c2=A, c3=R, c4=O):
# Down words:
# Col 1: C A M A (r1=C, r2=A, r3=M, r4=A)
# Col 2: A N O S (r1=A, r2=N, r3=O, r4=S)
# Col 3: R I O   (r1=R, r2=I, r3=O)
# Col 4: O L A   (r1=O, r2=L, r3=A) -> OLÁ!
# Row 1 (c1..c4): C A R O -> CARO!
# Row 2 (c1..c4): A N I L -> ANIL! (Cor azulada profunda)
# Row 3 (c1..c4): M O O A? Not a word.
# ========================================================

# Let's write a small solver in python that finds perfect grids for us:
with open("C:/Users/Kauã Silva/AppData/Local/Temp/pt_words.txt", "w") as f:
    pass

print("Writing generator...")
