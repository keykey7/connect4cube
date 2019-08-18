import board
import neopixel

from connect4cube import RED, BLUE, EMPTY
from connect4cube.viewer import BoardViewer


class LedViewer(BoardViewer):
    def __init__(self, board, pixel_count=125, pixel_pin=board.D18):
        """
        :param board:
        :param pixel_count: amount of pixels
        :param pixel_pin: The neopixel library makes use of the BCM pin numbering scheme.
        """
        super().__init__(board)
        self.pixels = neopixel.NeoPixel(pixel_pin, pixel_count, auto_write=False, pixel_order=neopixel.GRB) \
            if pixel_count > 0 else None

    def xyz2pxid(self, x, y, z) -> int:
        transform = {
                (0, 0, 0):  20, (1, 0, 0):  19, (2, 0, 0):  10, (3, 0, 0):   9, (4, 0, 0):   0,
                (0, 1, 0):  29, (1, 1, 0):  30, (2, 1, 0):  39, (3, 1, 0):  40, (4, 1, 0):  49,
                (0, 2, 0):  70, (1, 2, 0):  69, (2, 2, 0):  60, (3, 2, 0):  59, (4, 2, 0):  50,
                (0, 3, 0):  79, (1, 3, 0):  80, (2, 3, 0):  89, (3, 3, 0):  90, (4, 3, 0):  99,
                (0, 4, 0): 120, (1, 4, 0): 119, (2, 4, 0): 110, (3, 4, 0): 109, (4, 4, 0): 100,
                (0, 0, 1):  21, (1, 0, 1):  18, (2, 0, 1):  11, (3, 0, 1):   8, (4, 0, 1):   1,
                (0, 1, 1):  28, (1, 1, 1):  31, (2, 1, 1):  38, (3, 1, 1):  41, (4, 1, 1):  48,
                (0, 2, 1):  71, (1, 2, 1):  68, (2, 2, 1):  61, (3, 2, 1):  58, (4, 2, 1):  51,
                (0, 3, 1):  78, (1, 3, 1):  81, (2, 3, 1):  88, (3, 3, 1):  91, (4, 3, 1):  98,
                (0, 4, 1): 121, (1, 4, 1): 118, (2, 4, 1): 111, (3, 4, 1): 108, (4, 4, 1): 101,
                (0, 0, 2):  22, (1, 0, 2):  17, (2, 0, 2):  12, (3, 0, 2):   7, (4, 0, 2):   2,
                (0, 1, 2):  27, (1, 1, 2):  32, (2, 1, 2):  37, (3, 1, 2):  42, (4, 1, 2):  47,
                (0, 2, 2):  72, (1, 2, 2):  67, (2, 2, 2):  62, (3, 2, 2):  57, (4, 2, 2):  52,
                (0, 3, 2):  77, (1, 3, 2):  82, (2, 3, 2):  87, (3, 3, 2):  92, (4, 3, 2):  97,
                (0, 4, 2): 122, (1, 4, 2): 117, (2, 4, 2): 112, (3, 4, 2): 107, (4, 4, 2): 102,
                (0, 0, 3):  23, (1, 0, 3):  16, (2, 0, 3):  13, (3, 0, 3):   6, (4, 0, 3):   3,
                (0, 1, 3):  26, (1, 1, 3):  33, (2, 1, 3):  36, (3, 1, 3):  43, (4, 1, 3):  46,
                (0, 2, 3):  73, (1, 2, 3):  66, (2, 2, 3):  63, (3, 2, 3):  56, (4, 2, 3):  53,
                (0, 3, 3):  76, (1, 3, 3):  83, (2, 3, 3):  86, (3, 3, 3):  93, (4, 3, 3):  96,
                (0, 4, 3): 123, (1, 4, 3): 116, (2, 4, 3): 113, (3, 4, 3): 106, (4, 4, 3): 103,
                (0, 0, 4):  24, (1, 0, 4):  15, (2, 0, 4):  14, (3, 0, 4):   5, (4, 0, 4):   4,
                (0, 1, 4):  25, (1, 1, 4):  34, (2, 1, 4):  35, (3, 1, 4):  44, (4, 1, 4):  45,
                (0, 2, 4):  74, (1, 2, 4):  65, (2, 2, 4):  64, (3, 2, 4):  55, (4, 2, 4):  54,
                (0, 3, 4):  75, (1, 3, 4):  84, (2, 3, 4):  85, (3, 3, 4):  94, (4, 3, 4):  95,
                (0, 4, 4): 124, (1, 4, 4): 115, (2, 4, 4): 114, (3, 4, 4): 105, (4, 4, 4): 104}
        return transform[x, y, z]

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        self.pixels[pxid] = (r, g, b)

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
