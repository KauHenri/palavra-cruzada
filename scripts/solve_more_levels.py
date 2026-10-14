# Search script to find complete, valid 8x7 and 9x7 Swedish Crosswords
import json

# Word lists for culinary and cinema
WORDS_VALID = [
    # 6 letters
    "SALGAR", "ALEGRE", "BRASIL", "CINEMA", "AMORES", "ROCHAS", "FLORES", "JANTAR",
    "PRATOS", "CARNES", "SOPAS", "MOLHOS", "TORTAS", "FRUTAS", "QUEIJO", "CREMES",
    "CIDADE", "EXIBIR", "SORRIA", "FESTAS", "AMIGOS", "TELONA", "CENAS", "ARTES",
    # 5 letters
    "DOCES", "SABOR", "PUDIM", "ARROZ", "FEIJA", "PEIXE", "MOLHO", "TORTA", "FRUTA",
    "MASSA", "PIZZA", "CREPE", "HOTEL", "PRAIA", "NORTE", "VERAO", "CALOR", "FESTA",
    "NOITE", "LIVRO", "FILME", "OSCAR", "PAPEL", "DRAMA", "CANTO", "AMADA", "PORTO",
    "CAMPO", "TERRA", "BARCO", "NAVIO", "FAROL", "VENTO", "MUNDO", "MAPAS", "HOTEL",
    # 4 letters
    "CAFE", "BOLO", "DOCE", "PUDI", "SOPA", "MESA", "FOGO", "AGUA", "OLEO", "CEBO",
    "ALHO", "VARA", "ISCA", "PESC", "CENA", "FITA", "TELA", "ATOR", "OURO", "RISO",
    "FOTO", "ROTA", "MAPA", "MALA", "GUIA", "TREM", "AUTO", "CASA", "AMOR", "VIDA",
    "LUA", "SOL", "MAR", "RIO", "RUA", "PAZ", "LUZ", "MEL", "CHA", "UVA", "OVO",
    "PÃO", "CHÁ", "CEU", "SOM", "DIA", "ATO", "COR", "VER", "DAR", "BOM", "SIM",
    "LA", "AR", "AU", "GA", "EM", "EU", "TU", "SE", "IR", "OI", "DF", "SP", "RJ", "SC", "RS"
]

print(f"Loaded {len(WORDS_VALID)} words")
