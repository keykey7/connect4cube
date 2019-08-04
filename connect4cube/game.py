import logging
from itertools import permutations, combinations_with_replacement, product

import numpy as np

EMPTY = 0
RED = 1
BLUE = 2


class RuleViolation(Exception):
    pass


class Game:
    LOG = logging.getLogger(__name__)
    DIR = list(product([0, 1], repeat=3))

    def __init__(self):
        self.cube = np.full((5, 5, 5), EMPTY)
        self.next = RED

    def move(self, x, y):
        assert 0 <= x < 5 and 0 <= y < 5
        z = 0
        while z < 5 and self.cube[x, y, z] != EMPTY:
            z += 1
        if z == 5:
            raise RuleViolation("already full at {},{}".format(x, y))
        self.cube[x, y, z] = self.next
        self.next = RED if self.next == BLUE else BLUE

    def field(self, x, y, z):
        assert 0 <= x < 5 and 0 <= y < 5 and 0 <= z < 5
        return self.cube[x, y, z]

    def winner(self):
        redo this...


        for p0 in self.DIR:
            color0 = self.cube[p0]
            if color0 == EMPTY:
                break
            for direction in self.DIR:
                p = p0
                for i in range(4):  # three more with same color
                    p = (p[0] + direction[0], p[1] + direction[1], p[2] + direction[2])
                    if color0 != self.cube[p]:
                        break
                    if i == 3:
                        return color0
        return EMPTY
