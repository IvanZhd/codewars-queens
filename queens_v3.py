# %%
import random
import numpy as np
import time
import itertools


def timeit(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print("func:%r args:[%r, %r] took: %2.4f sec" %
              (f.__name__, args, kw, te - ts))
        return result

    return timed


class queens:

    def __init__(self, n, fixed_position):
        self.fixed_position = fixed_position
        self.n = n
        self.attempt = 0
        self.attempts_max = 100
        self.solved = False
        self.board = np.zeros((self.n, self.n))
        self.boardtext = ""

        print("Class queens is initialized")

    def place(self):
        # Count attempt
        self.attempt += 1
        # Reset queens position
        self.queens_positions = [self.fixed_position]
        # Generate rows and cols
        rows = list(range(self.n))
        rows.remove(self.fixed_position[0])
        cols = list(range(self.n))
        cols.remove(self.fixed_position[1])
        # Iterate over rows
        for row in rows:
            # Validate
            self.validate(row, cols)
            # Remove from colums if validated (there is a new queens position)
            col = self.queens_positions[-1][1]
            if col in cols:
                cols.remove(col)

    def validate(self, row, cols):

        for col in cols:
            # Get all combinations with previous positions
            comb = list(itertools.combinations(
                self.queens_positions + [(row, col)], 2))
            # Check if is not on a diagonal with another queen
            valid = not any(
                list(map(lambda x: self.checkSameDiag(*x), comb)))
            # If position is not valid, then repeat random choice, otherwise add this position to list
            if valid:
                self.queens_positions.append((row, col))
                break

    def getBoard(self):
        # Convert array fo tuples into array
        a = np.array([*self.queens_positions])
        # Place 2 for queens positions
        self.board[a[:, 0], a[:, 1]] = 2
        # Check if solved
        self.solved = np.count_nonzero(self.board == 2) == self.n

    @staticmethod
    def checkSameDiag(pos1, pos2):
        # Condition to check if the both the elements are in same diagonal of a matrix
        I, J = pos1
        P, Q = pos2
        if abs(P-I) == abs(Q-J):
            return True
        else:
            return False


if __name__ == "__main__":

    q = queens(8, (0, 0))

    while q.attempt <= q.attempts_max:
        q.place()
        if len(q.queens_positions) == q.n:
            break

    q.getBoard()

    print(q.board)
    print(q.solved)
    print(q.attempt)

# %%
