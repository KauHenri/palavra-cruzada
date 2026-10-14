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
        print(f"[OK] Level {self.id} '{self.title}: {self.subtitle}' ({self.rows}x{self.cols}) -> {len(self.words)} words, {letters} letter cells")
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
# LEVEL 1: Aquecimento Romântico (5x5)
# =========================================================================
l1 = LevelBuilder(1, "Fase 1", "Primeiro Encontro", "Amor & Sintonia", 5, 5)
l1.word("BOM", "right", 1, 1, "Oposto de ruim", 1, 0, "👍")
l1.word("ORA", "right", 2, 1, "Reza com fé e carinho", 2, 0, "🙏")
l1.word("MAR", "right", 3, 1, "Água salgada com ondas", 3, 0, "🌊")
l1.word("BOM", "down", 1, 1, "Gostoso, agradável", 0, 1, "✨")
l1.word("ORA", "down", 1, 2, "Suplica com devoção", 0, 2)
l1.word("MAR", "down", 1, 3, "Praia, oceano", 0, 3, "🏖️")
l1.word("LUA", "down", 1, 4, "Brilha no céu noturno", 0, 4, "🌙")
l1.word("AMOR", "right", 4, 1, "O sentimento do casal", 4, 0, "❤️")
levels.append(l1.build())


# =========================================================================
# LEVEL 2: Quebra-Cabeça Parisiense (9x7)
# =========================================================================
l2 = LevelBuilder(2, "Fase 2", "Quebra-Cabeça Paris", "Viagem & Conhecimentos", 9, 7)
# Down col 6: OLIVEIRA (r1..r8)
l2.word("OLIVEIRA", "down", 1, 6, "Árvore de onde vêm as azeitonas", 0, 6, "🫒")
# Across row 5: ALEGRE (r5, c1..c6)
l2.word("ALEGRE", "right", 5, 1, "Feliz e radiante", 5, 0, "😄")
# Down col 1: AMADA (r1..r5, ends at (5,1) 'A' from ALEGRE)
l2.word("AMADA", "down", 1, 1, "Pessoa querida e amada", 0, 1, "🥰")
# Down col 3: CR (r1..r2: (1,3)=C, (2,3)=R)
l2.word("CR", "down", 1, 3, "Iniciais de crepe na foto (cr-...-e)", 0, 3, "🥞")
# Down col 3: PERU (r4..r7: (4,3)=P, (5,3)=E, (6,3)=R, (7,3)=U)
l2.word("PERU", "down", 4, 3, "Ave tradicional da ceia de Natal", 3, 3, "🦃")
# Across row 1: ARCO (r1, c1..c4: (1,1)=A, (1,2)=R, (1,3)=C, (1,4)=O)
l2.word("ARCO", "right", 1, 1, "Monumento famoso em Paris (do Triunfo)", 1, 0, "🏛️")
# Across row 8: RUA (r8, c4..c6: (8,4)=R, (8,5)=U, (8,6)=A from OLIVEIRA)
l2.word("RUA", "right", 8, 4, "Via urbana por onde passam carros", 8, 3, "🛣️")
# Across row 7: AR (r7, c5..c6: (7,5)=A, (7,6)=R from OLIVEIRA)
l2.word("AR", "right", 7, 5, "Gás argônio na tabela periódica", 7, 4, "💨")
# Down col 4: GA (r5..r6: (5,4)=G from ALEGRE, (6,4)=A)
l2.word("GA", "down", 5, 4, "Símbolo químico do Gálio", 4, 4, "🧪")
# Down col 4: R (r8, c4: 18ª letra)
l2.word("R", "down", 8, 4, "18ª letra do nosso alfabeto", 7, 4)
# Across row 6: I (r6, c6: 3ª vogal)
l2.word("I", "right", 6, 6, "3ª vogal do alfabeto", 6, 5)
# Down col 5: AU (r7..r8: (7,5)=A from AR, (8,5)=U from RUA)
l2.word("AU", "down", 7, 5, "Som que o cachorro faz ao latir", 6, 5, "🐶")
# Across row 8: LA (r8, c1..c2: (8,1)=L, (8,2)=A)
l2.word("LA", "right", 8, 1, "Ali, naquele lugar distante", 8, 0, "📍")
levels.append(l2.build())


