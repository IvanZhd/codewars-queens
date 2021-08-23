# %%
import os

os.environ["NUMPY_EXPERIMENTAL_ARRAY_FUNCTION"] = "0"

import numpy as np
import time
import re
import cProfile
import pstats


def timeit(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print("func:%r args:[%r, %r] took: %2.4f sec" % (f.__name__, args, kw, te - ts))
        return result

    return timed


class queens:
    def __init__(self, n, fixed_position):
        self.fixed_position = fixed_position
        self.n = n
        self.attempt = 0
        self.queens_positions = []
        self.text = ""
        self.attempts_max = 10000
        self.solved = False

    def init_board(self):
        self.board = np.ones((self.n, self.n))
        self.count_queens = 0
        self.queens_positions = []
        self.place_queen(self.fixed_position)

    # @timeit
    def place_queen(self, position):
        row, col = position
        # Fill row
        self.board[row, :] = 0
        # Fill column
        self.board[:, col] = 0
        # Fill diagonals
        d1 = np.diag(self.board, k=col - row)
        d2 = np.diag(np.flipud(self.board), k=col + row - self.n + 1)
        d1.flags["WRITEABLE"] = True
        d2.flags["WRITEABLE"] = True
        d1[...] = 0
        d2[...] = 0
        # Place queen
        self.queens_positions.append(position)
        # Count queens
        self.count_queens += 1

    def place_board(self):
        # Initiate a new board
        self.init_board()
        # Fill the board until there is no safe position
        # Iterate over rows
        for i, row in enumerate(self.board):
            # Get array of next nonzeros (safe positons)
            a = np.nonzero(row)[0]
            # If there some nonzeros (safe positions)
            if a.size != 0:
                # Place queen in that position
                self.place_queen((i, a[np.random.choice(a.shape[0], 1)][0]))

    @timeit
    def place_allqueens(self):
        """It is not all time possible to place N queens at first attempt.
        I use while loop to make multiple attempts and place queens randomly to safe positions.
        The safe cells (zeros) are getting updated after each placement of a queen.
        There is also no solution for some fixed positions, e.g. n=4 and (0,0)"""

        # Do until N queens are placed
        while self.attempt < self.attempts_max:
            # Select function depending on multiprocessing
            self.place_board()
            # Quit only if N queens are placed
            if self.count_queens == self.n:
                self.solved = True
                print("Solution is found")
                break
            # Count attempt
            self.attempt += 1
        # Show message if max attempts is reached
        if self.attempt == self.attempts_max:
            print("Max attempts is reached")

    def board2text(self):
        # Convert array fo tuples into array
        a = np.array([*self.queens_positions])
        # Place 2 for queens positions
        self.board[a[:, 0], a[:, 1]] = 2
        # Dictionary to format text
        d = {"\[": "", "\]": "", " ": "", "0.": ".", "2.": "Q"}
        # Convert matrix to string
        self.text = np.array2string(self.board)
        # Do replacements to get required text output
        for old, new in d.items():
            self.text = re.sub(old, new, self.text)
        self.text = self.text + "\n"


def solve_n_queens(n, fixed_queen):

    # For 2 and 3 there is not solution
    if (n in [2, 3]) or any(x >= n for x in fixed_queen):
        print("No solution")
        return None
    # For other cases there might be also no solution for a specific fixed position
    else:
        q = queens(n, fixed_queen)
        q.place_allqueens()
        if q.solved:
            q.board2text()
            print(q.board)
            return q.text
        else:
            return None


if __name__ == "__main__":

    with cProfile.Profile() as pr:
        solve_n_queens(500, (0, 0))

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


# %%
