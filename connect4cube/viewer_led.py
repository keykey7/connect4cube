import Adafruit_WS2801

from connect4cube import RED, BLUE, EMPTY
from connect4cube.viewer import BoardViewer


class LedViewer(BoardViewer):
    def __init__(self, board, pixel_count=125, pixel_clock=18, pixel_dout=23):
        """
        :param board:
        :param pixel_count: amount of pixels
        :param pixel_clock: The WS2801 library makes use of the BCM pin numbering scheme.
            Specify a software SPI connection for Raspberry Pi
        :param pixel_dout: see above
        """
        super().__init__(board)
        self.pixels = Adafruit_WS2801.WS2801Pixels(pixel_count, clk=pixel_clock, do=pixel_dout) if pixel_count > 0 \
            else None

    def xyz2pxid(self, x, y, z) -> int:
        raise NotImplementedError("actual mapping to be implemented")

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        color = Adafruit_WS2801.RGB_to_color(r, g, b)
        self.pixels.set_pixel(pxid, color)

    def show(self):
        self.pixels.show()

    def paint(self):
        self.set_board_colors()
        self.show()

    def player_plays(self, x, y):
        # TODO: obviously we want an animation here :)
        self.set_board_colors()
        z = 4
        while z >= 0 and self.board.field(x, y, z) == EMPTY:
            z -= 1
        value = self.board.field(x, y, z)
        if value == RED:
            color = (255, 0, 0)
        elif value == BLUE:
            color = (0, 0, 255)
        else:
            raise AssertionError()
        self.set_color(x, y, z, *color)
        self.show()

    def player_selects(self, x, y):
        self.set_board_colors()
        if self.board.field(x, y, 4) != EMPTY:
            # unplayable
            self.set_color(x, y, 4, 0, 50, 0)
        else:
            z = 4
            while z >= 0 and self.board.field(x, y, z) == EMPTY:
                self.set_color(x, y, z, 0, 155, 0)
                z -= 1
            z += 1
            self.set_color(x, y, z, 0, 255, 0)
        self.show()

    def set_board_colors(self):
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    value = self.board.field(x, y, z)
                    if value == RED:
                        color = (150, 0, 0)
                    elif value == BLUE:
                        color = (0, 0, 150)
                    else:
                        color = (0, 0, 0)
                    self.set_color(x, y, z, *color)
