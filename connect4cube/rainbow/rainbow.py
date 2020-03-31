import logging
from connect4cube.app import App
from connect4cube.hardware.button_events import ButtonEvents
from connect4cube.hardware.cube import Cube
from connect4cube.hardware.util import is_a_raspberry
from connect4cube.util.color import wheel

if not is_a_raspberry():
    from time import sleep

LOG = logging.getLogger(__name__)


class Rainbow(App):
    def __init__(self):
        self.button_events = ButtonEvents()
        self.cube = Cube()
        self.cube_buffer = self.cube.get_empty_cube_buffer()

    def rainbow_cycle(self):
        for i in range(255):
            for y in range(5):
                for x in range(5):
                    color = wheel((y * 50 + x * 10 + i) % 255)
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
