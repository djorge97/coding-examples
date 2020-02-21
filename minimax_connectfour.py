import abc
import copy
import math
import time
import random


class Game(object):
    """A connect four game."""

    def __init__(self, grid):
        """Instances differ by their board."""
        self.grid = copy.deepcopy(grid)  # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            for mark in row:
                print(mark, end='')
            print()
        print()

    def possible_moves(self):
        """Return a list of possible moves given the current board."""
        # Define possible moves as an empty list
        posmvs = list()

        # Iterate through grid and check for open spaces that a piece can be dropped into
        for j in range(8):
            for i in range(8):
                # Can drop piece if the top of the column has a blank space
                if self.grid[i][j] == '-':
                    posmvs.append(j)
                    break
        # Returns list of free columns to drop into
        return posmvs

    def neighbor(self, col, color):
        """Return a Game instance like this one but with a move made into the specified column."""
        # Drops piece into chosen column until it either hits bottom or another piece, replacing blank space
        neighbor = Game(self.grid)

        for i in range(7):
            for j in range(7):
                # Places piece if empty column
                if j == col and self.grid[i][j] == '-' and i + 1 == 7 and self.grid[i + 1][j] == '-':
                    neighbor.grid[i + 1][j] = color
                # Places piece if there is a piece below it
                elif j == col and self.grid[i][j] == '-' and (self.grid[i + 1][j] == 'R' or self.grid[i + 1][j] == 'B'):
                    neighbor.grid[i][j] = color
        # Returns instance of Game with move made
        return neighbor

    def utility(self):
        """Return the minimax utility value of this game"""
        # Calculate number of pieces in a row red has and add together associated scores
        rscore = self.redscore()
        # Calculate number of pieces in a row black has and add together associated scores
        bscore = self.blackscore()
        # Subtract black score from red score to get final utility
        h = rscore - bscore
        return h

    def redscore(self):
        score = 0
        # Check horizontal consecutive pieces
        # 2 consecutive pieces: +10 to score
        for i in range(8):
            for j in range(7):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] != 'R':
                        score += 10
                elif j == 6:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j-1] != 'R':
                        score += 10
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j-1] != 'R' and self.grid[i][j+2] != 'R':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for i in range(8):
            for j in range(6):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] != 'R':
                        score += 50
                elif j == 5:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j-1] != 'R':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] != 'R' and self.grid[i][j-1] != 'R':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for i in range(8):
            for j in range(5):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] == 'R' and self.grid[i][j+4] != 'R':
                        score += 50
                elif j == 4:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] == 'R' and self.grid[i][j-1] != 'R':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] == 'R' and self.grid[i][j+4] != 'R' and self.grid[i][j-1] != 'R':
                        score += 50
        # Check vertical consecutive pieces
        # 2 consecutive pieces: +10 to score
        for j in range(8):
            for i in range(7):
                # Edge pieces
                if i == 0:
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j] == 'R' and self.grid[i + 2][j] != 'R':
                        score += 10
                elif i == 6:
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j] == 'R' and self.grid[i - 1][j] != 'R':
                        score += 10
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j] == 'R' and self.grid[i - 1][j] != 'R' and self.grid[i + 2][j] != 'R':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for i in range(8):
            for j in range(6):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] != 'R':
                        score += 50
                elif j == 5:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j-1] != 'R':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] != 'R' and self.grid[i][j-1] != 'R':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for j in range(8):
            for i in range(5):
                # Edge pieces
                if i == 0:
                    if self.grid[i][j] == 'R' and self.grid[i+1][j] == 'R' and self.grid[i+2][j] == 'R' and self.grid[i+3][j] == 'R' and self.grid[i+4][j] != 'R':
                        score += 50
                elif i == 4:
                    if self.grid[i][j] == 'R' and self.grid[i+1][j] == 'R' and self.grid[i+2][j] == 'R' and self.grid[i+3][j] == 'R' and self.grid[i-1][j] != 'R':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'R' and self.grid[i+1][j] == 'R' and self.grid[i+2][j] == 'R' and self.grid[i+3][j] == 'R' \
                            and self.grid[i+4][j] != 'R' and self.grid[i-1][j] != 'R':
                        score += 50
        # Check + slope diagonal consecutive pieces
        # 2 consecutive pieces: +10 to score
        for j in range(0, 7):
            for i in range(1, 8):
                # "Edge" pieces
                if (i == 1 and j == 0) or (i == 7 and j == 6):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R':
                        score += 10
                elif (i == 1 and 1 <= j <= 6) or (1 <= i <= 6 and j == 6):
                    if self.grid[i][j] == 'R' and self.grid[i-1][j+1] == 'R' and self.grid[i+1][j-1] != 'R':
                        score += 10
                elif (2 <= i <= 7 and j == 0) or (i == 7 and 0 <= j <= 5):
                    if self.grid[i][j] == 'R' and self.grid[i-1][j+1] == 'R' and self.grid[i-2][j+2] != 'R':
                        score += 10
                # Non-edge pieces
                elif 2 <= i <= 6 and 1 <= j <= 5:
                    if self.grid[i][j] == 'R' and self.grid[i-1][j+1] == 'R' and self.grid[i-2][j+2] != 'R' and self.grid[i+1][j-1] != 'R':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for j in range(0, 6):
            for i in range(2, 8):
                # "Edge" pieces
                if (i == 2 and j == 0) or (i == 7 and j == 5):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R':
                        score += 50
                elif (i == 2 and 1 <= j <= 5) or (2 <= i <= 6 and j == 5):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R' and self.grid[i + 1][j - 1] != 'R':
                        score += 50
                elif (3 <= i <= 7 and j == 0) or (i == 7 and 0 <= j <= 4):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R' and self.grid[i - 3][j + 3] != 'R':
                        score += 50
                # Non-edge pieces
                elif 3 <= i <= 6 and 1 <= j <= 4:
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R'\
                            and self.grid[i - 3][j + 3] != 'R' and self.grid[i + 1][j - 1] != 'R':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for j in range(0, 5):
            for i in range(3, 8):
                # "Edge" pieces
                if (i == 3 and j == 0) or (i == 7 and j == 4):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R' and self.grid[i - 3][j + 3] == 'R':
                        score += 100
                elif (i == 3 and 1 <= j <= 4) or (3 <= i <= 6 and j == 4):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R' and self.grid[i - 3][j + 3] == 'R' \
                            and self.grid[i + 1][j - 1] != 'R':
                        score += 100
                elif (4 <= i <= 7 and j == 0) or (i == 7 and 0 <= j <= 3):
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R' and self.grid[i - 3][j + 3] == 'R' \
                            and self.grid[i - 4][j + 4] != 'R':
                        score += 100
                # Non-edge pieces
                elif 4 <= i <= 6 and 1 <= j <= 3:
                    if self.grid[i][j] == 'R' and self.grid[i - 1][j + 1] == 'R' and self.grid[i - 2][j + 2] == 'R' and self.grid[i - 3][j + 3] == 'R'\
                            and self.grid[i - 4][j + 4] != 'R' and self.grid[i + 1][j - 1] != 'R':
                        score += 100
        # Check - slope diagonal consecutive pieces
        # 2 consecutive pieces: +10 to score
        for j in range(0, 7):
            for i in range(0, 7):
                # "Edge" pieces
                if (i == 6 and j == 0) or (i == 0 and j == 6):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R':
                        score += 10
                elif (i == 0 and 0 <= j <= 5) or (0 <= i <= 5 and j == 0):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] != 'R':
                        score += 10
                elif (1 <= i <= 6 and j == 6) or (i == 6 and 1 <= j <= 6):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i - 1][j - 1] != 'R':
                        score += 10
                # Non-edge pieces
                elif 1 <= i <= 5 and 1 <= j <= 5:
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' \
                            and self.grid[i + 2][j + 2] != 'R' and self.grid[i - 1][j - 1] != 'R':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for j in range(0, 6):
            for i in range(0, 6):
                # "Edge" pieces
                if (i == 5 and j == 0) or (i == 0 and j == 5):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R':
                        score += 50
                elif (i == 0 and 0 <= j <= 4) or (0 <= i <= 4 and j == 0):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' and self.grid[i + 3][j + 3] != 'R':
                        score += 50
                elif (1 <= i <= 5 and j == 5) or (i == 5 and 1 <= j <= 5):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' and self.grid[i - 1][j - 1] != 'R':
                        score += 50
                # Non-edge pieces
                elif 1 <= i <= 4 and 1 <= j <= 4:
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' \
                            and self.grid[i + 3][j + 3] != 'R' and self.grid[i - 1][j + 1] != 'R':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for j in range(0, 5):
            for i in range(3, 8):
                # "Edge" pieces
                if (i == 0 and j == 4) or (i == 4 and j == 0):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' and self.grid[i + 3][j + 3] == 'R':
                        score += 100
                elif (i == 0 and 0 <= j <= 3) or (0 <= i <= 3 and j == 0):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' and self.grid[i + 3][j + 3] == 'R' \
                            and self.grid[i + 4][j + 4] != 'R':
                        score += 100
                elif (1 <= i <= 4 and j == 4) or (i == 4 and 1 <= j <= 4):
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' and self.grid[i + 3][j + 3] == 'R' \
                            and self.grid[i - 1][j - 1] != 'R':
                        score += 100
                # Non-edge pieces
                elif 1 <= i <= 3 and 1 <= j <= 3:
                    if self.grid[i][j] == 'R' and self.grid[i + 1][j + 1] == 'R' and self.grid[i + 2][j + 2] == 'R' and self.grid[i + 3][j + 3] == 'R' \
                            and self.grid[i + 4][j + 4] != 'R' and self.grid[i - 1][j - 1] != 'R':
                        score += 100
        # Return final calculated score for red's positions
        return score

    def blackscore(self):
        score = 0
        # Check horizontal consecutive pieces
        # 2 consecutive pieces: +10 to score
        for i in range(8):
            for j in range(7):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] != 'B':
                        score += 10
                elif j == 6:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j - 1] != 'B':
                        score += 10
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j - 1] != 'B' and \
                            self.grid[i][j + 2] != 'B':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for i in range(8):
            for j in range(6):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] != 'B':
                        score += 50
                elif j == 5:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j - 1] != 'B':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] != 'B' and self.grid[i][j - 1] != 'B':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for i in range(8):
            for j in range(5):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] == 'B' and self.grid[i][j + 4] != 'B':
                        score += 50
                elif j == 4:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] == 'B' and self.grid[i][j - 1] != 'B':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] == 'B' and self.grid[i][j + 4] != 'B' and self.grid[i][j - 1] != 'B':
                        score += 50
        # Check vertical consecutive pieces
        # 2 consecutive pieces: +10 to score
        for j in range(8):
            for i in range(7):
                # Edge pieces
                if i == 0:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j] == 'B' and self.grid[i + 2][j] != 'B':
                        score += 10
                elif i == 6:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j] == 'B' and self.grid[i - 1][j] != 'B':
                        score += 10
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j] == 'B' and self.grid[i - 1][j] != 'B' and \
                            self.grid[i + 2][j] != 'B':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for i in range(8):
            for j in range(6):
                # Edge pieces
                if j == 0:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] != 'B':
                        score += 50
                elif j == 5:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j - 1] != 'B':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'B' and self.grid[i][j + 1] == 'B' and self.grid[i][j + 2] == 'B' and \
                            self.grid[i][j + 3] != 'B' and self.grid[i][j - 1] != 'B':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for j in range(8):
            for i in range(5):
                # Edge pieces
                if i == 0:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j] == 'B' and self.grid[i + 2][j] == 'B' and \
                            self.grid[i + 3][j] == 'B' and self.grid[i + 4][j] != 'B':
                        score += 50
                elif i == 4:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j] == 'B' and self.grid[i + 2][j] == 'B' and \
                            self.grid[i + 3][j] == 'B' and self.grid[i - 1][j] != 'B':
                        score += 50
                # Non-edge pieces
                else:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j] == 'B' and self.grid[i + 2][j] == 'B' and \
                            self.grid[i + 3][j] == 'B' \
                            and self.grid[i + 4][j] != 'B' and self.grid[i - 1][j] != 'B':
                        score += 50
        # Check + slope diagonal consecutive pieces
        # 2 consecutive pieces: +10 to score
        for j in range(0, 7):
            for i in range(1, 8):
                # "Edge" pieces
                if (i == 1 and j == 0) or (i == 7 and j == 6):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B':
                        score += 10
                elif (i == 1 and 1 <= j <= 6) or (1 <= i <= 6 and j == 6):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i + 1][j - 1] != 'B':
                        score += 10
                elif (2 <= i <= 7 and j == 0) or (i == 7 and 0 <= j <= 5):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] != 'B':
                        score += 10
                # Non-edge pieces
                elif 2 <= i <= 6 and 1 <= j <= 5:
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] != 'B' and \
                            self.grid[i + 1][j - 1] != 'B':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for j in range(0, 6):
            for i in range(2, 8):
                # "Edge" pieces
                if (i == 2 and j == 0) or (i == 7 and j == 5):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B':
                        score += 50
                elif (i == 2 and 1 <= j <= 5) or (2 <= i <= 6 and j == 5):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' and \
                            self.grid[i + 1][j - 1] != 'R':
                        score += 50
                elif (3 <= i <= 7 and j == 0) or (i == 7 and 0 <= j <= 4):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' and \
                            self.grid[i - 3][j + 3] != 'B':
                        score += 50
                # Non-edge pieces
                elif 3 <= i <= 6 and 1 <= j <= 4:
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' \
                            and self.grid[i - 3][j + 3] != 'B' and self.grid[i + 1][j - 1] != 'B':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for j in range(0, 5):
            for i in range(3, 8):
                # "Edge" pieces
                if (i == 3 and j == 0) or (i == 7 and j == 4):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' and \
                            self.grid[i - 3][j + 3] == 'B':
                        score += 100
                elif (i == 3 and 1 <= j <= 4) or (3 <= i <= 6 and j == 4):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' and \
                            self.grid[i - 3][j + 3] == 'B' \
                            and self.grid[i + 1][j - 1] != 'B':
                        score += 100
                elif (4 <= i <= 7 and j == 0) or (i == 7 and 0 <= j <= 3):
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' and \
                            self.grid[i - 3][j + 3] == 'B' \
                            and self.grid[i - 4][j + 4] != 'B':
                        score += 100
                # Non-edge pieces
                elif 4 <= i <= 6 and 1 <= j <= 3:
                    if self.grid[i][j] == 'B' and self.grid[i - 1][j + 1] == 'B' and self.grid[i - 2][j + 2] == 'B' and \
                            self.grid[i - 3][j + 3] == 'B' \
                            and self.grid[i - 4][j + 4] != 'B' and self.grid[i + 1][j - 1] != 'B':
                        score += 100
        # Check - slope diagonal consecutive pieces
        # 2 consecutive pieces: +10 to score
        for j in range(0, 7):
            for i in range(0, 7):
                # "Edge" pieces
                if (i == 6 and j == 0) or (i == 0 and j == 6):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B':
                        score += 10
                elif (i == 0 and 0 <= j <= 5) or (0 <= i <= 5 and j == 0):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] != 'B':
                        score += 10
                elif (1 <= i <= 6 and j == 6) or (i == 6 and 1 <= j <= 6):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i - 1][j - 1] != 'B':
                        score += 10
                # Non-edge pieces
                elif 1 <= i <= 5 and 1 <= j <= 5:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' \
                            and self.grid[i + 2][j + 2] != 'B' and self.grid[i - 1][j - 1] != 'B':
                        score += 10
        # 3 consecutive pieces: +50 to score
        for j in range(0, 6):
            for i in range(0, 6):
                # "Edge" pieces
                if (i == 5 and j == 0) or (i == 0 and j == 5):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B':
                        score += 50
                elif (i == 0 and 0 <= j <= 4) or (0 <= i <= 4 and j == 0):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' and \
                            self.grid[i + 3][j + 3] != 'B':
                        score += 50
                elif (1 <= i <= 5 and j == 5) or (i == 5 and 1 <= j <= 5):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' and \
                            self.grid[i - 1][j - 1] != 'B':
                        score += 50
                # Non-edge pieces
                elif 1 <= i <= 4 and 1 <= j <= 4:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' \
                            and self.grid[i + 3][j + 3] != 'B' and self.grid[i - 1][j + 1] != 'B':
                        score += 50
        # 4 consecutive pieces: +100 to score
        for j in range(0, 5):
            for i in range(3, 8):
                # "Edge" pieces
                if (i == 0 and j == 4) or (i == 4 and j == 0):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' and \
                            self.grid[i + 3][j + 3] == 'B':
                        score += 100
                elif (i == 0 and 0 <= j <= 3) or (0 <= i <= 3 and j == 0):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' and \
                            self.grid[i + 3][j + 3] == 'B' \
                            and self.grid[i + 4][j + 4] != 'B':
                        score += 100
                elif (1 <= i <= 4 and j == 4) or (i == 4 and 1 <= j <= 4):
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' and \
                            self.grid[i + 3][j + 3] == 'B' \
                            and self.grid[i - 1][j - 1] != 'B':
                        score += 100
                # Non-edge pieces
                elif 1 <= i <= 3 and 1 <= j <= 3:
                    if self.grid[i][j] == 'B' and self.grid[i + 1][j + 1] == 'B' and self.grid[i + 2][j + 2] == 'B' and \
                            self.grid[i + 3][j + 3] == 'B' \
                            and self.grid[i + 4][j + 4] != 'B' and self.grid[i - 1][j - 1] != 'B':
                        score += 100
        # Return final calculated score for red's positions
        return score

    def winning_state(self):
        """Returns float("inf") if Red wins; float("-inf") if Black wins;
           0 if board full; None if not full and no winner"""
        # Assign infinity and -infinity to variables for readability
        redw = float("inf")
        blackw = float("-inf")
        fullcheck = 0

        # Vertical four-in-a-row check
        for j in range(8):
            for i in range(5):
                # If 4 reds are consecutively in the same column, red wins, likewise for black
                if self.grid[i][j] == 'R' and self.grid[i+1][j] == 'R' and self.grid[i+2][j] == 'R' and self.grid[i+3][j] == 'R':
                    return redw
                elif self.grid[i][j] == 'B' and self.grid[i+1][j] == 'B' and self.grid[i+2][j] == 'B' and self.grid[i+3][j] == 'B':
                    return blackw
        # Horizontal four-in-a-row check
        for i in range(8):
            for j in range(5):
                # If 4 reds are consecutively in the same row, red wins, likewise for black
                if self.grid[i][j] == 'R' and self.grid[i][j+1] == 'R' and self.grid[i][j+2] == 'R' and self.grid[i][j+3] == 'R':
                    return redw
                elif self.grid[i][j] == 'B' and self.grid[i][j+1] == 'B' and self.grid[i][j+2] == 'B' and self.grid[i][j+3] == 'B':
                    return blackw
        # Positive slope diagonal check
        for j in range(5):
            for i in range(3, 8):
                if self.grid[i][j] == 'R' and self.grid[i-1][j+1] == 'R' and self.grid[i-2][j+2] == 'R' and self.grid[i-3][j+3] == 'R':
                    return redw
                elif self.grid[i][j] == 'B' and self.grid[i-1][j+1] == 'B' and self.grid[i-2][j+2] == 'B' and self.grid[i-3][j+3] == 'B':
                    return blackw
        # Negative slope diagonal check
        for j in range(5):
            for i in range(0, 5):
                if self.grid[i][j] == 'R' and self.grid[i+1][j+1] == 'R' and self.grid[i+2][j+2] == 'R' and self.grid[i+3][j+3] == 'R':
                    return redw
                elif self.grid[i][j] == 'B' and self.grid[i+1][j+1] == 'B' and self.grid[i+2][j+2] == 'B' and self.grid[i+3][j+3] == 'B':
                    return blackw
        # Full board check
        for i in range(8):
            for j in range(8):
                # Checks each square and increments counter anytime a piece is found; if 64 pieces are found,
                # board is full
                if self.grid[i][j] == 'R' or self.grid[i][j] == 'B':
                    fullcheck += 1
                if fullcheck == 64:
                    return 0
        # If function hasn't returned a value at this point, we can assume the board is not full and there is no winner
        return None