# =========================================================================
# LEVEL 3: Sabores & Delícias (6x6)
# =========================================================================
l3 = LevelBuilder(3, "Fase 3", "Sabores & Delícias", "Culinária & Sobremesas", 6, 6)
# Row 1: CAFÉ (c1..c4: (1,1)=C, (1,2)=A, (1,3)=F, (1,4)=E)
l3.word("CAFE", "right", 1, 1, "Bebida quente para começar o dia", 1, 0, "☕")
# Col 1: CASA (r1..r4: (1,1)=C, (2,1)=A, (3,1)=S, (4,1)=A)
l3.word("CASA", "down", 1, 1, "Lar aconchegante do casal", 0, 1, "🏡")
# Row 2: AMOR (c1..c4: (2,1)=A, (2,2)=M, (2,3)=O, (2,4)=R)
l3.word("AMOR", "right", 2, 1, "O tempero principal da nossa vida", 2, 0, "❤️")
# Col 2: MEL (r2..r4: (2,2)=M from AMOR, (3,2)=E, (4,2)=L) -> Clue at (0,2)!
# But wait, (1,2) is 'A' from CAFÉ!
# So MEL starting at (2,2) would have clue above it at (1,2), but (1,2) is 'A'!
# In Swedish crosswords, if (1,2) is a letter, the word in col 2 either starts at (1,2) with 'A', OR its clue is at (0,2) and the word starts at (1,2)!
# If col 2 starts at (1,2) with 'A', the word can be A M E I or A M O R!
# (1,2)=A, (2,2)=M from AMOR, (3,2)=O, (4,2)=R -> AMOR down!
# Or A M I G O (r1=A, r2=M, r3=I, r4=G, r5=O) -> AMIGO!
# Let's check AMIGO down at col 2:
# (1,2)=A (matches CAFÉ: C-A-F-E)
# (2,2)=M (matches AMOR: A-M-O-R)
# (3,2)=I
# (4,2)=G
# (5,2)=O
# Clue at (0,2) pointing down: "Companheiro leal e querido"!
# That is completely brilliant!
l3.word("AMIGO", "down", 1, 2, "Companheiro leal e querido", 0, 2, "🤝")

# Now Col 4 down: starts at (1,4) with 'E' from CAFÉ!
# (1,4)=E, (2,4)=R from AMOR, (3,4)=A -> ERA! (Tempo, época).
# Clue at (0,4) pointing down: "Período marcante da história"!
l3.word("ERA", "down", 1, 4, "Período marcante da história", 0, 4, "⏳")

# Now Row 3 across:
# (3,1)=S from CASA (C-A-S-A)
# (3,2)=I from AMIGO (A-M-I-G-O)
# (3,3)=M
# (3,4)=A from ERA (E-R-A)
# (3,1)=S, (3,2)=I, (3,3)=M, (3,4)=A -> S I M A? No, S I M!
# (3,1)=S, (3,2)=I, (3,3)=M -> SIM! (Resposta positiva e alegre no altar!)
l3.word("SIM", "right", 3, 1, "Resposta afirmativa e feliz no altar", 3, 0, "💍")

# Now Row 4 across:
# (4,1)=A from CASA
# (4,2)=G from AMIGO
# (4,3)=U
# (4,4)=A
# A - G - U - A -> ÁGUA! (Líquido vital e refrescante!)
l3.word("AGUA", "right", 4, 1, "Líquido vital essencial para a vida", 4, 0, "💧")

# Col 3 down:
# (1,3)=F from CAFÉ, (2,3)=O from AMOR, (3,3)=M from SIM, (4,3)=U from ÁGUA!
# What about (1,3)=F, (2,3)=O, (3,3)=G, (4,3)=O?
# If Row 3 has (3,3)=G: S I G A (Siga em frente)!
# (3,1)=S, (3,2)=I, (3,3)=G, (3,4)=A from ERA!
# S - I - G - A -> SIGA!
# And (4,3) from ÁGUA is U?
# What if Row 4 is A G O R A: (4,1)=A, (4,2)=G, (4,3)=O, (4,4)=R?
# If (4,3)=O, then Col 3: (1,3)=F, (2,3)=O, (3,3)=G, (4,3)=O!
# F - O - G - O -> FOGO!
# Look at Col 3: F O G O! (Fogo da paixão!)
# (1,3)=F (from CAFÉ)
# (2,3)=O (from AMOR)
# (3,3)=G (from SIGA)
# (4,3)=O (from AGORA)
# Clue at (0,3) pointing down: "Chama ardente e calorosa"!
# That is ASTONISHING! Everything matches!
# Let's adjust Row 3 to SIGA and Row 4 to AGORA:
l3 = LevelBuilder(3, "Fase 3", "Sabores & Amor", "Culinária & Paixão", 6, 6)
l3.word("CAFE", "right", 1, 1, "Bebida quente para começar o dia", 1, 0, "☕")
l3.word("CASA", "down", 1, 1, "Lar aconchegante do casal", 0, 1, "🏡")
l3.word("AMOR", "right", 2, 1, "O tempero principal da nossa vida", 2, 0, "❤️")
l3.word("AMIGO", "down", 1, 2, "Companheiro leal e querido", 0, 2, "🤝")
l3.word("FOGO", "down", 1, 3, "Chama ardente da paixão", 0, 3, "🔥")
l3.word("ERA", "down", 1, 4, "Período marcante da história", 0, 4, "⏳")
l3.word("SIGA", "right", 3, 1, "Em frente! Instrução de trânsito ou GPS", 3, 0, "🚦")
l3.word("AGORA", "right", 4, 1, "Neste exato momento, sem demora", 4, 0, "⏰")
levels.append(l3.build())


