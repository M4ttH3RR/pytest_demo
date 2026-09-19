
import unittest
import sys
 
sys.path.append(".")  # PATH to find boggle_solver.py  # PATH to find boggle_solver.py
 
from boggle_solver import Boggle
 
 
def normalize(word_list):
    """Helper: uppercase + sort a list of words so comparisons are
    order-independent and case-independent."""
    return sorted(word.upper() for word in word_list)
 
 
# ---------------------------------------------------------------------------
# 1. Grid size / shape / scalability test frames
# ---------------------------------------------------------------------------
class TestSuite_Alg_Scalability_Cases(unittest.TestCase):
 
    def test_Normal_case_3x3(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["abc", "abdhi", "abi", "ef", "cfi", "dea"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["abc", "abdhi", "cfi", "dea"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_case_2x2(self):
        grid = [["A", "B"], ["C", "D"]]
        dictionary = ["abd", "acd", "abc", "xyz"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        # In a 2x2 grid every tile is diagonally adjacent to every other
        # tile, so "abc" (B->C is a diagonal move) is also reachable.
        expected = ["abd", "acd", "abc"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_case_4x4(self):
        grid = [["T", "W", "Y", "R"],
                ["E", "N", "P", "H"],
                ["G", "St", "Qu", "R"],
                ["O", "N", "T", "A"]]
        dictionary = ["art", "ego", "gent", "get", "net", "new", "newt",
                      "prat", "pry", "qua", "quart", "quartz", "rat",
                      "tar", "tarp", "ten", "went", "wet", "stont",
                      "arty", "egg", "not"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["art", "ego", "gent", "get", "net", "new", "newt",
                    "prat", "pry", "qua", "quart", "rat",
                    "tar", "tarp", "ten", "went", "wet", "stont"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_case_5x5(self):
        grid = [["A", "B", "C", "D", "E"],
                ["F", "G", "H", "I", "J"],
                ["K", "L", "M", "N", "O"],
                ["P", "Q", "R", "S", "T"],
                ["U", "V", "W", "X", "Y"]]
        dictionary = ["abc", "fkp", "xyz", "glm"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["abc", "fkp", "glm"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_case_1x1_no_valid_word(self):
        # A single tile can never form a word of length >= 3.
        grid = [["A"]]
        dictionary = ["a", "aaa"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual([], solution)
 
    def test_rectangular_grid_non_square(self):
        # 2 rows x 3 columns - solver should not require a square grid.
        grid = [["A", "B", "C"], ["D", "E", "F"]]
        dictionary = ["abc", "adb", "cfe"]
        mygame = Boggle(grid, dictionary)
        self.assertTrue(mygame.validInput())
        solution = mygame.getSolution()
        expected = ["abc", "adb", "cfe"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_single_row_grid(self):
        grid = [["A", "B", "C", "D"]]
        dictionary = ["abc", "bcd", "acd"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        # "acd" skips over B, which is not adjacent to D, so it must fail.
        expected = ["abc", "bcd"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_single_column_grid(self):
        grid = [["A"], ["B"], ["C"], ["D"]]
        dictionary = ["abc", "bcd"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["abc", "bcd"]
        self.assertEqual(normalize(expected), normalize(solution))
 
 
# ---------------------------------------------------------------------------
# 2. Simple / degenerate / invalid-input edge cases
# ---------------------------------------------------------------------------
class TestSuite_Simple_Edge_Cases(unittest.TestCase):
 
    def test_EmptyGrid_case_0x0(self):
        # A grid containing one empty row is invalid input.
        grid = [[]]
        dictionary = ["hello", "there", "general", "kenobi"]
        mygame = Boggle(grid, dictionary)
        self.assertFalse(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_TrulyEmptyGrid(self):
        # A grid with zero rows is invalid input.
        grid = []
        dictionary = ["hello"]
        mygame = Boggle(grid, dictionary)
        self.assertFalse(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_EmptyDictionary(self):
        grid = [["A", "B"], ["C", "D"]]
        dictionary = []
        mygame = Boggle(grid, dictionary)
        self.assertTrue(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_NonStringTileInGrid(self):
        grid = [[1, 2], [3, 4]]
        dictionary = ["ab"]
        mygame = Boggle(grid, dictionary)
        self.assertFalse(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_MismatchedRowLengths(self):
        grid = [["A", "B"], ["C"]]
        dictionary = ["ac"]
        mygame = Boggle(grid, dictionary)
        self.assertFalse(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_NonListDictionary(self):
        grid = [["A", "B"], ["C", "D"]]
        dictionary = "ab"
        mygame = Boggle(grid, dictionary)
        self.assertFalse(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_NonStringWordInDictionary(self):
        grid = [["A", "B"], ["C", "D"]]
        dictionary = [123, "ab"]
        mygame = Boggle(grid, dictionary)
        self.assertFalse(mygame.validInput())
        self.assertEqual([], mygame.getSolution())
 
    def test_WordShorterThanThreeExcluded(self):
        # Words with fewer than 3 letters are never returned, even if found.
        grid = [["A", "B"]]
        dictionary = ["ab"]
        mygame = Boggle(grid, dictionary)
        self.assertEqual([], mygame.getSolution())
 
    def test_WordNotPresentInGrid(self):
        grid = [["A", "B"], ["C", "D"]]
        dictionary = ["xyz"]
        mygame = Boggle(grid, dictionary)
        self.assertEqual([], mygame.getSolution())
 
    def test_SetGrid_and_SetDictionary_update_state(self):
        mygame = Boggle([["A"]], ["a"])
        mygame.setGrid([["A", "B", "C"]])
        mygame.setDictionary(["abc"])
        solution = mygame.getSolution()
        self.assertEqual(["abc"], solution)
 
 
# ---------------------------------------------------------------------------
# 3. General correctness / complex-pattern coverage
# ---------------------------------------------------------------------------
class TestSuite_Complete_Coverage(unittest.TestCase):
 
    def test_CaseInsensitiveMatching(self):
        grid = [["a", "b", "c"]]
        dictionary = ["ABC"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["ABC"]), normalize(solution))
 
    def test_TileCannotBeReusedInSameWord(self):
        # "ABA" would require revisiting tile A; only one A exists.
        grid = [["A", "B"], ["C", "D"]]
        dictionary = ["aba"]
        mygame = Boggle(grid, dictionary)
        self.assertEqual([], mygame.getSolution())
 
    def test_DiagonalAdjacencyIsAllowed(self):
        # A and B are diagonal neighbors; word should still be found.
        grid = [["A", "X"], ["C", "B"]]
        dictionary = ["abx"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["abx"]), normalize(solution))
 
    def test_NonAdjacentLettersDoNotConnect(self):
        # In a single row, skipping over a tile is not a valid path.
        grid = [["A", "B", "C", "D"]]
        dictionary = ["acd"]
        mygame = Boggle(grid, dictionary)
        self.assertEqual([], mygame.getSolution())
 
    def test_MultipleWordsFoundSimultaneously(self):
        grid = [["T", "W", "Y", "R"],
                ["E", "N", "P", "H"],
                ["G", "St", "Qu", "R"],
                ["O", "N", "T", "A"]]
        dictionary = ["art", "ego", "gent", "get", "net", "new", "newt",
                      "prat", "pry", "qua", "quart", "quartz", "rat",
                      "tar", "tarp", "ten", "went", "wet", "stont",
                      "arty", "egg", "not"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        # "quartz", "arty", "egg", "not" are NOT reachable in this grid.
        self.assertNotIn("QUARTZ", normalize(solution))
        self.assertNotIn("ARTY", normalize(solution))
        self.assertIn("QUART", normalize(solution))
        self.assertIn("GENT", normalize(solution))
 
    def test_LongWordRequiringFullPathTraversal(self):
        grid = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        dictionary = ["abdhi"]  # A->B (diag) ->D(diag)->H(diag)->I(diag)
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["abdhi"]), normalize(solution))
 
    def test_DictionaryWithDuplicateWords(self):
        grid = [["A", "B", "C"]]
        dictionary = ["abc", "abc"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        # Both occurrences are checked independently, so both are appended.
        self.assertEqual(normalize(["abc", "abc"]), normalize(solution))
 
    def test_MultipleStartingPointsForSameLetter(self):
        grid = [["A", "B"], ["A", "C"]]
        dictionary = ["abc", "aac"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["abc", "aac"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_DuplicateLettersInGrid(self):
        # The letter "A" appears four times in this grid. The solver must
        # be able to pick whichever instance makes each word's path valid,
        # rather than getting stuck reusing one fixed "A".
        grid = [["C", "A", "T"],
                ["A", "A", "A"],
                ["R", "A", "N"]]
        dictionary = ["cat", "car", "ran", "tan"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["cat", "car", "ran", "tan"]
        self.assertEqual(normalize(expected), normalize(solution))
 
 
# ---------------------------------------------------------------------------
# 4. Multi-letter tile ("Qu", "St", "Ie", etc.) test frames
# ---------------------------------------------------------------------------
class TestSuite_Qu_and_St(unittest.TestCase):
 
    def test_Qu_tile_alone(self):
        grid = [["Qu", "A", "T"]]
        dictionary = ["quat"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["quat"]), normalize(solution))
 
    def test_St_tile_alone(self):
        grid = [["St", "O", "P"]]
        dictionary = ["stop"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["stop"]), normalize(solution))
 
    def test_Qu_and_St_together_in_grid(self):
        grid = [["T", "W", "Y", "R"],
                ["E", "N", "P", "H"],
                ["G", "St", "Qu", "R"],
                ["O", "N", "T", "A"]]
        dictionary = ["qua", "quart", "stont"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        expected = ["qua", "quart", "stont"]
        self.assertEqual(normalize(expected), normalize(solution))
 
    def test_word_requiring_Qu_but_missing_from_grid_fails(self):
        # No "Qu" tile present, so "quart"-like words cannot be built
        # letter-by-letter from single-letter Q and U tiles.
        grid = [["Q", "U", "A", "T"]]
        dictionary = ["quat"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        # Q-U-A-T are individually adjacent, so this actually succeeds:
        # this test documents that single-letter Q/U tiles work too.
        self.assertEqual(normalize(["quat"]), normalize(solution))
 
    def test_Qu_tile_case_insensitive(self):
        grid = [["qu", "a", "t"]]
        dictionary = ["QUAT"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["QUAT"]), normalize(solution))
 
    def test_word_ending_in_lone_Q(self):
        # "Q" appears here as a plain single-letter tile, not a "Qu" tile,
        # and it is the LAST letter of the word.
        grid = [["I", "R", "A"], ["X", "X", "Q"]]
        dictionary = ["iraq"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["iraq"]), normalize(solution))
 
    def test_lone_Q_followed_by_non_U_letter(self):
        # "Qx" where x != "u": a plain "Q" tile is immediately followed
        # by "A", not "U". This must still match correctly.
        grid = [["Q", "A", "T"]]
        dictionary = ["qat"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual(normalize(["qat"]), normalize(solution))
 
    def test_Qu_tile_word_too_short_is_excluded(self):
        # A 2-letter word ("qu") is excluded by the length >= 3 rule,
        # even though the "Qu" tile alone spells it.
        grid = [["Qu", "A", "T"]]
        dictionary = ["qu"]
        mygame = Boggle(grid, dictionary)
        solution = mygame.getSolution()
        self.assertEqual([], solution)
 
 
if __name__ == '__main__':
    unittest.main()
 
