from connect4cube import RED, BLUE, EMPTY


class BoardViewer:
    def __init__(self, board):
        self.board = board

    def draw(self):
        pass

    def player_plays(self, x, y):
        self.draw()

    def player_selects(self, x, y):
        self.draw()

    def finish(self, winning_coords):
        self.draw()


class StdoutViewer(BoardViewer):
    def __init__(self, board, ansi=True):
        super().__init__(board)
        self.ansi = ansi

    def draw_str(self, select_coords=None):
        if self.ansi:
            header = "  y →         z↑1         z↑2         z↑3          🤔{} #{}\n"
            switcher = {
                RED: '\033[31m○\033[39m ',
                BLUE: '\033[34m●\033[39m ',
                EMPTY: '\033[37m·\033[39m '
            }
        else:
            header = "  Y->         Z1          Z2          Z3            !{} #{}\n"
            switcher = {
                RED: "x ",
                BLUE: "o ",
                EMPTY: ". "
            }
        s = header.format(switcher.get(self.board.next_color), self.board.round)
        for x in range(5):
            for z in range(5):
                if z == 0 and x == 0:
                    s += "X "
                elif z == 0 and x == 1 and self.ansi:
                    s += "↓ "
                else:
                    s += "  "
                for y in range(5):
                    v = self.board.field(x, y, z)
                    vs = switcher.get(v, "{}?".format(v))
                    if select_coords is not None and [x, y, z] in select_coords:
                        s = s[:-1]  # need the previous space
                        if self.ansi:
                            vs = '\033[47m ' + vs + '\033[49m'
                        else:
                            vs = "[" + vs[0] + "]"
                    s += vs
            s += "\n"
        return s

    def draw(self):
        print(self.draw_str())

    def player_plays(self, x, y):
        z = 4
        while z >= 0 and self.board.field(x, y, z) == EMPTY:
            z -= 1
        print(self.draw_str([[x, y, z]]))

    def finish(self, winning_coords):
        print(self.draw_str(winning_coords))