# =========================================================================
# LEVEL 4: Viagem & Férias (6x6)
# =========================================================================
l4 = LevelBuilder(4, "Fase 4", "Pé na Estrada", "Viagens & Aventuras", 6, 6)
# (1, 1..4): PRAIA (wait, 5 letters: c1..c5)
l4.word("PRAIA", "right", 1, 1, "Areia macia, ondas e sol", 1, 0, "🏖️")
# (1, 1) down: P A Z (r1=P, r2=A, r3=Z)
l4.word("PAZ", "down", 1, 1, "A tranquilidade das férias", 0, 1, "🕊️")
# (2, 1..4): AMOR ((2,1)=A from PAZ, (2,2)=M, (2,3)=O, (2,4)=R)
l4.word("AMOR", "right", 2, 1, "Viajar juntinhos é puro...", 2, 0, "💖")
# Col 4 down: ROTA (r2..r5: (2,4)=R from AMOR, (3,4)=O, (4,4)=T, (5,4)=A)
l4.word("ROTA", "down", 2, 4, "Caminho traçado no GPS", 1, 4, "🧭")
# Row 4 across: FOTO (c1=F, c2=O, c3=T, c4=O? But (4,4) is 'T' from ROTA!)
# If (4,4) is T, then (4,1)=A, (4,2)=U, (4,3)=T, (4,4)=O? (4,4) is T!
# Word ending with T? In Portuguese, words don't end in T.
# But ROTA can start at (1,4): (1,4)=A from PRAIA (P-R-A-I-A: (1,1)=P, (1,2)=R, (1,3)=A, (1,4)=I, (1,5)=A)!
# Look: (1,4) in PRAIA is 'I'!
# Word down starting with 'I' at (1,4):
# I L H A (r1=I, r2=L, r3=H, r4=A)!
# Look at that: ILHA! (Ilha paradisíaca no mar!)
# (1,4)=I (from PRAIA)
# (2,4)=L
# (3,4)=H
# (4,4)=A
# And at row 2: (2,1)=A from PAZ, (2,2)=Z, (2,3)=U, (2,4)=L -> AZUL!
# (2,1)=A (from PAZ: P-A-Z)
# (2,2)=Z
# (2,3)=U
# (2,4)=L (matches ILHA's 'L' at (2,4)!)
# AZUL: "A cor do mar do Caribe"!
# Now look at Row 4: ending with 'A' at (4,4) from ILHA!
# M A L A (c1=M, c2=A, c3=L, c4=A)! (Mala de viagem!)
# (4,1)=M
# (4,2)=A
# (4,3)=L
# (4,4)=A (matches ILHA's 'A' at (4,4)!)
# Look at that perfection:
# PRAIA across at Row 1!
# PAZ down at Col 1!
# AZUL across at Row 2!
# ILHA down at Col 4!
# MALA across at Row 4!
# Col 2 down: (1,2)=R from PRAIA, (2,2)=Z from AZUL, (3,2)=empty, (4,2)=A from MALA.
# If (3,1) is 'Z' from PAZ, Row 3 can be:
# Z E L O (Zelo / carinho!)
# (3,1)=Z (from PAZ: P-A-Z)
# (3,2)=E
# (3,3)=L
# (3,4)=O? But ILHA has (3,4)='H'!
# What word starts with Z and has 'H' at index 3?
# Or clue at (3,2) and (3,3)!
l4_clean = LevelBuilder(4, "Fase 4", "Pé na Estrada", "Viagens & Praias", 6, 6)
l4_clean.word("PRAIA", "right", 1, 1, "Areia macia, ondas e sol", 1, 0, "🏖️")
l4_clean.word("PAZ", "down", 1, 1, "Tranquilidade nas férias", 0, 1, "🕊️")
l4_clean.word("AZUL", "right", 2, 1, "A cor do mar cristalino", 2, 0, "🌊")
l4_clean.word("ILHA", "down", 1, 4, "Destino paradisíaco cercado de água", 0, 4, "🏝️")
l4_clean.word("MALA", "right", 4, 1, "Bagagem para levar as roupas", 4, 0, "🧳")
levels.append(l4_clean.build())


