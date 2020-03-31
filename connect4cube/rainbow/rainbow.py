import logging
from connect4cube.app import App
from connect4cube.hardware.button_events import ButtonEvents
from connect4cube.hardware.cube import Cube, get_empty_cube_buffer
from connect4cube.hardware.util import is_a_raspberry
from connect4cube.util.color import wheel

if not is_a_raspberry():
    from time import sleep

LOG = logging.getLogger(__name__)


class Rainbow(App):
    def __init__(self):
        self.button_events = ButtonEvents()
        self.cube = Cube()
        self.cube_buffer = get_empty_cube_buffer()

    def run(self):
        wheel_pos = 0
        try:
            while True:
                if self.button_events.get_event(block=False):
                    LOG.debug("button pressed, interrupting rainbow")
                    raise RainbowInterrupted()
                rainbow(self.cube_buffer, wheel_pos)
                self.cube.draw(self.cube_buffer)
                self.cube.show()
                wheel_pos = (wheel_pos + 1) % 255
                if not is_a_raspberry():
                    sleep(0.02)
        except RainbowInterrupted:
            return

    def get_preview(self):
        preview = get_empty_cube_buffer()
        rainbow(preview, 0)
        return preview

    def get_description(self) -> str:
        return "rainbow"


class RainbowInterrupted(RuntimeError):
    pass


def rainbow(cube_buffer, wheel_pos):
    for y in range(5):
        for x in range(5):
            color = wheel((y * 50 + x * 10 + wheel_pos) % 255)
            for z in range(5):
                cube_buffer[x][y][z] = color
