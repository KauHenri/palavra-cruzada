import unicodedata
import random
import time

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Load words
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
common_set = set()
with open("scripts/common_words.txt", "r", encoding="utf-8", errors="ignore") as f:
    for l in f:
        c = strip_accents(l.strip())
        if c.isalpha(): common_set.add(c)

# Let's add extra familiar words
extra_familiar = [
    "BRASIL", "VIAGEM", "PRAIAS", "CIDADE", "HOTEL", "NAVIO", "BARCO", "NORTE", "LESTE", "OESTE",
    "PASSEIO", "ROTEIRO", "DESTINO", "TURISMO", "CAPITAL", "BAHIA", "MINAS", "RIO", "SOL", "MAR",
    "LUA", "CEU", "AR", "PAZ", "LUZ", "SOM", "DIA", "FIM", "VER", "DAR", "SER", "BEM", "SIM",
    "AMOR", "VIDA", "CASA", "FLOR", "DOCE", "AZUL", "ROSA", "FOGO", "AGUA", "NOVO", "MESA", "BOLO",
    "ALTO", "BELA", "OURO", "ARTE", "COPO", "ROTA", "SELO", "BOLA", "REDE", "VILA", "ILHA",
    "BEIJO", "LIVRO", "PRAIA", "MUNDO", "TEMPO", "FORCA", "NOITE", "SONHO", "FESTA", "SORTE",
    "VENTO", "CALOR", "PIZZA", "FRUTA", "CAMPO", "PORTA", "PRATO", "ARROZ", "CARRO", "BANHO",
    "VERDE", "LINDO", "AMIGO", "CHAVE", "AREIA", "RADIO", "FAROL", "CINEMA", "PIPOCA", "JANTAR",
    "ESTRELA", "CORACAO", "CULTURA", "NATUREZA", "FAMILIA", "CANCION", "MERCADO", "PALACIO",
    "AMOROSO", "SERENOS", "BONITAS", "SEMANAS", "AVENIDA", "CASTELO", "MORENAS", "AMAVIES",
    "AMAVEL", "BONITO", "ALEGRE", "SEGURO", "ESPACO", "CANTOR", "VIOLAO", "TEATRO", "MUSEUS"
]
for w in extra_familiar:
    common_set.add(strip_accents(w))

print(f"Common vocabulary: {len(common_set)} words")

# Mask 8x7 with clues at (3,3) and (5,4)
rows, cols = 8, 7
slots = [
    {"id": "A1", "dir": "right", "row": 1, "col": 1, "len": 6, "coords": [(1, c) for c in range(1, 7)]},
    {"id": "A2", "dir": "right", "row": 2, "col": 1, "len": 6, "coords": [(2, c) for c in range(1, 7)]},
    {"id": "A3", "dir": "right", "row": 3, "col": 1, "len": 2, "coords": [(3, 1), (3, 2)]},
    {"id": "A4", "dir": "right", "row": 3, "col": 4, "len": 3, "coords": [(3, 4), (3, 5), (3, 6)]},
    {"id": "A5", "dir": "right", "row": 4, "col": 1, "len": 6, "coords": [(4, c) for c in range(1, 7)]},
    {"id": "A6", "dir": "right", "row": 5, "col": 1, "len": 3, "coords": [(5, 1), (5, 2), (5, 3)]},
    {"id": "A7", "dir": "right", "row": 5, "col": 5, "len": 2, "coords": [(5, 5), (5, 6)]},
    {"id": "A8", "dir": "right", "row": 6, "col": 1, "len": 6, "coords": [(6, c) for c in range(1, 7)]},
    {"id": "A9", "dir": "right", "row": 7, "col": 1, "len": 6, "coords": [(7, c) for c in range(1, 7)]},

    {"id": "D1", "dir": "down", "row": 1, "col": 1, "len": 7, "coords": [(r, 1) for r in range(1, 8)]},
    {"id": "D2", "dir": "down", "row": 1, "col": 2, "len": 7, "coords": [(r, 2) for r in range(1, 8)]},
    {"id": "D3", "dir": "down", "row": 1, "col": 3, "len": 2, "coords": [(1, 3), (2, 3)]},
    {"id": "D4", "dir": "down", "row": 4, "col": 3, "len": 4, "coords": [(r, 3) for r in range(4, 8)]},
    {"id": "D5", "dir": "down", "row": 1, "col": 4, "len": 4, "coords": [(r, 4) for r in range(1, 5)]},
    {"id": "D6", "dir": "down", "row": 6, "col": 4, "len": 2, "coords": [(6, 4), (7, 4)]},
    {"id": "D7", "dir": "down", "row": 1, "col": 5, "len": 7, "coords": [(r, 5) for r in range(1, 8)]},
    {"id": "D8", "dir": "down", "row": 1, "col": 6, "len": 7, "coords": [(r, 6) for r in range(1, 8)]},
]

# Sort words for each slot by commonality first
slot_word_lists = []
for s in slots:
    l = s["len"]
    cands = list(words_by_len.get(l, []))
    # prioritize common words
    cands.sort(key=lambda w: (w in common_set, random.random()), reverse=True)
    slot_word_lists.append(cands)

def solve(max_seconds=20):
    grid = [['' for _ in range(cols)] for _ in range(rows)]
    assigned = [None] * len(slots)
    used = set()
    start_t = time.time()

    def backtrack():
        if time.time() - start_t > max_seconds: return None

        # Pick slot with MRV
        best_idx = None
        best_words = None

        for idx, s in enumerate(slots):
            if assigned[idx] is not None: continue
            pattern = [grid[r][c] for r, c in s["coords"]]
            matching = []
            for w in slot_word_lists[idx]:
                if w in used: continue
                match = True
                for i, ch in enumerate(pattern):
                    if ch != '' and ch != w[i]:
                        match = False
                        break
                if match:
                    matching.append(w)
                    if len(matching) > 100: break

            if len(matching) == 0:
                return None

            if best_words is None or len(matching) < len(best_words):
                best_words = matching
                best_idx = idx
                if len(best_words) <= 1: break

        if best_idx is None:
            return grid

        s = slots[best_idx]
        coords = s["coords"]

        for w in best_words[:25]:
            old = [grid[r][c] for r, c in coords]
            for i, (r, c) in enumerate(coords): grid[r][c] = w[i]
            assigned[best_idx] = w
            used.add(w)

            res = backtrack()
            if res: return res

            for i, (r, c) in enumerate(coords): grid[r][c] = old[i]
            assigned[best_idx] = None
            used.remove(w)

        return None

    res = backtrack()
    return res, assigned

print("Searching for high-quality solution...")
res, assigned = solve(25)
if res:
    print("Found solution!")
    for r in range(1, rows):
        row_str = " ".join(res[r][c] if (r, c) not in [(3, 3), (5, 4)] else "[]" for c in range(1, cols))
        print(f"Row {r}: {row_str}")
    common_count = sum(1 for w in assigned if w in common_set)
    print(f"Common words count: {common_count}/{len(assigned)}")
    for idx, s in enumerate(slots):
        is_comm = "★" if assigned[idx] in common_set else " "
        print(f" {is_comm} {s['id']} ({s['dir']} {s['row']},{s['col']}): {assigned[idx]}")
else:
    print("No solution found in time limit.")
