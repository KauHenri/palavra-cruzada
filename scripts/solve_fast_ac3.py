import unicodedata
from collections import defaultdict
import random
import time
import json

def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn').upper()

# Curated 2-letter words (ONLY unmistakably familiar, everyday words)
clean_2 = {
    "AR": "RESPIRAÇÃO",
    "IR": "PARTIR",
    "PO": "POEIRA",
    "PE": "MEMBRO INFERIOR",
    "PA": "FERRAMENTA",
    "FE": "CRENÇA",
    "LA": "AQUELE LUGAR",
    "NO": "AMARRAÇÃO",
    "DO": "NOTA MUSICAL",
    "RE": "MARCHA DO CARRO",
    "FA": "NOTA MUSICAL",
    "LE": "LÊ LIVROS",
    "OI": "SAUDAÇÃO",
    "EU": "PRIMEIRA PESSOA",
    "TU": "SEGUNDA PESSOA",
    "UM": "PRIMEIRO NÚMERO",
    "JA": "AGORA MESMO",
    "HA": "VERBO HAVER",
    "SO": "SEM NINGUÉM",
    "AI": "GRITO DE DOR",
    "VA": "SIGA EM FRENTE",
    "VE": "ENXERGA",
    "CA": "AQUI MESMO",
    "TI": "A VOCÊ",
    "AO": "RUMO AO",
    "DA": "DE ELA",
    "NA": "EM ELA",
    "EM": "DENTRO DE",
    "OU": "ALTERNATIVA",
    "SE": "CONDIÇÃO",
    "AS": "ARTIGO PLURAL",
    "OS": "ARTIGO PLURAL",
}

# Curated 3-letter words
clean_3 = {
    "SOL": "ASTRO REI",
    "LUA": "ASTRO DA NOITE",
    "MAR": "ÁGUA SALGADA",
    "RIO": "CURSO DE ÁGUA",
    "RUA": "VIA PÚBLICA",
    "CEU": "ONDE VOAM AVES",
    "MEL": "DOCE DAS ABELHAS",
    "PAO": "ALIMENTO BÁSICO",
    "PAZ": "SEM GUERRA",
    "LUZ": "CLAREIA TUDO",
    "COR": "AZUL OU VERMELHO",
    "SOM": "O QUE SE OUVE",
    "REI": "COROA E TRONO",
    "MAO": "CINCO DEDOS",
    "FIM": "TÉRMINO",
    "ANO": "DOZE MESES",
    "ATO": "GESTO OU AÇÃO",
    "ELO": "ANEL DE CORRENTE",
    "ERA": "ÉPOCA HISTÓRICA",
    "SAL": "TEMPERO BRANCO",
    "ASA": "MEMBRO DE AVE",
    "UVA": "FRUTA DO VINHO",
    "OVO": "VEM DA GALINHA",
    "ACO": "METAL FORTE",
    "BOA": "GENTIL E CALMA",
    "RIR": "DAR GARGALHADA",
    "VER": "ENXERGAR",
    "DAR": "OFERECER",
    "SER": "EXISTIR",
    "VOZ": "SOM DA BOCA",
    "BEM": "OPOSTO DE MAL",
    "CHA": "BEBIDA QUENTE",
    "DIA": "HORA DO SOL",
    "DOM": "TALENTO NATO",
    "LEI": "REGRA DO PAÍS",
    "PIA": "ONDE LAVA LOUÇA",
    "GEL": "FIXA O CABELO",
    "GAS": "USA NO FOGÃO",
    "LAR": "NOSSA CASA",
    "FIO": "CABO DE ENERGIA",
    "OLA": "OI AMIGÁVEL",
    "CAO": "MELHOR AMIGO",
    "BAU": "GUARDA TESOURO",
    "GOL": "FESTA NO ESTÁDIO",
    "BOI": "ANIMAL DO PASTO",
    "PAI": "FIGURA PATERNA",
    "MAE": "FIGURA MATERNA",
    "TIO": "IRMÃO DO PAI",
    "TIA": "IRMÃ DA MÃE",
    "BOM": "OPOSTO DE RUIM",
    "SIM": "RESPOSTA POSITIVA",
    "NAO": "RESPOSTA NEGATIVA",
    "VOU": "IREI EMBORA",
    "SOU": "EU EXISTO",
    "ELE": "AQUELE RAPAZ",
    "ELA": "AQUELA MULHER",
    "NEM": "TAMPOUCO",
    "FAZ": "REALIZA",
    "FEZ": "CONCLUIU",
    "VIU": "ENXERGOU",
    "DIZ": "FALA EM VOZ ALTA",
    "FUI": "JÁ ESTIVE LÁ",
    "FIZ": "JÁ TERMINEI",
    "TEM": "POSSUI",
    "SAO": "COM SAÚDE",
    "VAI": "SE DESLOCA",
    "VEM": "CHEGA PERTO",
    "UMA": "ARTIGO FEMININO",
    "DEZ": "DEPOIS DO NOVE",
    "DOR": "INCÔMODO FÍSICO",
    "RIM": "ÓRGÃO DO CORPO",
    "TOM": "TIMBRE DA VOZ",
    "TEU": "PERTENCE A TI",
    "MEU": "PERTENCE A MIM",
    "SEU": "PERTENCE A ELE",
    "AVE": "BICHO DE PENAS",
    "BAR": "LOCAL DE BEBIDAS",
    "VIL": "CRUEL E MAU",
    "VEZ": "MOMENTO OU TURNO",
    "VIA": "CAMINHO OU ROTA",
    "CAL": "PÓ PARA PINTURA",
    "ECO": "SOM REPETIDO",
}

