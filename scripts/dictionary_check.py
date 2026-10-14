# Script to generate authentic Brazilian crosswords with only real words
# Real words database
WORDS = set([
    # 8 letters
    "ADORAVEL", "OLIVEIRA", "BRASILIA", "PORTUGAL", "SALVADOR", "CURITIBA", "CAMPINAS",
    # 7 letters
    "ALEGRES", "CAMPEAO", "RECEITA", "SABORES", "CINEMAS", "ESTRELA", "PASSEIO", "COLADA",
    # 6 letters
    "ADEPTO", "ALEGRE", "BRASIL", "CINEMA", "JANTAR", "FLORES", "CIDADE", "EXIBIR",
    "SORRIA", "FESTAS", "AMIGOS", "TELONA", "SALGAR", "CARROS", "CAMPO", "PORTOS",
    # 5 letters
    "TOPAR", "PERU", "VARA", "PRAIA", "HOTEL", "NORTE", "VERAO", "CALOR", "FESTA",
    "NOITE", "LIVRO", "FILME", "OSCAR", "PAPEL", "DRAMA", "CANTO", "AMADA", "PORTO",
    "NAVIO", "FAROL", "VENTO", "MUNDO", "MAPAS", "DOCES", "SABOR", "PUDIM", "ARROZ",
    "PEIXE", "MOLHO", "TORTA", "FRUTA", "MASSA", "PIZZA", "CREPE", "CHAVE", "COCAR",
    # 4 letters
    "PROL", "PERU", "VARA", "AMOR", "CASA", "VIDA", "BOLO", "DOCE", "SOPA", "MESA",
    "FOGO", "AGUA", "ALHO", "CENA", "FITA", "TELA", "ATOR", "OURO", "RISO", "FOTO",
    "ROTA", "MAPA", "MALA", "GUIA", "TREM", "AUTO", "LUA", "SOL", "MAR", "RIO",
    "RUA", "PAZ", "LUZ", "MEL", "CHA", "UVA", "OVO", "PAO", "CEU", "SOM", "DIA",
    "ATO", "COR", "VER", "DAR", "BOM", "SIM", "LA", "AR", "AU", "GA", "DF", "SC",
    "SP", "RJ", "MG", "PR", "BA", "RS", "ES", "GO", "MT", "MS", "AM", "PA", "CE",
    "RN", "PB", "PE", "AL", "SE", "PI", "MA", "TO", "RO", "AC", "AP", "RR"
])

print(f"Total words: {len(WORDS)}")
