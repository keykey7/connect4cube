from connect4cube import RED, BLUE, EMPTY


class BoardViewer:
    def __init__(self, board):
        self.board = board

    def draw(self):
        raise NotImplementedError

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

    def draw_str(self):
        if self.ansi:
            header = "  y →         z↑1         z↑2         z↑3          🤔{} #{}\n"
            switcher = {
                RED: '\033[31m' + "○ " + '\033[30m',
                BLUE: '\033[34m' + "● " + '\033[30m',
                EMPTY: '\033[37m' + "· " + '\033[30m'
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
                    s += switcher.get(v, "{}?".format(v))
            s += "\n"
        return s

    def draw(self):
        print(self.draw_str())