# Blacklist of English, obscure, archaic, offensive words
blacklist = {
    "ART", "ALIENS", "VINTAGE", "HALL", "STAN", "CHET", "DICK", "FUCK", "SHIT",
    "SA", "ADA", "ACE", "ST", "EST", "BELMAZ", "ZORAIA", "LOROSA", "ARATUS", "ICAPUI",
    "ASIM", "NAOS", "VECTOR", "TOTO", "ARGO", "RAMONA", "OTAN", "JIRO", "ANAS", "MAMILO",
    "SOIOTO", "ERGUER", "MADRIA", "AMICAL", "MATESE", "ARARAI", "IGDLOITA", "OURESCER",
    "ALOMORFO", "ESTEREIS", "DALE", "LIONEL", "DUMA", "ME", "ARI", "DORIAN", "MADI",
    "LEAR", "ELAINE", "NAPIER", "IVES", "LAOS", "ELISSA", "MARISA", "MARIACHI", "SECTOR",
    "OLOFRO", "MEBOSA", "AMAL", "TAMA", "CAMADA", "AMADAS", "MICADO", "ROBE", "UNOS",
    "ARSENICO", "ZELOSO", "LOIROS", "LOIRAS", "NERO", "ERIC", "DAMIEN", "ALAN", "CHAD",
    "HOME", "SECTOR", "BURRO", "CORNO", "PUTA", "VIADO", "GAY"
}

