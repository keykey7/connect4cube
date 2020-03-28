import logging
from time import sleep, time
from threading import Lock

from gpiozero import Button

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.player import BasePlayer

LOG = logging.getLogger(__name__)
DEBOUNCE_TIME = 0.2


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://gpiozero.readthedocs.io/en/stable/
    """
    def __init__(self, viewer, north=19, east=13, south=26, west=6, drop=12, reset=16):
        """
        all pin numbers in BMC, see https://pinout.xyz/
        """
        super().__init__(viewer)
        pin2fn = {
            north: (lambda: self.axis_pressed(-1, 0),) * 2,
            east: (lambda: self.axis_pressed(0, 1),) * 2,
            south: (lambda: self.axis_pressed(1, 0),) * 2,
            west: (lambda: self.axis_pressed(0, -1),) * 2,
            drop: (self.drop_pressed, None),
            reset: (self.undo_pressed, self.reset_pressed)
        }
        self.buttons = []
        for pin, fns in pin2fn.items():
            button = Button(pin, hold_repeat=True, hold_time=0.4)
            button.when_pressed = fns[0]
            if fns[1] is not None:
                button.when_held = fns[1]
            self.buttons.append(button)
        self.drop_clicked = False
        self.reset_clicked = False
        self.undo_clicked = False
        self.selected = (2, 2)
        self.lock = Lock()
        self.last_interaction = 0
        self.last_axis_time = 0
        self.last_drop_time = 0
        self.last_undo_time = 0
        self.last_direction = (0, 0)
        # short timeout after a game starts, it is increased on the first input
        self.timeout = 30

    def axis_pressed(self, dx, dy):
        with self.lock:
            if time() - self.last_axis_time < DEBOUNCE_TIME and (-dx, -dy) == self.last_direction:
                LOG.debug("debounce: ignoring input")
                return
            self.timeout = 200
            self.last_interacted = self.last_axis_time = time()
            self.last_direction = (dx, dy)
            x, y = self.selected
            x += dx
            y += dy
            if not (0 <= x < 5 and 0 <= y < 5):
                LOG.debug("out of bounds: ignoring {},{}".format(x, y))
                return
            if self.drop_clicked:
                LOG.debug("too late: ignoring {},{}".format(x, y))
                return
            self.selected = (x, y)
            LOG.debug("GPIO selected {},{}".format(x, y))
            self.do_select(x, y)

    def drop_pressed(self):
        with self.lock:
            if time() - self.last_drop_time < DEBOUNCE_TIME:
                LOG.debug("debounce: ignoring input")
                return
            self.timeout = 200
            self.last_interacted = self.last_drop_time = time()
            LOG.debug("GPIO drop button pressed")
            if self.board.field(*self.selected, 4) != EMPTY:
                LOG.debug("non playable location, ignoring")
                return
            self.drop_clicked = True

    def undo_pressed(self):
        with self.lock:
            if time() - self.last_undo_time < DEBOUNCE_TIME:
                LOG.debug("debounce: ignoring input")
                return
            self.timeout = 200
            self.last_interacted = self.last_undo_time = time()
            LOG.debug("GPIO undo button pressed")
            self.undo_clicked = True

    def reset_pressed(self):
        with self.lock:
            if time() - self.last_interaction < DEBOUNCE_TIME:
                LOG.debug("debounce: ignoring input")
                return
            LOG.debug("GPIO reset button pressed")
            self.reset_clicked = True

    def do_play(self) -> tuple:
        self.drop_clicked = False
        self.undo_clicked = False
        if self.selected == (-1, -1):
            self.selected = (2, 2)
        with self.lock:
            self.do_select(*self.selected)  # first show the last selected location
        self.last_interaction = self.last_axis_time = self.last_drop_time = self.last_undo_time = time()
        while not self.drop_clicked and not self.reset_clicked and not self.undo_clicked:
            if time() - self.last_interaction > self.timeout:
                raise PlayerTimeoutError()
            sleep(0.1)  # TODO: preferably an interrupt instead of polling here
        if self.undo_clicked:
            return (-1, -1)
        if self.reset_clicked:
            raise PlayerResetError()
        return self.selected

    def close(self):
        # close any GPIO ports or creating a new player instance will fail until the garbage collector runs
        for button in self.buttons:
            button.close()


class PlayerTimeoutError(TimeoutError):
    pass


class PlayerResetError(InterruptedError):
    pass
