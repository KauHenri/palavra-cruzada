import unicodedata
import random
import time
from strict_verifier import test_level_design

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
print("Loading words...")
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    raw = [l.strip() for l in f if l.strip()]

words_by_len = {}
raw_by_clean = {}
for w in raw:
    clean = strip_accents(w)
    if not clean.isalpha(): continue
    l = len(clean)
    if 2 <= l <= 8:
        if l not in words_by_len: words_by_len[l] = set()
        words_by_len[l].add(clean)
        if clean not in raw_by_clean:
            raw_by_clean[clean] = w

# Load common words
common_set = set()
with open("scripts/common_words.txt", "r", encoding="utf-8", errors="ignore") as f:
    for l in f:
        c = strip_accents(l.strip())
        if c.isalpha() and len(c) >= 2:
            common_set.add(c)

# Curated familiar words
familiar_words = [
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
    # 5 letters
    "BEIJO", "LIVRO", "PRAIA", "HOTEL", "MUNDO", "TEMPO", "FORCA", "NOITE", "SONHO", "FESTA", "SORTE",
    "PLANO", "VENTO", "CALOR", "PIZZA", "FRUTA", "NAVIO", "CREPE", "PERU", "CAMPO", "PORTA", "PRATO",
    "ARROZ", "CARRO", "BANHO", "CANTO", "CARTA", "VERDE", "LINDO", "AMIGO", "CHAVE", "BARCO", "AREIA",
    "RADIO", "FAROL", "COSTA", "TRENO", "NORTE", "LESTE", "OESTE", "BAHIA", "MINAS", "GOIAS", "CEARA",
    # 6 letters
    "BRASIL", "VIAGEM", "CIDADE", "PARQUE", "VERAO", "MUSICA", "CHEIRO", "CINEMA", "PIPOCA", "JANTAR",
    "ABRACO", "ALEGRE", "ADEPTO", "COLADA", "AMAVEL", "BONITO", "SEGURO", "ESPACO", "CANTOR", "VIOLAO",
    "TEATRO", "MUSEUS", "FLORES", "FRUTAS", "NUVENS", "VENTOS", "CAMINH", "PLANTA", "PRAIAS", "PRATOS",
    # 7 letters
    "PORTUGAL", "BRASILIA", "OLIVEIRA", "ESTRELA", "CORACAO", "NATUREZA", "FAMILIA", "PALACIO", "CARIOCA",
    "PAULISTA", "ADORAVEL", "AMOROSOS", "PASSEIO", "ROTEIRO", "DESTINO", "TURISMO"
]
for w in familiar_words:
    common_set.add(strip_accents(w))

# Build slots for 8x7 with clues at (3, 3) and (4, 4)
rows, cols = 8, 7
slots = [
    # Across
    {"id": "A1", "dir": "right", "row": 1, "col": 1, "len": 6, "coords": [(1, c) for c in range(1, 7)]},
    {"id": "A2", "dir": "right", "row": 2, "col": 1, "len": 6, "coords": [(2, c) for c in range(1, 7)]},
    {"id": "A3", "dir": "right", "row": 3, "col": 1, "len": 2, "coords": [(3, 1), (3, 2)]},
    {"id": "A4", "dir": "right", "row": 3, "col": 4, "len": 3, "coords": [(3, 4), (3, 5), (3, 6)]},
    {"id": "A5", "dir": "right", "row": 4, "col": 1, "len": 3, "coords": [(4, 1), (4, 2), (4, 3)]},
    {"id": "A6", "dir": "right", "row": 4, "col": 5, "len": 2, "coords": [(4, 5), (4, 6)]},
    {"id": "A7", "dir": "right", "row": 5, "col": 1, "len": 6, "coords": [(5, c) for c in range(1, 7)]},
    {"id": "A8", "dir": "right", "row": 6, "col": 1, "len": 6, "coords": [(6, c) for c in range(1, 7)]},
    {"id": "A9", "dir": "right", "row": 7, "col": 1, "len": 6, "coords": [(7, c) for c in range(1, 7)]},

    # Down
    {"id": "D1", "dir": "down", "row": 1, "col": 1, "len": 7, "coords": [(r, 1) for r in range(1, 8)]},
    {"id": "D2", "dir": "down", "row": 1, "col": 2, "len": 7, "coords": [(r, 2) for r in range(1, 8)]},
    {"id": "D3", "dir": "down", "row": 1, "col": 3, "len": 2, "coords": [(1, 3), (2, 3)]},
    {"id": "D4", "dir": "down", "row": 4, "col": 3, "len": 4, "coords": [(r, 3) for r in range(4, 8)]},
    {"id": "D5", "dir": "down", "row": 1, "col": 4, "len": 3, "coords": [(r, 4) for r in range(1, 4)]},
    {"id": "D6", "dir": "down", "row": 5, "col": 4, "len": 3, "coords": [(r, 4) for r in range(5, 8)]},
    {"id": "D7", "dir": "down", "row": 1, "col": 5, "len": 7, "coords": [(r, 5) for r in range(1, 8)]},
    {"id": "D8", "dir": "down", "row": 1, "col": 6, "len": 7, "coords": [(r, 6) for r in range(1, 8)]},
]