# Load dictionary
pt_dict = set()
pt_display = {}
with open("scripts/palavras_full.txt", "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
        raw = line.strip()
        w = strip_accents(raw)
        if w.isalpha():
            pt_dict.add(w)
            if w not in pt_display:
                pt_display[w] = raw.upper()

# Load top 50k
w50 = set()
with open("scripts/pt_br_50k.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if parts:
            w = strip_accents(parts[0])
            if w.isalpha():
                w50.add(w)

# Filter 6-letter words: top 50k, in pt_dict, not blacklisted
# Also verify freq in top_common_clean >= 100
freq = defaultdict(int)
proper = set()
with open("scripts/top_common_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            w = strip_accents(parts[0])
            if parts[1][0].isupper():
                proper.add(w)
            if len(parts) >= 3:
                try: freq[w] = max(freq[w], int(parts[2]))
                except: pass

clean_6 = []
for w in (w50 & pt_dict) - proper - blacklist:
    if len(w) == 6 and freq[w] >= 150:
        clean_6.append(w)

print(f"Curated clean words: 2-letters: {len(clean_2)}, 3-letters: {len(clean_3)}, 6-letters: {len(clean_6)}")

words_by_len = {
    2: list(clean_2.keys()),
    3: list(clean_3.keys()),
    6: clean_6
}

# Build index for fast lookup
index = defaultdict(set)
for l in words_by_len:
    for w in words_by_len[l]:
        for pos, ch in enumerate(w):
            index[(l, pos, ch)].add(w)

# Define 7x7 standard Direct Crossword slots
slots = [
    {'id': 'R1', 'dir': 'A', 'cells': [(1, c) for c in range(1, 7)]},
    {'id': 'R2', 'dir': 'A', 'cells': [(2, c) for c in range(1, 7)]},
    {'id': 'A3_1', 'dir': 'A', 'cells': [(3, 1), (3, 2)]},
    {'id': 'A3_2', 'dir': 'A', 'cells': [(3, 4), (3, 5), (3, 6)]},
    {'id': 'A4_1', 'dir': 'A', 'cells': [(4, 1), (4, 2), (4, 3)]},
    {'id': 'A4_2', 'dir': 'A', 'cells': [(4, 5), (4, 6)]},
    {'id': 'R5', 'dir': 'A', 'cells': [(5, c) for c in range(1, 7)]},
    {'id': 'R6', 'dir': 'A', 'cells': [(6, c) for c in range(1, 7)]},

    {'id': 'C1', 'dir': 'D', 'cells': [(r, 1) for r in range(1, 7)]},
    {'id': 'C2', 'dir': 'D', 'cells': [(r, 2) for r in range(1, 7)]},
    {'id': 'D3_1', 'dir': 'D', 'cells': [(1, 3), (2, 3)]},
    {'id': 'D3_2', 'dir': 'D', 'cells': [(4, 3), (5, 3), (6, 3)]},
    {'id': 'D4_1', 'dir': 'D', 'cells': [(1, 4), (2, 4), (3, 4)]},
    {'id': 'D4_2', 'dir': 'D', 'cells': [(5, 4), (6, 4)]},
    {'id': 'C5', 'dir': 'D', 'cells': [(r, 5) for r in range(1, 7)]},
    {'id': 'C6', 'dir': 'D', 'cells': [(r, 6) for r in range(1, 7)]},
]

# Map intersections
intersections = defaultdict(list)
for i, s1 in enumerate(slots):
    for j, s2 in enumerate(slots):
        if i >= j: continue
        common = set(s1['cells']) & set(s2['cells'])
        for cell in common:
            p1 = s1['cells'].index(cell)
            p2 = s2['cells'].index(cell)
            intersections[i].append((j, p1, p2))
            intersections[j].append((i, p2, p1))

def solve_grid(used_words=set(), max_solutions=1):
    solutions = []
    
    # We will search with domain propagation
    # Initial domains:
    domains = [set(words_by_len[len(slot['cells'])]) - used_words for slot in slots]
    
    # AC-3 initial filtering
    # Each entry in queue is (i, j, p_i, p_j): checking if domain of i has support in j
    queue = [(i, j, p_i, p_j) for i in range(len(slots)) for (j, p_i, p_j) in intersections[i]]
    while queue:
        i, j, p_i, p_j = queue.pop(0)
        chars_j = {w[p_j] for w in domains[j]}
        to_remove = {w for w in domains[i] if w[p_i] not in chars_j}
        if to_remove:
            domains[i] -= to_remove
            if not domains[i]:
                return []
            for (k, p_i_k, p_k) in intersections[i]:
                if k != j:
                    # We need to re-check k against i
                    queue.append((k, i, p_k, p_i_k))

    print("Domain sizes after initial AC-3:")
    for idx, d in enumerate(domains):
        print(f"  {slots[idx]['id']} ({len(slots[idx]['cells'])}): {len(d)}")

    def backtrack(domains, assigned, local_used):
        if len(solutions) >= max_solutions:
            return
        if all(a is not None for a in assigned):
            solutions.append({slots[i]['id']: assigned[i] for i in range(len(slots))})
            return

        # Pick slot with MRV
        unassigned = [i for i in range(len(slots)) if assigned[i] is None]
        unassigned.sort(key=lambda i: len(domains[i]))
        best_i = unassigned[0]
        
        cands = list(domains[best_i] - local_used)
        random.shuffle(cands)
        
        for w in cands:
            # Propagate choice
            new_domains = [set(d) for d in domains]
            new_domains[best_i] = {w}
            new_assigned = list(assigned)
            new_assigned[best_i] = w
            new_used = local_used | {w}
            
            # Check constraints on neighbors
            possible = True
            for (j, pi, pj) in intersections[best_i]:
                if new_assigned[j] is None:
                    ch = w[pi]
                    new_domains[j] = {wj for wj in new_domains[j] if wj[pj] == ch and wj not in new_used}
                    if not new_domains[j]:
                        possible = False
                        break
            if possible:
                backtrack(new_domains, new_assigned, new_used)

    backtrack(domains, [None]*len(slots), set())
    return solutions

print("Testing AC-3 solver...")
t0 = time.time()
sols = solve_grid(max_solutions=5)
print(f"Solved in {time.time() - t0:.2f}s! Found {len(sols)} solutions.")
for idx, sol in enumerate(sols):
    print(f"--- Solution {idx+1} ---")
    for k, v in sol.items():
        print(f"  {k}: {v} ({pt_display.get(v, v)})")
