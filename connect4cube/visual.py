

class BoardViewer:
    def __init__(self, board):
        self.board = board

    def draw(self):
        raise NotImplementedError


class AnsiStdoutViewer(BoardViewer):
    def draw(self):
        pass
