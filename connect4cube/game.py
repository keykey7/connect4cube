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
    DIR.pop(0)

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
        current = self.next
        self.cube[x, y, z] = current
        self.next = RED if self.next == BLUE else BLUE
        return self.is_winning(x, y, z, current)

    def field(self, x, y, z):
        assert 0 <= x < 5 and 0 <= y < 5 and 0 <= z < 5
        return self.cube[x, y, z]

    def is_winning(self, x, y, z, color):
        for d in self.DIR:
            p = (x, y, z)
            i = 0
            for i in range(3):
                p = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
                if p[0] > 5 or p[1] > 5 or p[2] > 5:
                    break
                if color != self.cube[p]:
                    break
                if i == 2:
                    return True
            p = (x, y, z)
            for i in range(i, 3):
                p = (p[0] - d[0], p[1] - d[1], p[2] - d[2])
                if 0 > p[0] or 0 > p[1] or 0 > p[2]:
                    break
                if color != self.cube[p]:
                    break
                if i == 2:
                    return True
        return False
