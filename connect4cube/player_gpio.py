import logging
from time import sleep

from gpiozero import Button

from connect4cube import EMPTY
from connect4cube.player import BasePlayer

LOG = logging.getLogger(__name__)


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://gpiozero.readthedocs.io/en/stable/
    """
    def __init__(self, north=19, east=13, south=26, west=6, button1=12):
        """
        all pin numbers in BMC, see https://pinout.xyz/
        """
        super().__init__()
        pin2fn = {
            north: lambda: self.axis_pressed(1, 0),
            east: lambda: self.axis_pressed(0, 1),
            south: lambda: self.axis_pressed(-1, 0),
            west: lambda: self.axis_pressed(0, -1),
            button1: self.button_pressed
        }
        self.buttons = []
        for pin, fn in pin2fn.items():
            button = Button(pin, hold_repeat=True, hold_time=2)
            button.when_pressed = fn
            if pin != button1:  # button press shouldn't be repeatable, for direction repeat is ok
                button.when_held = fn
            self.buttons.append(button)
        self.clicked = False
        self.selected = (2, 2)

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
        if self.board.field(*self.selected, 4) != EMPTY:
            LOG.debug("non playable location, ignoring")
            return
        self.clicked = True

    def do_play(self) -> tuple:
        self.clicked = False
        self.do_select(*self.selected)  # first show the last selected location
        while not self.clicked:
            sleep(0.1)  # TODO: preferably an interrupt instead of polling here
        return self.selected
