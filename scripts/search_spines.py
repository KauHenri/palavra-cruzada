import unicodedata
from strict_verifier import test_level_design

# Let's test a handcrafted 9x7 level: "Fase 1: Pelo Brasil"
# Authentic Swedish Crossword layout with interior clues:
# Let's see:
# Can we have:
# Col 1: B - R - A - S - I - L - I - A (BRASÍLIA - 8 letters down)
# Col 6: P - O - R - T - U - G - A - L (PORTUGAL - 8 letters down)
# Row 1: B - O - M - D - I - A? B - O - N - I - T - P?
# Row 1: B - R - I - N - C - P?
# B at (1,1), P at (1,6).
# 6 letters starting with B and ending with P? No Portuguese word ends with P!
# Wait! In Quebra-cabeça 18:
# Row 1 was: A - D - E - P - T - O (6 letters: ADEPTO)
# Col 1 was: A - D - O - R - A - V - E - L (8 letters: ADORÁVEL)
# Col 6 was: O - L - I - V - E - I - R - A (8 letters: OLIVEIRA)
# Notice: Row 1 started with 'A' (first letter of ADORÁVEL) and ended with 'O' (first letter of OLIVEIRA)!
# And Row 5: A - L - E - G - R - E (6 letters: ALEGRE)
# Started with 'A' (fifth letter of ADORÁVEL) and ended with 'E' (fifth letter of OLIVEIRA)!
# That is why ADORÁVEL and OLIVEIRA were chosen:
# At row 1: A and O -> ADEPTO!
# At row 5: A and E -> ALEGRE!
# That is pure genius!

# Now, can we find other pairs of 8-letter words for Col 1 and Col 6?
# Let's search!