# =========================================================================
# LEVEL 5: Noite de Cinema (6x6)
# =========================================================================
l5 = LevelBuilder(5, "Fase 5", "Noite de Estreia", "Cinema & Emoção", 6, 6)
# Across:
# Row 1: CENA (c1..c4: (1,1)=C, (1,2)=E, (1,3)=N, (1,4)=A)
l5.word("CENA", "right", 1, 1, "Momento marcante do filme", 1, 0, "🎬")
# Col 1: COR (r1..r3: (1,1)=C, (2,1)=O, (3,1)=R)
l5.word("COR", "down", 1, 1, "Efeito visual da fotografia", 0, 1, "🎨")
# Row 2: OURO (c1..c4: (2,1)=O from COR, (2,2)=U, (2,3)=R, (2,4)=O)
l5.word("OURO", "right", 2, 1, "A cor da cobiçada estatueta do Oscar", 2, 0, "🏆")
# Col 4: ATO (r1..r3: (1,4)=A from CENA, (2,4)=T? In OURO, (2,4) is 'O'!
# So Col 4 down: A O ? A O R T A?
# What if OURO ends with A? O U R A (Oura?)
# What if Row 2 is O L H A (c1=O, c2=L, c3=H, c4=A)?
# (2,1)=O (from COR)
# (2,2)=L
# (2,3)=H
# (2,4)=A
# And Col 4 down: (1,4)=A from CENA, (2,4)=A from OLHA, (3,4)=R -> A S A? A B A!
# (1,4)=A, (2,4)=B? Then Row 2 is O B R A! (OBRA cinematográfica!)
# LOOK AT OBRA:
# (2,1)=O (from COR: C-O-R)
# (2,2)=B
# (2,3)=R
# (2,4)=A
# OBRA: "Uma grande obra de arte no cinema!"
# And Col 4 down:
# (1,4)=A (from CENA: C-E-N-A)
# (2,4)=A (from OBRA: O-B-R-A)
# (3,4)=R
# A - A - R? Or (1,4)=A, (2,4)=A, (3,4)=S?
# What if Col 4 is A R T E:
# (1,4)=A (from CENA)
# (2,4)=R -> so Row 2 ends in 'R'!
# What 4-letter word starts with 'O' and ends in 'R'?
# O S C A R! (5 letters: c1=O, c2=S, c3=C, c4=A, c5=R)
# Or O D O R (4 letters)!
# Or A M O R (c1=A, c2=M, c3=O, c4=R)!
# Look at that:
# Row 1: C A R O (c1=C, c2=A, c3=R, c4=O)
# Row 2: A M O R (c1=A, c2=M, c3=O, c4=R)
# Row 3: R O S A (c1=R, c2=O, c3=S, c4=A)
# Down:
# Col 1: C A R (r1=C, r2=A, r3=R)
# Col 2: A M O (r1=A, r2=M, r3=O) -> AMO! (Eu te amo!)
# Col 3: R O S (r1=R, r2=O, r3=S)
# Col 4: O R A (r1=O, r2=R, r3=A) -> ORA!
# Look at Col 2: A M O! (Eu te amo!)
# Look at Col 4: O R A!
# Look at Row 2: A M O R!
# Look at Row 3: R O S A!
# That is pure magic!
l5_clean = LevelBuilder(5, "Fase 5", "Clássicos do Cinema", "Romance na Telona", 5, 5)
l5_clean.word("CARO", "right", 1, 1, "Ingresso caro ou pessoa querida", 1, 0, "🎟️")
l5_clean.word("AMOR", "right", 2, 1, "A história mais bonita contada no cinema", 2, 0, "❤️")
l5_clean.word("ROSA", "right", 3, 1, "Flor entregue no encontro romântico", 3, 0, "🌹")
l5_clean.word("CAR", "down", 1, 1, "Carro antigo de colecionador nos filmes", 0, 1, "🚗")
l5_clean.word("AMO", "down", 1, 2, "'Eu te amo', frase clássica do casal", 0, 2, "💬")
l5_clean.word("ORA", "down", 1, 4, "Expressão de torcida pelo final feliz", 0, 4, "✨")
levels.append(l5_clean.build())

# Write out levels.ts
print(f"Total compiled levels: {len(levels)}")

ts_content = "import type { LevelDefinition } from '../types/game';\n\n"
ts_content += "export const LEVELS: LevelDefinition[] = " + json.dumps(levels, indent=2, ensure_ascii=False) + ";\n"

with open("c:/ProjetosIA/Palavra_Cruzada/src/data/levels.ts", "w", encoding="utf-8") as f:
    f.write(ts_content)

print("[SUCCESS] src/data/levels.ts written successfully!")
