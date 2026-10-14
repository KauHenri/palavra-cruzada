# Solver to generate valid Swedish Crosswords with interior clues
import unicodedata

def clean_word(w):
    return ''.join(c for c in unicodedata.normalize('NFD', w) if unicodedata.category(c) != 'Mn').upper()

# Common valid Portuguese words by length
WORDS_8 = [
    ("ADORAVEL", "Muito agradável e querido"),
    ("OLIVEIRA", "Árvore de onde vêm as azeitonas"),
    ("PORTUGAL", "País europeu de língua irmã"),
    ("BRASILIA", "Capital federal do Brasil"),
    ("SALVADOR", "Primeira capital do Brasil"),
    ("CAMPINAS", "Grande cidade do interior paulista"),
    ("CURITIBA", "Capital do estado do Paraná"),
    ("AMOROSOS", "Pessoas cheias de carinho"),
    ("ALEGRIAS", "Momentos de grande felicidade")
]

WORDS_6 = [
    ("ADEPTO", "Aquele que segue uma doutrina"),
    ("ALEGRE", "Muito feliz e radiante"),
    ("BRASIL", "Nosso país amado"),
    ("CINEMA", "Arte da sétima tela"),
    ("VIAGEM", "Passeio para conhecer lugares"),
    ("AMORES", "Pessoas muito queridas"),
    ("ROCHAS", "Pedras sólidas"),
    ("FLORES", "Desabrocham na primavera")
]

print("Ready to construct!")
