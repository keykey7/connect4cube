import Adafruit_WS2801

from connect4cube import RED, BLUE
from connect4cube.viewer import BoardViewer


class LedViewer(BoardViewer):
    def __init__(self, board, pixel_count=125, pixel_clock=18, pixel_dout=23):
        """
        :param board:
        :param pixel_count: amount of pixels
        :param pixel_clock: The WS2801 library makes use of the BCM pin numbering scheme. Specify a software SPI connection for Raspberry Pi
        :param pixel_dout: see above
        """
        super().__init__(board)
        self.pixels = Adafruit_WS2801.WS2801Pixels(pixel_count, clk=pixel_clock, do=pixel_dout)

    def xyz2pxid(self, x, y, z) -> int:
        raise NotImplementedError("actual mapping to be implemented")

    def draw(self):
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    pxid = self.xyz2pxid(x, y, z)
                    value = self.board.field(x, y, z)
                    if value == RED:
                        color = Adafruit_WS2801.RGB_to_color(255, 0, 0)
                    elif value == BLUE:
                        color = Adafruit_WS2801.RGB_to_color(0, 0, 255)
                    else:
                        color = 0
                    self.pixels.set_pixel(pxid, color)
        self.pixels.show()
