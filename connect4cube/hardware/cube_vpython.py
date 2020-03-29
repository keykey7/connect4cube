import logging
from time import sleep

from gpiozero import Device
from vpython import sphere, vector, canvas, color

LOG = logging.getLogger(__name__)


class VPythonCube:
    """
    A Mockup class for local pingpong LED debugging
    """
    no_color = color.white * 0.2

    def __init__(self):
        self.canvas = canvas(width=1900, height=900)
        self.pixels = [None] * 125
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    pxid = self.xyz2pxid(x, y, z)
                    led = sphere(canvas=self.canvas,
                                 pos=vector(y - 2, z - 2, x - 2),
                                 radius=0.2,  # pingpong ball diameter is 40mm, distance between 'em 100mm
                                 color=self.no_color,
                                 emissive=True)
                    # noinspection PyTypeChecker
                    self.pixels[pxid] = led
        self.canvas.camera.rotate(angle=0.1, axis=vector(1, 1, 0), origin=self.canvas.center)
        self.canvas.center = vector(0, 0, 0)
        self.canvas.bind("keydown", handle_mock_gpio)  # handle keypresses

    def xyz2pxid(self, x, y, z) -> int:
        return x + y * 5 + z * 25

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        self.pixels[pxid].color = vector(r / 256.0, g / 256.0, b / 256.0) * 0.8 + self.no_color

    def show(self):
        pass


def handle_mock_gpio(event):
    SHORT = 0
    LONG = 1
    LOG.debug("keydown {}".format(event.key))
    pin = {
        "up": (19, SHORT),
        "down": (26, SHORT),
        "left": (6, SHORT),
        "right": (13, SHORT),
        " ": (12, SHORT),
        "\n": (12, SHORT),
        "r": (16, SHORT),
        "R": (16, LONG)
    }.get(event.key, (0, 0))
    if pin != (0, 0):
        pin_dev = Device.pin_factory.pin(pin[0])
        pin_dev.drive_low()
        if pin[1] == SHORT:
            sleep(0.1)
        else:
            sleep(1)
        pin_dev.drive_high()
