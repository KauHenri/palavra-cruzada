# Python script to build Fase 2 and Fase 3 with 100% real words and interior clues
import json

# Let's verify Fase 2: "Quebra-cabeça 19 - Destinos & Viagens" (9 rows x 7 cols)
# Grid:
# Col 1 down (r1..r8): B-R-A-S-I-L-I-A (BRASÍLIA: Capital federal do Brasil)
# Col 6 down (r1..r8): P-O-R-T-U-G-A-L (PORTUGAL: País europeu irmão)
# Row 5 across (r5, c1..c6): I-L-H-A-U-G?
# If at (5, 3) is a clue cell:
# (5, 1) = I, (5, 2) = A -> IA (Inteligência Artificial)
# (5, 4) = R, (5, 5) = U, (5, 6) = A -> RUA! (Via urbana)
# Look at that: (5, 6) is 'U' from PORTUGAL:
# P - O - R - T - **U** - G - A - L -> row 5 is indeed 'U'!
# So (5, 4)=R, (5, 5)=U, (5, 6)=A? Wait, (5, 6) is 'U'!
# What 3-letter word ends in 'U'?
# C - É - U (CÉU: "Onde voam os aviões")!
# (5, 4) = C
# (5, 5) = E
# (5, 6) = U (matches PORTUGAL's 'U' at row 5!)
# C - E - U = CÉU!
# That is pure genius!

# Let's check Row 8 across (r8, c1..c6):
# (8, 1) = A (from BRASÍLIA)
# (8, 6) = L (from PORTUGAL)
# If (8, 3) is a clue cell:
# (8, 1) = A, (8, 2) = R -> AR! ("O que respiramos")
# (8, 4) = S, (8, 5) = O, (8, 6) = L -> SOL! ("Aquece os dias de praia")
# Look at that:
# Row 8: (8, 1)=A, (8, 2)=R -> AR!
# (8, 3) = CLUE!
# (8, 4)=S, (8, 5)=O, (8, 6)=L -> SOL! (matches PORTUGAL's 'L' at row 8!)
# AR e SOL!

# Let's check Row 1 across (r1, c1..c6):
# (1, 1) = B (from BRASÍLIA)
# (1, 6) = P (from PORTUGAL)
# (1, 1) = B, (1, 2) = O, (1, 3) = M -> BOM! ("Agradável e positivo")
# (1, 4) = CLUE!
# (1, 5) = S, (1, 6) = P -> SP! ("Sigla do estado de São Paulo")

# Let's check Row 2 across (r2, c1..c6):
# (2, 1) = R (from BRASÍLIA)
# (2, 6) = O (from PORTUGAL)
# (2, 1) = R, (2, 2) = I, (2, 3) = O -> RIO! ("Curso de água doce")
# (2, 4) = CLUE!
# (2, 5) = D, (2, 6) = O -> DO! ("De + o")

# Let's check Row 3 across (r3, c1..c6):
# (3, 1) = A (from BRASÍLIA)
# (3, 6) = R (from PORTUGAL)
# (3, 1) = A, (3, 2) = S, (3, 3) = A -> ASA! ("Permite o voo do pássaro")
# (3, 4) = CLUE!
# (3, 5) = A, (3, 6) = R -> AR! ("Espaço aéreo")

# Let's check Row 4 across (r4, c1..c6):
# (4, 1) = S (from BRASÍLIA)
# (4, 6) = T (from PORTUGAL)
# (4, 1) = S, (4, 2) = U, (4, 3) = L -> SUL! ("Ponto cardeal frio")
# (4, 4) = CLUE!
# (4, 5) = O, (4, 6) = T -> OT?
# What if (4, 5) is 'U': U - T - I (UTI)?
# Or (4, 4) = CLUE pointing down into col 5:
# (4, 5) is CLUE pointing right to (4, 6) 'T'!
# "Letra após o S" -> T!

# Now let's check Row 6 across (r6, c1..c6):
# (6, 1) = L (from BRASÍLIA)
# (6, 6) = G (from PORTUGAL)
# (6, 1) = L, (6, 2) = U, (6, 3) = A -> LUA! ("Brilha na noite")
# (6, 4) = CLUE!
# (6, 5) = M, (6, 6) = G -> MG! ("Sigla de Minas Gerais")

# Now let's check Row 7 across (r7, c1..c6):
# (7, 1) = I (from BRASÍLIA)
# (7, 6) = A (from PORTUGAL)
# (7, 1) = I, (7, 2) = A -> IA! ("Inteligência Artificial")
# (7, 3) = CLUE!
# (7, 4) = D, (7, 5) = I, (7, 6) = A -> DIA! ("Período claro com sol")
# (7, 4)=D, (7, 5)=I, (7, 6)=A -> DIA! (matches PORTUGAL's 'A' at row 7!)

# Look at the down words in cols 2, 3, 4, 5:
# Col 2 (r1..r8):
# (1, 2) = O (from BOM)
# (2, 2) = I (from RIO)
# (3, 2) = S (from ASA)
# (4, 2) = U (from SUL)
# (5, 2) = CLUE!
# (6, 2) = U (from LUA)
# (7, 2) = A (from IA)
# (8, 2) = R (from AR)
# Look at (1..4, 2): O - I - S - U?
# If Row 1 has (1, 2) = U: B U M?
# Let's adjust so down words in cols 2, 3, 4, 5 are also 100% dictionary words!
print("Designing verified matrix...")
