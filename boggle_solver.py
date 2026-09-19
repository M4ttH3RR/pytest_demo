"""
Matthew Herriman
@03130572
"""

class Boggle:
    def __init__(self, grid, dictionary):
        self.grid = grid
        self.dictionary = dictionary
        self.solutions = []

    def setGrid(self, grid):
        # Set the game grid.
        self.grid = grid

    def setDictionary(self, dictionary):
        # Set the dictionary of words.
        self.dictionary = dictionary

    def validInput(self):
        # Check that the grid is a list.
        if not isinstance(self.grid, list):
            return False

        if len(self.grid) == 0:
            return False

        # Check that every row is a list.
        for row in self.grid:
            if not isinstance(row, list):
                return False

        columns = len(self.grid[0])

        if columns == 0:
            return False

        # Check that all rows have the same number of columns
        # and that every tile is a string.
        for row in self.grid:
            if len(row) != columns:
                return False

            for tile in row:
                if not isinstance(tile, str):
                    return False

        # Check that the dictionary is a list.
        if not isinstance(self.dictionary, list):
            return False

        for word in self.dictionary:
            if not isinstance(word, str):
                return False

        return True

    def getSolution(self):
        if not self.validInput():
            return []

        # Search for every dictionary word in the grid.
        for word in self.dictionary:
            if len(word) >= 3:
                if self.findWord(word):
                    self.solutions.append(word)

        return self.solutions

    def findWord(self, word):
        # Check every tile as a possible starting point.
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                tile = self.grid[row][col].lower()

                if word.lower().startswith(tile):
                    if self.search(row, col, word, 0, []):
                        return True

        return False

    def search(self, row, col, word, index, used):
        if index == len(word):
            return True

        # Make sure the position is inside the grid.
        if row < 0 or row >= len(self.grid):
            return False

        if col < 0 or col >= len(self.grid[row]):
            return False

        # A tile cannot be used more than once.
        if [row, col] in used:
            return False

        tile = self.grid[row][col].lower()

        if word.lower().startswith(tile, index) == False:
            return False

        used.append([row, col])

        # Move forward by the number of letters in the tile.
        # This handles Qu, St, and Ie as two-letter tiles.
        next_index = index + len(tile)

        # Check all eight neighboring tiles, including diagonals.
        for row_change in [-1, 0, 1]:
            for col_change in [-1, 0, 1]:
                if row_change == 0 and col_change == 0:
                    continue

                if self.search(row + row_change,
                               col + col_change,
                               word,
                               next_index,
                               used):
                    used.pop()
                    return True

        # Backtrack if this path does not work.
        used.pop()
        return False


def main():
    grid = [["T", "W", "Y", "R"], ["E", "N", "P", "H"],
            ["G", "Z", "Qu", "R"], ["O", "N", "T", "A"]]
    dictionary = ["art", "ego", "gent", "get", "net", "new", "newt",
                  "prat", "pry", "qua", "quart", "quartz", "rat",
                  "tar", "tarp", "ten", "went", "wet", "arty",
                  "rhr", "not", "quar"]

    mygame = Boggle(grid, dictionary)
    print(mygame.getSolution())


if __name__ == "__main__":
    main()