import logging
from itertools import product

RED = 0
BLUE = 1
EMPTY = 2
POS_DIRECTIONS = list(product([0, 1], repeat=3))
POS_DIRECTIONS.pop(0)  # (0,0,0) isn't a valid move direction


class Board:
    LOG = logging.getLogger(__name__)

    def __init__(self):
        self.cube = [[[EMPTY for z in range(5)] for y in range(5)] for x in range(5)]
        self.next_color = RED
        self.round = 0

    def __str__(self):
        switcher = {
            RED: '\033[31m' + "○ " + '\033[30m',
            BLUE: '\033[34m' + "● " + '\033[30m',
            EMPTY: '\033[37m' + "· " + '\033[30m'
        }
        s = "  y →         z↑1         z↑2         z↑3          🤔{} #{}\n"\
            .format(switcher.get(self.next_color), self.round)
        for x in range(5):
            for z in range(5):
                if z == 0 and x == 0:
                    s += "x "
                elif z == 0 and x == 1:
                    s += "↓ "
                else:
                    s += "  "
                for y in range(5):
                    v = self.cube[x][y][z]
                    s += switcher.get(v, "{}?".format(v))
            s += "\n"
        return s

    def move(self, x, y) -> bool:
        assert 0 <= x < 5 and 0 <= y < 5
        z = 0
        while z < 5 and self.cube[x][y][z] != EMPTY:
            z += 1
        assert z < 5
        current = self.next_color
        self.cube[x][y][z] = current
        self.next_color = RED if self.next_color == BLUE else BLUE
        self.round += 1
        return self.is_winning(x, y, z, current)

    def field(self, x, y, z):
        assert 0 <= x < 5 and 0 <= y < 5 and 0 <= z < 5
        return self.cube[x][y][z]

    def is_winning(self, x0, y0, z0, color) -> bool:
        for d in POS_DIRECTIONS:
            (x, y, z) = (x0, y0, z0)
            i = 0
            for i in range(3):
                (x, y, z) = (x + d[0], y + d[1], z + d[2])
                if x >= 5 or y >= 5 or z >= 5:
                    break
                if color != self.cube[x][y][z]:
                    break
                if i == 2:
                    return True
            (x, y, z) = (x0, y0, z0)
            for i in range(i, 3):
                (x, y, z) = (x - d[0], y - d[1], z - d[2])
                if 0 > x or 0 > y or 0 > z:
                    break
                if color != self.cube[x][y][z]:
                    break
                if i == 2:
                    return True
        return False
