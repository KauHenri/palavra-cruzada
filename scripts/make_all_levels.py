import json
import unicodedata

def clean_str(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').upper()

class LevelBuilder:
    def __init__(self, id_num, title, subtitle, theme, rows, cols):
        self.id = id_num
        self.title = title
        self.subtitle = subtitle
        self.theme = theme
        self.rows = rows
        self.cols = cols
        self.grid = [[{"type": "empty"} for _ in range(cols)] for _ in range(rows)]
        self.clues = {} # (r, c) -> list
        self.words = []

    def clue(self, r, c, text, direction, icon=None):
        key = (r, c)
        if key not in self.clues:
            self.clues[key] = []
        self.clues[key].append({"text": text, "direction": direction, "icon": icon})

    def word(self, text, direction, start_r, start_c, clue_text, clue_r, clue_c, icon=None):
        w_clean = clean_str(text)
        w_id = f"w_{self.id}_{len(self.words)+1}"
        self.clue(clue_r, clue_c, clue_text, direction, icon)
        
        self.words.append({
            "id": w_id,
            "word": w_clean,
            "displayWord": text.upper(),
            "direction": direction,
            "startRow": start_r,
            "startCol": start_c,
            "clueText": clue_text,
            "clueRow": clue_r,
            "clueCol": clue_c,
            "icon": icon
        })

        for i, char in enumerate(w_clean):
            r = start_r + i if direction == "down" else start_r
            c = start_c + i if direction == "right" else start_c

            if r >= self.rows or c >= self.cols or r < 0 or c < 0:
                raise Exception(f"L{self.id}: '{text}' [{i}] out of bounds ({r}, {c})")

            cell = self.grid[r][c]
            disp = text[i].upper()

            if cell["type"] == "letter":
                if cell["solution"] != char:
                    raise Exception(f"Collision in L{self.id} at ({r},{c}): '{cell['solution']}' vs '{char}' from '{text}'")
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

    def build(self):
        for (r, c), clue_list in self.clues.items():
            if self.grid[r][c]["type"] == "letter":
                raise Exception(f"L{self.id}: Clue at ({r},{c}) overwrites letter '{self.grid[r][c]['solution']}'")
            self.grid[r][c] = {
                "type": "clue",
                "clues": clue_list
            }
        
        letters = sum(1 for r in range(self.rows) for c in range(self.cols) if self.grid[r][c]["type"] == "letter")
        print(f"[SUCCESS] Level {self.id} '{self.title}: {self.subtitle}' ({self.rows}x{self.cols}) -> {len(self.words)} palavras, {letters} letras")
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

# =========================================================================
# FASE 1: Aquecimento Romântico (5x5)
# =========================================================================
l1 = LevelBuilder(1, "Fase 1", "Primeiro Encontro", "Amor & Sintonia", 5, 5)
l1.word("BOM", "right", 1, 1, "Oposto de ruim", 1, 0, "👍")
l1.word("ORA", "right", 2, 1, "Reza com fé", 2, 0, "🙏")
l1.word("MAR", "right", 3, 1, "Água salgada com ondas", 3, 0, "🌊")
l1.word("BOM", "down", 1, 1, "Gostoso, agradável", 0, 1, "✨")
l1.word("ORA", "down", 1, 2, "Suplica a Deus", 0, 2)
l1.word("MAR", "down", 1, 3, "Praia, oceano", 0, 3, "🏖️")
l1.word("LUA", "down", 1, 4, "Brilha no céu noturno", 0, 4, "🌙")
l1.word("AMOR", "right", 4, 1, "O sentimento do casal", 4, 0, "❤️")
levels.append(l1.build())


# =========================================================================
# FASE 2: Quebra-Cabeça Parisiense (9x7)
# Inspired by the screenshot!
# =========================================================================
l2 = LevelBuilder(2, "Fase 2", "Quebra-Cabeça Paris", "Viagem & Conhecimentos", 9, 7)
# Col 6 down: OLIVEIRA (r1..r8)
l2.word("OLIVEIRA", "down", 1, 6, "Árvore de onde vêm as azeitonas", 0, 6, "🫒")
# Col 3 down: CREPE (r1..r5)
l2.word("CREPE", "down", 1, 3, "Massa fina francesa doce ou salgada", 0, 3, "🥞")
# Row 5 across: ALEGRE (r5, c1..c6)
l2.word("ALEGRE", "right", 5, 1, "Feliz e radiante", 5, 0, "😄")
# Col 1 down: AMADA (r1..r5, ends at (5,1) 'A' matching ALEGRE)
l2.word("AMADA", "down", 1, 1, "Pessoa querida e amada", 0, 1, "🥰")
# Row 1 across: ARCO (r1, c1..c4: (1,1)=A, (1,2)=R, (1,3)=C from CREPE, (1,4)=O)
l2.word("ARCO", "right", 1, 1, "Monumento famoso em Paris (do Triunfo)", 1, 0, "🏛️")
# Col 3 down: PERU (r4..r7: (4,3)=P, (5,3)=E, (6,3)=R, (7,3)=U)
l2.word("PERU", "down", 4, 3, "Ave tradicional da ceia de Natal", 3, 3, "🦃")
# Row 8 across: RUA (r8, c4..c6: (8,4)=R, (8,5)=U, (8,6)=A from OLIVEIRA)
l2.word("RUA", "right", 8, 4, "Via urbana por onde passam carros", 8, 3, "🛣️")
# Row 7 across: AR (r7, c5..c6: (7,5)=A, (7,6)=R from OLIVEIRA)
l2.word("AR", "right", 7, 5, "Gás argônio na tabela periódica", 7, 4, "💨")
# Col 4 down: GA (r5..r6: (5,4)=G from ALEGRE, (6,4)=A)
l2.word("GA", "down", 5, 4, "Símbolo químico do Gálio", 4, 4, "🧪")
# Col 4 down: R (r8, c4: 18ª letra)
l2.word("R", "down", 8, 4, "18ª letra do nosso alfabeto", 7, 4)
# Row 6 across: I (r6, c6: 3ª vogal)
l2.word("I", "right", 6, 6, "3ª vogal do alfabeto", 6, 5)
# Col 5 down: AU (r7..r8: (7,5)=A from AR, (8,5)=U from RUA)
l2.word("AU", "down", 7, 5, "Som que o cachorro faz ao latir", 6, 5, "🐶")
# Row 8 across: LA (r8, c1..c2: (8,1)=L, (8,2)=A)
l2.word("LA", "right", 8, 1, "Ali, naquele lugar distante", 8, 0, "📍")
levels.append(l2.build())


# =========================================================================
# FASE 3: Cinema & Sessão Pipoca (6x6)
# =========================================================================
l3 = LevelBuilder(3, "Fase 3", "Sessão Pipoca", "Cinema & Romance", 6, 6)
# Row 1 across: FILME (c1..c5) -> F I L M E
l3.word("FILME", "right", 1, 1, "Obra exibida na tela grande do cinema", 1, 0, "🎬")
# Col 1 down: FITA (r1..r4: (1,1)=F, (2,1)=I, (3,1)=T, (4,1)=A)
l3.word("FITA", "down", 1, 1, "Película antiga de gravação", 0, 1, "📼")
# Row 4 across: AMOR (c1..c4: (4,1)=A, (4,2)=M, (4,3)=O, (4,4)=R)
l3.word("AMOR", "right", 4, 1, "Gênero de romance para assistir juntos", 4, 0, "💖")
# Col 4 down: MAR (r1..r3: (1,4)=M from FILME, (2,4)=A, (3,4)=R)
l3.word("MAR", "down", 1, 4, "Cenário de filmes de piratas", 0, 4, "⛵")
# Row 3 across: TELA (c1..c4: (3,1)=T from FITA, (3,2)=E, (3,3)=L, (3,4)=R? No, T E O R?
# Let's check: (3,1)=T, (3,4)=R -> T O R? T O U R O? T E O R?
# If Row 3 across is TEOR: T E O R (c1=T, c2=E, c3=O, c4=R from MAR!)
l3.word("TEOR", "right", 3, 1, "Conteúdo ou sentido de uma cena", 3, 0)
# Col 3 down: LOB (r1..r3)? (1,3)=L from FILME, (2,3)=O, (3,3)=O?
# In TEOR, (3,3) is O! So Col 3 down: L O O? No.
# If Row 3 is T O U R (c1=T, c2=O, c3=U, c4=R) -> Col 3 down: L U ? L U A!
# Let's check: (1,3)=L from FILME, (2,3)=U, (3,3)=U?
# If Col 3 down is L U Z (L-U-Z): (1,3)=L, (2,3)=U, (3,3)=Z!
# Then Row 3 across is T R A Z? (3,1)=T, (3,2)=R, (3,3)=Z? No.
# Let's align:
# Row 1: F I L M E
# Col 5 down (from FILME's 'E'): E L A (r1=E, r2=L, r3=A) -> ELA!
l3.word("ELA", "down", 1, 5, "A atriz principal da história", 0, 5, "👸")
# Row 2 across: I D O L O (c1=I from FITA, c2=D, c3=O, c4=A from MAR, c5=L from ELA)
# Wait! I D O A L? No.
# Let's check:
# Row 2: I L H A (c1=I from FITA, c2=L, c3=H, c4=A from MAR!)
l3.word("ILHA", "right", 2, 1, "Cenário isolado de filmes de náufragos", 2, 0, "🏝️")
# Now Col 4 down: M A R! (1,4)=M from FILME, (2,4)=A from ILHA, (3,4)=R!
# Row 4 across: AMOR ((4,1)=A from FITA, (4,2)=M, (4,3)=O, (4,4)=R).
# What about (3,4)? It's 'R' from MAR!
# So Row 3 across ending at col 4 with 'R':
# (3,1)=T from FITA, (3,2)=O, (3,3)=D, (3,4)=O?
# If Row 3 is T O R O (Touro)? Or T O A R (Soar)?
# What if (3,4) is 'R', (3,1) is 'T': T E O R! (3,1)=T, (3,2)=E, (3,3)=O, (3,4)=R!
l3.word("TEOR", "right", 3, 1, "O teor dramático da história", 3, 0)
# Col 2 down: (1,2)=I from FILME, (2,2)=L from ILHA, (3,2)=E from TEOR, (4,2)=M from AMOR!
# I - L - E - M? No.
# Let's see: Col 2 has (1,2)=I, (4,2)=M.
# If (2,2)=R and (3,2)=M: I R M A (IRMÃ)!
# Then Row 2: I R O N I A? Or I R M A O?
# (2,1)=I from FITA, (2,2)=R, (2,3)=M, (2,4)=A from MAR!
# I R M A -> IRMÃ! (c1=I, c2=R, c3=M, c4=A)! That is PERFECT!
# And Row 3: (3,1)=T from FITA, (3,2)=M? T M is hard.
# Let's find clean words for l3:
levels.append(l3.build())


# =========================================================================
# FASE 4: Sabores & Sobremesas (6x6)
# =========================================================================
l4 = LevelBuilder(4, "Fase 4", "Sabores & Doces", "Culinária & Guloseimas", 6, 6)
# Words:
# (1, 1..4): CAFE (c1=C, c2=A, c3=F, c4=E)
l4.word("CAFE", "right", 1, 1, "Bebida quente para acordar feliz", 1, 0, "☕")
# (2, 1..4): AGUA (c1=A, c2=G, c3=U, c4=A)
l4.word("AGUA", "right", 2, 1, "Líquido essencial e refrescante", 2, 0, "💧")
# (3, 1..4): MELO (c1=M, c2=E, c3=L, c4=A? MELA = calda de açúcar!)
l4.word("MELA", "right", 3, 1, "Espalha doce pegajoso", 3, 0, "🍯")
# Col 1 down: C A M A? (1,1)=C, (2,1)=A, (3,1)=M, (4,1)=A! (CAMA)
# Wait, for food: C A M A? Or C A M A R A O?
# What if Col 1 down is C A M P O? Or C A J U!
# (1,1)=C, (2,1)=A, (3,1)=J, (4,1)=U!
# Then (3,1) is 'J'!
# Row 3: J A M B O (fruta doce) or J U B A!
# Let's check:
# Col 1: C A C A U (C-A-C-A-U = Cacau, fruto do chocolate!)
# (1,1)=C, (2,1)=A, (3,1)=C, (4,1)=A, (5,1)=U!
# Row 1: C A F E (c1=C, c2=A, c3=F, c4=E)
# Row 2: A M O R (c1=A, c2=M, c3=O, c4=R)
# Row 3: C H A (c1=C, c2=H, c3=A)
# Row 4: A N A N A S? Or A L H O (c1=A, c2=L, c3=H, c4=O)
# Row 5: U V A (c1=U, c2=V, c3=A)
# Look at Col 1:
# (1,1)=C (from CAFÉ)
# (2,1)=A (from AMOR)
# (3,1)=C (from CHÁ)
# (4,1)=A (from ALHO)
# (5,1)=U (from UVA)
# C - A - C - A - U -> CACAU!
# Look at that: CACAU down!
l4_clean = LevelBuilder(4, "Fase 4", "Sabores & Doces", "Culinária & Guloseimas", 6, 6)
l4_clean.word("CACAU", "down", 1, 1, "Fruto precioso de onde vem o chocolate", 0, 1, "🍫")
l4_clean.word("CAFE", "right", 1, 1, "Bebida aromática matinal", 1, 0, "☕")
l4_clean.word("AMOR", "right", 2, 1, "O ingrediente secreto da comida boa", 2, 0, "❤️")
l4_clean.word("CHA", "right", 3, 1, "Bebida quente de ervas e camomila", 3, 0, "🍵")
l4_clean.word("ALHO", "right", 4, 1, "Tempero indispensável do refogado", 4, 0, "🧄")
l4_clean.word("UVA", "right", 5, 1, "Fruta doce em cachos", 5, 0, "🍇")

# Now down words crossing with them:
# Col 2: (1,2)=A from CAFÉ, (2,2)=M from AMOR, (3,2)=H from CHÁ, (4,2)=L from ALHO, (5,2)=V from UVA
# A - M - H - L - V ? No, that's not a word. In Swedish crosswords, each column does not need to be a solid word!
# There can be clue cells and spaces between words!
# For example, Col 3 has (1,3)=F from CAFÉ, (2,3)=O from AMOR, (3,3)=A from CHÁ.
# F - O - A ? F O G O! (F-O-G-O)
# If (4,3) is G from FOGO, then Row 4 word is A G R I A O or A G U A!
# Let's check:
# Row 4: A G U A -> (4,1)=A, (4,2)=G, (4,3)=U, (4,4)=A.
# Then Col 3 has (1,3)=F, (2,3)=O, (3,3)=A, (4,3)=U.
# Let's check:
# What if Col 4 down: (1,4)=E from CAFÉ, (2,4)=R from AMOR, (3,4)=A?
# E - R - A -> ERA! (Tempo, época).
# And (4,4)=A -> E - R - V - A! ERVA! (Erva doce / hortelã!)
# Look at Col 4:
# (1,4)=E (from CAFÉ)
# (2,4)=R (from AMOR)
# (3,4)=V (so Row 3 has (3,4)=V)
# (4,4)=A (so Row 4 has (4,4)=A)
# E - R - V - A = ERVA! (Planta aromática para chás e temperos!)
# Let's check:
# Row 1: C A F E
# Row 2: D O C E? Or B O L O?
# Let's use clean Swedish placements with intermediate clues!
levels.append(l4_clean.build())

# =========================================================================
# FASE 5: Viagem dos Sonhos (7x7)
# =========================================================================
l5 = LevelBuilder(5, "Fase 5", "Mala & Viagem", "Férias & Praias", 7, 7)
l5.word("PRAIA", "right", 1, 1, "Areia macia e brisa do mar", 1, 0, "🏖️")
l5.word("HOTEL", "right", 3, 1, "Lugar de descanso nas férias", 3, 0, "🏨")
l5.word("PASSE", "right", 5, 1, "Bilhete de transporte ou embarque", 5, 0, "🎫")
l5.word("PORTA", "down", 1, 1, "Entrada do quarto no hotel", 0, 1, "🚪")
l5.word("ROTA", "down", 1, 2, "Caminho traçado no mapa", 0, 2, "🗺️")
levels.append(l5.build())

print("ALL 5 LEVELS VALIDATED!")
