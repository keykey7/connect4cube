import logging
from queue import Empty

from connect4cube.connect4 import EMPTY
from connect4cube.connect4.player import BasePlayer
from connect4cube.hardware.button_events import ButtonEvents

LOG = logging.getLogger(__name__)


class GpioPlayer(BasePlayer):
    """
    A binary-joystick controlled player using RasPi GPIOs
    https://gpiozero.readthedocs.io/en/stable/
    """
    def __init__(self, viewer):
        BasePlayer.__init__(self, viewer)
        self.button_events = ButtonEvents()
        self.selected = (2, 2)
        # short timeout after a game starts, it is increased on the first input
        self.timeout = 30
        self.return_position = (None, None)

    def axis_pressed(self, dx, dy):
        LOG.debug("axis button pressed: {} {}".format(dx, dy))
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
        if self.board.field(*self.selected, 4) != EMPTY:
            LOG.debug("non playable location, ignoring")
            return
        self.return_position = self.selected

    def undo_pressed(self):
        LOG.debug("undo button pressed")
        self.return_position = (-1, -1)

    @staticmethod
    def reset_pressed():
        LOG.debug("reset button pressed")
        raise PlayerResetError()

    def do_play(self) -> tuple:
        if self.selected == (-1, -1):
            self.selected = (2, 2)
        self.do_select(*self.selected)  # first show the last selected location
        # consume all events which are still in the queue
        try:
            while self.button_events.event_queue.get(block=False):
                self.button_events.event_queue.task_done()
        except Empty:
            pass
        self.return_position = (None, None)
        event_functions = {
            self.button_events.Event.UP_PRESSED: lambda: self.axis_pressed(-1, 0),
            self.button_events.Event.UP_REPEATED: lambda: self.axis_pressed(-1, 0),
            self.button_events.Event.DOWN_PRESSED: lambda: self.axis_pressed(1, 0),
            self.button_events.Event.DOWN_REPEATED: lambda: self.axis_pressed(1, 0),
            self.button_events.Event.LEFT_PRESSED: lambda: self.axis_pressed(0, -1),
            self.button_events.Event.LEFT_REPEATED: lambda: self.axis_pressed(0, -1),
            self.button_events.Event.RIGHT_PRESSED: lambda: self.axis_pressed(0, 1),
            self.button_events.Event.RIGHT_REPEATED: lambda: self.axis_pressed(0, 1),
            self.button_events.Event.A_PRESSED: self.drop_pressed,
            self.button_events.Event.A_REPEATED: None,
            self.button_events.Event.B_PRESSED: self.undo_pressed,
            self.button_events.Event.B_REPEATED: self.reset_pressed,
        }
        while self.return_position is (None, None):
            try:
                event = self.button_events.event_queue.get(timeout=self.timeout)
                self.button_events.event_queue.task_done()
                event_function = event_functions[event]
                if event_function is not None:
                    event_functions[event]()
            except Empty:
                raise PlayerTimeoutError()
            # increase timeout after first event
            self.timeout = 200
        return self.return_position


class PlayerTimeoutError(TimeoutError):
    pass


class PlayerResetError(InterruptedError):
    pass