print(f"Mask has {len(slots)} slots. Starting search for Level 1...")

def search_solutions(theme_anchor=None, max_tries=5):
    # Setup candidate lists
    cand_lists = []
    for s in slots:
        l = s["len"]
        w_list = list(words_by_len.get(l, []))
        # Sort common first
        w_list.sort(key=lambda w: (w in common_set, random.random()), reverse=True)
        cand_lists.append(w_list)

    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()

    # If anchor given, e.g. A1="BRASIL" or similar
    if theme_anchor:
        slot_idx, word = theme_anchor
        assigned[slot_idx] = word
        used.add(word)
        for i, (r, c) in enumerate(slots[slot_idx]["coords"]):
            grid[r][c] = word[i]

    def solve(depth=0):
        # MRV
        best_idx = None
        best_words = None

        for idx, s in enumerate(slots):
            if assigned[idx] is not None: continue
            pattern = [grid[r][c] for r, c in s["coords"]]
            matching = []
            for w in cand_lists[idx]:
                if w in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != w[i]:
                        match = False
                        break
                if match:
                    matching.append(w)
                    if len(matching) > 40: break

            if len(matching) == 0:
                return None

            if best_words is None or len(matching) < len(best_words):
                best_words = matching
                best_idx = idx
                if len(best_words) <= 1: break

        if best_idx is None:
            return [row[:] for row in grid], assigned[:]

        s = slots[best_idx]
        coords = s["coords"]

        # Try top candidates (prefer common)
        for w in best_words[:15]:
            old = [grid[r][c] for r, c in coords]
            for i, (r, c) in enumerate(coords): grid[r][c] = w[i]
            assigned[best_idx] = w
            used.add(w)

            res = solve(depth + 1)
            if res: return res

            for i, (r, c) in enumerate(coords): grid[r][c] = old[i]
            assigned[best_idx] = None
            used.remove(w)

        return None

    return solve()

# Let's try anchoring A1 with a theme word
for anchor in ["BRASIL", "VIAGEM", "PRAIAS", "CIDADE", None]:
    print(f"Trying anchor: {anchor}...")
    anchor_tuple = (0, anchor) if anchor else None
    res = search_solutions(anchor_tuple)
    if res:
        sol_grid, sol_assigned = res
        print("FOUND SOLUTION!")
        for r in range(1, rows):
            line = []
            for c in range(1, cols):
                if (r, c) in [(3, 3), (4, 4)]:
                    line.append("[]")
                else:
                    line.append(sol_grid[r][c])
            print(f"  Row {r}: {' '.join(line)}")

        common_c = sum(1 for w in sol_assigned if w in common_set)
        print(f"  Common words: {common_c}/{len(sol_assigned)}")
        for i, s in enumerate(slots):
            is_comm = "[C]" if sol_assigned[i] in common_set else "[ ]"
            print(f"    {is_comm} {s['id']} ({s['dir']}): {sol_assigned[i]}")
        break
