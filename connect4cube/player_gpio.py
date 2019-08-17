import logging
from time import sleep

from gpiozero import Button

from connect4cube.player import BasePlayer

LOG = logging.getLogger(__name__)


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://gpiozero.readthedocs.io/en/stable/
    """
    def __init__(self, north=5, east=6, south=12, west=13, button1=16):
        """
        all pin numbers in BMC, see https://pinout.xyz/
        """
        super().__init__()
        pin2fn = {
            north: self.north,
            east: lambda: self.axis_pressed(0, 1),
            south: lambda: self.axis_pressed(-1, 0),
            west: lambda: self.axis_pressed(0, -1),
            button1: self.button_pressed
        }
        self.buttons = []
        for pin, fn in pin2fn.items():
            button = Button(pin, hold_repeat=True, hold_time=2)
            button.when_pressed = fn
            button.when_held = fn
            self.buttons.append(button)
        self.clicked = False
        self.selected = (2, 2)

    def north(self):
        self.axis_pressed(1, 0)

    def axis_pressed(self, dx, dy):
        x, y = self.selected
        x += dx
        y += dy
        if not (0 <= x < 5 and 0 <= y < 5):
            LOG.debug("out of bounds: ignoring {},{}".format(x, y))
            return
        if self.clicked:
            LOG.debug("too late: ignoring {},{}".format(x, y))
            return
        self.selected = (x, y)
        LOG.debug("GPIO selected {},{}".format(x, y))
        self.do_select(x, y)

    def button_pressed(self):
        LOG.debug("GPIO button pressed")
        self.clicked = True

    def do_play(self) -> tuple:
        self.clicked = False
        while not self.clicked:
            sleep(0.1)
        return self.selected
