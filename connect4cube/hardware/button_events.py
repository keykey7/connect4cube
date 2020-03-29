import logging
from time import time
from queue import Queue
from threading import Lock
from enum import Enum, auto

from gpiozero import Button

LOG = logging.getLogger(__name__)
DEBOUNCE_TIME = 0.1


class ButtonEvents:
    """
    Singleton class for button events, because the hardware can only be accessed by one.
    """
    instance = None

    class __ButtonEvents:
        def __init__(self, axis_up=19, axis_down=26, axis_left=6, axis_right=13, button_a=12, button_b=16):
            """
            all pin numbers in BMC, see https://pinout.xyz/
            """
            pin2fn = {
                axis_up: (
                    lambda: self.button_pressed(self.Event.UP_PRESSED),
                    lambda: self.button_repeated(self.Event.UP_REPEATED)
                ),
                axis_down: (
                    lambda: self.button_pressed(self.Event.DOWN_PRESSED),
                    lambda: self.button_repeated(self.Event.DOWN_REPEATED)
                ),
                axis_left: (
                    lambda: self.button_pressed(self.Event.LEFT_PRESSED),
                    lambda: self.button_repeated(self.Event.LEFT_REPEATED)
                ),
                axis_right: (
                    lambda: self.button_pressed(self.Event.RIGHT_PRESSED),
                    lambda: self.button_repeated(self.Event.RIGHT_REPEATED)
                ),
                button_a: (
                    lambda: self.button_pressed(self.Event.A_PRESSED),
                    lambda: self.button_repeated(self.Event.A_REPEATED)
                ),
                button_b: (
                    lambda: self.button_pressed(self.Event.B_PRESSED),
                    lambda: self.button_repeated(self.Event.B_REPEATED)
                ),
            }
            self.buttons = []
            for pin, fns in pin2fn.items():
                button = Button(pin, hold_repeat=True, hold_time=1)
                button.when_pressed = fns[0]
                button.when_held = fns[1]
                self.buttons.append(button)

            # up/down and left/right are combined for debouncing
            # if the joystick is released it tends to jump back activate the reversed direction
            self.last_up_down_time = self.LastEventTime()
            self.last_left_right_time = self.LastEventTime()
            self.last_a_time = self.LastEventTime()
            self.last_b_time = self.LastEventTime()
            self.last_event_times = {
                self.Event.UP_PRESSED: self.last_up_down_time,
                self.Event.DOWN_PRESSED: self.last_up_down_time,
                self.Event.LEFT_PRESSED: self.last_left_right_time,
                self.Event.RIGHT_PRESSED: self.last_left_right_time,
                self.Event.A_PRESSED: self.last_a_time,
                self.Event.B_PRESSED: self.last_b_time,

            }

            self.lock = Lock()
            self.event_queue = Queue()

        def button_pressed(self, event):
            LOG.debug("button event: {}".format(event))
            with self.lock:
                if time() - self.last_event_times[event].last_event_time < DEBOUNCE_TIME:
                    LOG.debug("debounce: ignoring input")
                    return
            self.last_event_times[event].last_event_time = time()
            self.event_queue.put(event)

        def button_repeated(self, event):
            LOG.debug("button event: {}".format(event))
            self.event_queue.put(event)

        def close(self):
            # close any GPIO ports or creating a new instance will fail until the garbage collector runs
            for button in self.buttons:
                button.close()

        class Event(Enum):
            """
            Button event identifiers to send via a queue to consumers.
            """
            UP_PRESSED = auto()
            DOWN_PRESSED = auto()
            LEFT_PRESSED = auto()
            RIGHT_PRESSED = auto()
            A_PRESSED = auto()
            B_PRESSED = auto()
            UP_REPEATED = auto()
            DOWN_REPEATED = auto()
            LEFT_REPEATED = auto()
            RIGHT_REPEATED = auto()
            A_REPEATED = auto()
            B_REPEATED = auto()

        class LastEventTime:
            """
            Class to store the last event time.
            Separate class so it can be used in a dictionary with multiple keys.
            """
            def __init__(self, last_event_time=0):
                self.last_event_time = last_event_time

    def __init__(self):
        if not ButtonEvents.instance:
            ButtonEvents.instance = ButtonEvents.__ButtonEvents()

    def __getattr__(self, name):
        return getattr(self.instance, name)
