import json
import unicodedata
import random
from strict_verifier import test_level_design

# Load common words
def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Let's inspect a handcrafted candidate for Level 1 (Viagens & Natureza)
# Grid 9 rows x 7 cols (standard Coquetel layout)
# Row 0: EMPTY, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE
# Col 0: CLUE, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE, CLUE

# Let's test a clean, proven layout where every word is a popular, beloved Portuguese word!
# Let's see:
# Words like:
# BRASIL (6), PRAIA (5), HOTEL (5), NAVIO (5), NORTE (5), LESTE (5), OESTE (5),
# BAHIA (5), MINAS (5), GOIAS (5), AMAPÁ (5), CEARA (5), RIO (3), SOL (3), MAR (3),
# LUA (3), CEU (3), AR (2), PAZ (3), ILHA (4), ROTA (4), MAPA (4), TREM (4),
# AUTO (4), VILA (4), FAROL (5), DUNAS (5), CLIMA (5), PORTO (5), VIAGEM (6)

# Let's write a solver that takes an anchor theme and fills the grid
