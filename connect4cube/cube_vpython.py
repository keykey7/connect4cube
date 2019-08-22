import logging
from time import sleep

from gpiozero import Device
from vpython import sphere, vector, canvas, color


LOG = logging.getLogger(__name__)


class VPythonCube:
    """
    A Mockup class for local pingpong LED debugging
    """
    no_color = color.white * 0.25

    def __init__(self):
        self.canvas = canvas()
        self.pixels = [None] * 125
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    pxid = self.xyz2pxid(x, y, z)
                    led = sphere(canvas=self.canvas,
                                 pos=vector(y - 2, z - 2, x - 2),
                                 radius=0.2,  # pingpong ball diameter is 40mm, distance between 'em 100mm
                                 color=self.no_color)
                    # noinspection PyTypeChecker
                    self.pixels[pxid] = led
        self.canvas.bind("keydown", handle_mock_gpio)  # handle keypresses

    def xyz2pxid(self, x, y, z) -> int:
        return x + y * 5 + z * 25

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        self.pixels[pxid].color = vector(r / 200.0, g / 200.0, b / 200.0) * 0.75 + self.no_color

    def show(self):
        pass


def handle_mock_gpio(event):
    LOG.debug("keydown {}".format(event.key))
    pin = {
        "up": 19,
        "down": 26,
        "left": 6,
        "right": 13,
        " ": 12,
        "\n": 12,
        "r": 16
    }.get(event.key, 0)
    if pin != 0:
        pin_dev = Device.pin_factory.pin(pin)
        pin_dev.drive_low()
        sleep(0.1)
        pin_dev.drive_high()
