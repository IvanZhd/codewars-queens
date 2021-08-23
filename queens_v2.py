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
        self.text = ""
        self.attempts_max = 10000
        self.solved = False
        print("Class queens is initialized")

    def initBoard(self):
        self.board = np.zeros((self.n, self.n))
        self.queens_positions = []

    def shuffle(self):
        rows = list(range(self.n))
        cols = list(range(self.n))
        random.shuffle(rows)
        random.shuffle(cols)
        self.queens_positions = list(zip(rows, cols))

    # @timeit
    def place(self):
        # Convert array fo tuples into array
        a = np.array([*self.queens_positions])
        # Place 2 for queens positions
        self.board[a[:, 0], a[:, 1]] = 2
        # Count attempt
        self.attempt += 1

    def checkSameDiag(self, pos1, pos2):
        # Condition to check if the both the elements are in same diagonal of a matrix
        I, J = pos1
        P, Q = pos2
        if abs(P-I) == abs(Q-J):
            return True
        else:
            return False

    def validate(self):
        # All combinations of pairs of queens positions to check if there are some on same diagonal
        comb = list(itertools.combinations(q.queens_positions, 2))
        a = list(map(lambda x: self.checkSameDiag(*x), comb))
        self.solved = not any(a)


if __name__ == "__main__":

    q = queens(20, (0, 0))

    while True:
        q.initBoard()
        q.shuffle()
        q.place()
        q.validate()
        if q.solved == True:
            break

    print(q.board)
    print(q.solved)

    # l = [(0, 1), (1, 3), (2, 5), (3, 0), (4, 2), (5, 4)]
    # comb = list(itertools.combinations(l, 2))
    # print(comb)
    # a = list(map(lambda x: q.checkSameDiag(*x), comb))
    # print(a)
    # solved = not any(a)

    # print(solved)

# %%