class Agent(object):
    """Abstract class, extended by classes RandomAgent, FirstMoveAgent, MinimaxAgent.
    Do not make an instance of this class."""

    def __init__(self, color):
        """Agents use either RED or BLACK chips."""
        self.color = color

    @abc.abstractmethod
    def move(self, game):
        """Abstract. Must be implemented by a class that extends Agent."""
        pass


class RandomAgent(Agent):
    """Naive agent -- always performs a random move"""

    def move(self, game):
        """Returns a random move"""
        # Selects a random move from the list of possible moves, i.e. open columns
        col = random.choice(game.possible_moves())
        return col


class FirstMoveAgent(Agent):
    """Naive agent -- always performs the first move"""

    def move(self, game):
        """Returns the first possible move"""
        # Selects first move on the list of possible moves
        posmvs = game.possible_moves()
        col = posmvs[0]
        return col


class MinimaxAgent(Agent):
    """Smart agent -- uses minimax to determine the best move"""

    def move(self, game):
        """Returns the best move using minimax"""
        col, score = self.minimax(game, 4, True, -math.inf, math.inf)
        return col

    # Apply Minimax algorithm (based on pseudocode from Wikipedia article on Minimax)
    def minimax(self, game, layer, max_player, a, b):
        # If depth is 0 or we reach the terminal node, return the heuristic value of the node
        if layer == 0:
            return None, game.utility()
        if max_player:
            # Maxvalue begins at -infinity
            maxval = -math.inf
            col = 0
            for j in game.possible_moves():
                # Iterate through possible moves and make recursive moves alternating between maxplayer and minplayer
                val = MinimaxAgent.minimax(self, game.neighbor(j, 'R'), layer - 1, False, a, b, )[1]
                # If returned value is greater than the max value, assign make the value the new max and compare it to
                # alpha, taking the max of the value, alpha pair
                if val > maxval:
                    maxval = val
                    col = j
                a = max(a, maxval)
                if a >= b:
                    break
            return col, maxval
        else:
            # Min_player so to speak
            # Minvalue begins at infinity
            minval = math.inf
            col = 0
            for j in game.possible_moves():
                val = MinimaxAgent.minimax(self, game.neighbor(j, 'B'), layer - 1, True, a, b)[1]
                # If returned value is less than the min value, assign the value with the new min and compare it to
                # beta, taking the min of the value, beta pair
                if val < minval:
                    minval = val
                    col = j
                b = min(b, minval)
                if a >= b:
                    break
            return col, minval


