# Backtracking solver to find 100% real Swedish crossword grids
import unicodedata

def clean(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn').upper()

# Real words dictionary
DICT = set([clean(w) for w in [
    # 8
    "BRASILIA", "PORTUGAL", "SALVADOR", "CURITIBA", "CAMPINAS", "ADORAVEL", "OLIVEIRA",
    # 7
    "AMIGAVEL", "ALEGRES", "CAMPEAO", "RECEITA", "SABORES", "CINEMAS", "ESTRELA", "PASSEIO",
    # 6
    "BRASIL", "ADEPTO", "ALEGRE", "CINEMA", "CIDADE", "EXIBIR", "SORRIA", "FESTAS", "AMIGOS",
    "TELONA", "SALGAR", "JANTAR", "FLORES", "MUITOS", "CAMINH", "PORTOS", "PRATOS", "CARROS",
    # 5
    "AMADO", "AMADA", "PLANO", "NORTE", "VERAO", "CALOR", "FESTA", "NOITE", "LIVRO", "FILME",
    "OSCAR", "PAPEL", "DRAMA", "CANTO", "PORTO", "NAVIO", "FAROL", "VENTO", "MUNDO", "MAPAS",
    "DOCES", "SABOR", "PUDIM", "ARROZ", "PEIXE", "MOLHO", "TORTA", "FRUTA", "MASSA", "PIZZA",
    "CREPE", "CHAVE", "COCAR", "TOPAR", "PERU", "VARA", "PRAIA", "HOTEL", "CAMPO", "TERRA",
    # 4
    "AMOR", "CASA", "VIDA", "BOLO", "DOCE", "SOPA", "MESA", "FOGO", "AGUA", "ALHO", "CENA",
    "FITA", "TELA", "ATOR", "OURO", "RISO", "FOTO", "ROTA", "MAPA", "MALA", "GUIA", "TREM",
    "AUTO", "PROL", "PERU", "VARA", "POTE", "GATO", "LOBO", "LEAO", "BOCA", "OLHO", "MAOS",
    "NOVO", "ALVO", "POVO", "NAVE", "COPO", "SELO", "VOTO", "DADO", "PENA", "BOLA", "REDE",
    # 3
    "SOL", "LUA", "MAR", "RIO", "RUA", "PAZ", "LUZ", "MEL", "CHA", "UVA", "OVO", "PAO",
    "CEU", "SOM", "DIA", "ATO", "COR", "VER", "DAR", "BOM", "SIM", "REI", "MAO", "FIM",
    "ANO", "ELO", "ERA", "SAL", "ASA", "ACO", "BOA", "RIR", "VOZ", "BEM", "OLA", "PRO",
    "EDU", "ROP", "OPI", "VOU", "SAI", "LEI", "PAI", "MAE", "TIO", "TIA", "AVO",
    # 2
    "LA", "AR", "AU", "GA", "DF", "SC", "SP", "RJ", "MG", "PR", "BA", "RS", "ES", "GO",
    "EM", "EU", "TU", "SE", "IR", "OI", "DO", "DA", "NO", "NA", "DE", "UM", "JA", "HA",
    "OC", "EP", "AV", "IA", "OU", "AI", "AS", "OS", "ME", "TE", "LE"
]])

print(f"Total dictionary entries: {len(DICT)}")
