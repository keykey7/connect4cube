import logging
from time import time
from queue import Queue, Empty

from gpiozero import Button

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.player import BasePlayer

LOG = logging.getLogger(__name__)
DEBOUNCE_TIME = 0.1


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://gpiozero.readthedocs.io/en/stable/
    """
    def __init__(self, viewer, up=19, right=13, down=26, left=6, drop=12, reset=16):
        """
        all pin numbers in BMC, see https://pinout.xyz/
        """
        super().__init__(viewer)
        self.queue = Queue()
        pin2fn = {
            up: (lambda: self.queue.put(lambda: self.axis_pressed(-1, 0)),) * 2,
            right: (lambda: self.queue.put(lambda: self.axis_pressed(0, 1)),) * 2,
            down: (lambda: self.queue.put(lambda: self.axis_pressed(1, 0)),) * 2,
            left: (lambda: self.queue.put(lambda: self.axis_pressed(0, -1)),) * 2,
            drop: (lambda: self.queue.put(self.drop_pressed), None),
            reset: (lambda: self.queue.put(self.undo_pressed), lambda: self.queue.put(self.reset_pressed))
        }
        self.buttons = []
        for pin, fns in pin2fn.items():
            button = Button(pin, hold_repeat=True, hold_time=0.4)
            button.when_pressed = fns[0]
            if fns[1] is not None:
                button.when_held = fns[1]
            self.buttons.append(button)
        self.selected = (2, 2)
        self.last_axis_time = 0
        self.last_drop_time = 0
        self.last_undo_time = 0
        self.last_direction = (0, 0)
        # short timeout after a game starts, it is increased on the first input
        self.timeout = 30
        self.return_position = (None, None)

    def axis_pressed(self, dx, dy):
        LOG.debug("axis button pressed: {} {}".format(dx, dy))
        if time() - self.last_axis_time < DEBOUNCE_TIME and \
                ((dx, dy) == self.last_direction or (-dx, -dy) == self.last_direction):
            LOG.debug("debounce: ignoring input")
            return
        self.last_axis_time = time()
        self.last_direction = (dx, dy)
        x, y = self.selected
        x += dx
        y += dy
        if not (0 <= x < 5 and 0 <= y < 5):
            LOG.debug("out of bounds: ignoring {},{}".format(x, y))
            return
        self.selected = (x, y)
        LOG.debug("selected {},{}".format(x, y))
        self.do_select(x, y)

    def drop_pressed(self):
        LOG.debug("drop button pressed")
        if time() - self.last_drop_time < DEBOUNCE_TIME:
            LOG.debug("debounce: ignoring input")
            return
        self.last_drop_time = time()
        if self.board.field(*self.selected, 4) != EMPTY:
            LOG.debug("non playable location, ignoring")
        self.return_position = self.selected

    def undo_pressed(self):
        LOG.debug("undo button pressed")
        if time() - self.last_undo_time < DEBOUNCE_TIME:
            LOG.debug("debounce: ignoring input")
            return
        self.last_undo_time = time()
        self.return_position = (-1, -1)

    def reset_pressed(self):
        LOG.debug("reset button pressed")
        raise PlayerResetError()

    def do_play(self) -> tuple:
        if self.selected == (-1, -1):
            self.selected = (2, 2)
        self.do_select(*self.selected)  # first show the last selected location
        # consume all events which are still in the queue
        try:
            while self.queue.get(block=False):
                self.queue.task_done()
        except Empty:
            pass
        self.return_position = (None, None)
        while self.return_position is (None, None):
            try:
                event_function = self.queue.get(timeout=self.timeout)
                self.queue.task_done()
                event_function()
            except Empty:
                raise PlayerTimeoutError()
            # increase timeout after first event
            self.timeout = 200
        return self.return_position

    def close(self):
        # close any GPIO ports or creating a new player instance will fail until the garbage collector runs
        for button in self.buttons:
            button.close()


class PlayerTimeoutError(TimeoutError):
    pass


class PlayerResetError(InterruptedError):
    pass
