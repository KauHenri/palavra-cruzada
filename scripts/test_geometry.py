import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
print("Loading words...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

words_by_len = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha(): continue
    l = len(clean)
    if 2 <= l <= 8:
        if l not in words_by_len: words_by_len[l] = set()
        words_by_len[l].add(clean)

# Load common words
common_words_set = set()
with open("scripts/common_words.txt", "r", encoding="utf-8", errors="ignore") as f:
    for l in f:
        c = strip_accents(l.strip())
        if c.isalpha() and len(c) >= 2:
            common_words_set.add(c)

# Add rich common vocabulary
extra = [
    # 2 letters
    "AR", "PA", "PE", "PO", "LA", "LE", "NO", "OU", "SE", "DO", "RE", "MI", "FA", "SI", "TI",
    "EU", "AI", "OI", "IR", "VI", "JA", "HA", "SO", "UM", "AS", "OS", "EM", "NA", "DA", "DE",
    # 3 letters
    "SOL", "LUA", "MAR", "RIO", "RUA", "CEU", "MEL", "PAO", "PAZ", "LUZ", "COR", "SOM", "REI",
    "MAO", "FIM", "ANO", "ATO", "ELO", "ERA", "SAL", "ASA", "UVA", "OVO", "ACO", "BOA", "RIR",
    "VER", "DAR", "SER", "VOZ", "BEM", "SIM", "CHA", "DIA", "DOM", "LEI", "PIA", "GEL", "GAS",
    "LAR", "FIO", "OLA", "MAS", "ATE", "POR", "SEM", "SOB", "TAL", "MAL", "MAU", "VEM", "VAI",
    # 4 letters
    "AMOR", "VIDA", "CASA", "FLOR", "DOCE", "AZUL", "ROSA", "FOGO", "AGUA", "NOVO", "BOCA", "OLHO",
    "GATO", "LOBO", "LEAO", "CAFE", "BOLO", "MESA", "SOPA", "FRIO", "ALTO", "BELA", "OURO", "NOTA",
    "NOME", "ALVO", "RISO", "ARTE", "POVO", "NAVE", "COPO", "ROTA", "SELO", "VOTO", "DADO", "PENA",
    "BOLA", "REDE", "VILA", "ILHA", "FARO", "PISO", "VARA", "TELA", "CENA", "FAMA", "MALA", "SACO",
    "RICO", "SUCO", "BICO", "ISCA", "SOFA", "ROLO", "POTE", "LAGO", "MAPA", "TREM", "AUTO", "PURA",
    "RARA", "DOR", "MEDO", "MAIS", "TUDO", "NADA", "CADA", "HORA", "FASE", "JOGO", "TEMO",
    # 5 letters
    "BEIJO", "LIVRO", "PRAIA", "HOTEL", "MUNDO", "TEMPO", "FORCA", "NOITE", "SONHO", "FESTA", "SORTE",
    "PLANO", "VENTO", "CALOR", "PIZZA", "FRUTA", "NAVIO", "CREPE", "PERU", "CAMPO", "PORTA", "PRATO",
    "ARROZ", "CARRO", "BANHO", "CANTO", "CARTA", "VERDE", "LINDO", "AMIGO", "CHAVE", "BARCO", "AREIA",
    "RADIO", "FAROL", "COSTA", "TRENO", "NORTE", "LESTE", "OESTE", "BAHIA", "MINAS", "GOIAS", "CEARA",
    "TERRA", "FOLHA", "PEIXE", "CORPO", "MENTE", "FORMA", "GRUPO", "PASSO", "VALOR", "CLIMA", "DUNAS",
    # 6 letters
    "BRASIL", "VIAGEM", "CIDADE", "PARQUE", "VERAO", "MUSICA", "CHEIRO", "CINEMA", "PIPOCA", "JANTAR",
    "ABRACO", "ALEGRE", "ADEPTO", "COLADA", "AMAVEL", "BONITO", "SEGURO", "ESPACO", "CANTOR", "VIOLAO",
    "TEATRO", "MUSEUS", "FLORES", "FRUTAS", "NUVENS", "VENTOS", "CAMINH", "PLANTA", "PRAIAS", "PRATOS",
    # 7-8 letters
    "PORTUGAL", "BRASILIA", "OLIVEIRA", "ESTRELA", "CORACAO", "NATUREZA", "FAMILIA", "PALACIO", "CARIOCA",
    "PAULISTA", "ADORAVEL", "AMOROSOS", "CAMINHO", "PASSEIO", "ROTEIRO", "DESTINO", "TURISMO"
]
for w in extra:
    common_words_set.add(strip_accents(w))

print(f"Total curated common words: {len(common_words_set)}")

# Quebra-cabeça 18 geometry:
# 9 rows x 7 cols
# Letter cells:
# Row 1: (1, 1..6) len 6
# Row 2: (2, 1) len 1, (2, 2)=CLUE, (2, 3..6) len 4
# Row 3: (3, 1..2) len 2, (3, 3)=CLUE, (3, 4..6) len 3
# Row 4: (4, 1..3) len 3, (4, 4)=CLUE, (4, 5..6) len 2
# Row 5: (5, 1..6) len 6
# Row 6: (6, 1..4) len 4, (6, 5)=CLUE, (6, 6) len 1
# Row 7: (7, 1..3) len 3, (7, 4)=CLUE, (7, 5..6) len 2
# Row 8: (8, 1..2) len 2, (8, 3)=CLUE, (8, 4..6) len 3

# Notice that row 2 col 1 was 1 letter (D) and row 6 col 6 was 1 letter (I).
# What if we eliminate those 1-letter cells?
# If (2, 1) is a CLUE cell! Then row 2 has no 1-letter cell.
# Or even better: what if:
# Row 2: (2, 1..2) len 2, (2, 3)=CLUE, (2, 4..6) len 3!
# Then row 2 has TWO words: length 2 and length 3! No 1-letter words!
# And Row 6: (6, 1..3) len 3, (6, 4)=CLUE, (6, 5..6) len 2!
# Then row 6 has TWO words: length 3 and length 2! No 1-letter words!

print("Testing revised flawless 9x7 geometry without 1-letter words...")
