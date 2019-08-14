from vpython import sphere, vector, canvas, color

from connect4cube.board import Board
from connect4cube.viewer_led import LedViewer


class VPythonViewer(LedViewer):
    """
    A Mockup class for local pingping LED debugging
    """
    no_color = color.gray(0.5)

    def __init__(self, board):
        super().__init__(board, pixel_count=0)
        c = canvas()
        self.pixels = [None] * 125
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    pxid = self.xyz2pxid(x, y, z)
                    led = sphere(canvas=c,
                                 pos=vector(x - 2, z - 2, y - 2),
                                 radius=0.33,
                                 color=self.no_color)
                    # noinspection PyTypeChecker
                    self.pixels[pxid] = led

    def xyz2pxid(self, x, y, z) -> int:
        return x + y * 5 + z * 25

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        self.pixels[pxid].color = vector(r, g, b) / 2 + self.no_color

    def show(self):
        pass


if __name__ == "__main__":
    testboard = Board()
    testboard.move(1, 2)
    testboard.move(1, 2)
    testboard.move(1, 2)
    testboard.move(1, 3)
    testboard.move(3, 3)
    testboard.move(3, 3)
    testboard.move(1, 0)
    testboard.move(0, 0)
    testboard.move(1, 0)
    VPythonViewer(testboard).draw()
