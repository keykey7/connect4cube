import logging
from connect4cube.app import App
from connect4cube.hardware.button_events import ButtonEvents
from connect4cube.hardware.cube import Cube
from connect4cube.hardware.util import is_a_raspberry

if not is_a_raspberry():
    from time import sleep

LOG = logging.getLogger(__name__)


class Rainbow(App):
    def __init__(self):
        self.button_events = ButtonEvents()
        self.cube = Cube()
        self.cube_buffer = self.cube.get_empty_cube_buffer()

    @staticmethod
    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return r, g, b

    def rainbow_cycle(self):
        for i in range(255):
            for y in range(5):
                for x in range(5):
                    color = self.wheel((y * 50 + x * 10 + i) % 255)
                    for z in range(5):
                        self.cube_buffer[x][y][z] = color
            self.cube.draw(self.cube_buffer)
            self.cube.show()
            if not is_a_raspberry():
                sleep(0.02)
            if self.button_events.get_event(0):
                LOG.debug("button pressed, interrupting rainbow")
                raise RainbowInterrupted()

    def run(self):
        try:
            while True:
                self.rainbow_cycle()
        except RainbowInterrupted:
            return

    def get_preview(self):
        preview = self.cube.get_empty_cube_buffer()
        preview[0, 0, 0] = 255, 255, 255
        return preview

    def get_description(self) -> str:
        return "rainbow"


class RainbowInterrupted(RuntimeError):
    pass
