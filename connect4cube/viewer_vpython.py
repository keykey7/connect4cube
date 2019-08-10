from vpython import sphere, vector, color

from connect4cube.board import Board
from connect4cube import RED, BLUE
from connect4cube.viewer import BoardViewer


class VPythonViewer(BoardViewer):
    def draw(self):
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    v = self.board.field(x, y, z)
                    c = color.white
                    r = 0.05
                    if v == RED:
                        c = color.red
                        r = 0.45
                    elif v == BLUE:
                        c = color.blue
                        r = 0.45
                    sphere(pos=vector(x - 2, z - 2, y - 2), radius=r, color=c, opacity=0.8)


if __name__ == "__main__":
    board = Board()
    board.move(1, 2)
    board.move(1, 2)
    board.move(1, 2)
    board.move(1, 3)
    board.move(3, 3)
    board.move(3, 3)
    board.move(1, 0)
    board.move(0, 0)
    board.move(1, 0)
    VPythonViewer(board).draw()