def tournament(simulations=50):
    """Simulate connect four games, of a minimax agent playing
    against a random agent"""
    redwin, blackwin, tie = 0, 0, 0
    for i in range(simulations):
        game = single_game(io=False)
        print(i, end=" ")
        if game.winning_state() == float("inf"):
            redwin += 1
        elif game.winning_state() == float("-inf"):
            blackwin += 1
        elif game.winning_state() == 0:
            tie += 1
    print("Red %d (%.0f%%) Black %d (%.0f%%) Tie %d" % (
        redwin, redwin / simulations * 100, blackwin, blackwin / simulations * 100, tie))

    return redwin / simulations


def single_game(io=True):
    """Create a game and have two agents play it."""
    game = Game([['-' for i in range(8)] for j in range(8)])  # 8x8 empty board
    if io:
        game.display()

    maxplayer = MinimaxAgent('R')
    minplayer = RandomAgent('B')

    while True:
        m = maxplayer.move(game)
        game = game.neighbor(m, maxplayer.color)
        if io:
            time.sleep(.5)
            game.display()

        if game.winning_state() is not None:
            break

        m = minplayer.move(game)
        game = game.neighbor(m, minplayer.color)
        if io:
            time.sleep(.5)
            game.display()

        if game.winning_state() is not None:
            break

    if game.winning_state() == float("inf"):
        print("RED WINS!")
    elif game.winning_state() == float("-inf"):
        print("BLACK WINS!")
    elif game.winning_state() == 0:
        print("TIE!")

    return game


if __name__ == '__main__':
    single_game(io=True)
    tournament(simulations=100)
