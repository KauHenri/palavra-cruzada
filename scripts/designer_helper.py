import unicodedata
from strict_verifier import test_level_design

# Let's write a helper to display and verify any grid in real time
def inspect_candidate(rows, cols, raw_grid, clues_map, words_meta):
    try:
        res = test_level_design(rows, cols, raw_grid, clues_map, words_meta)
        print("VERIFICATION PASSED!")
        return True
    except Exception as e:
        print(f"VERIFICATION FAILED: {e}")
        return False
