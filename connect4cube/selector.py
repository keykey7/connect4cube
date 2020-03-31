import logging

from connect4cube.hardware.cube import Cube
from connect4cube.connect4.connect4 import Connect4Demo, Connect4Human
from connect4cube.rainbow.rainbow import Rainbow
from connect4cube.hardware.button_events import ButtonEvents

LOG = logging.getLogger(__name__)


class Selector:
    def __init__(self):
        self.cube = Cube()
        self.button_events = ButtonEvents()
        self.apps = [Rainbow(), Connect4Demo(), Connect4Human()]
        self.selected = 0
        self.show_preview()

    def run(self):
        event = self.button_events.get_event()
        if event == self.button_events.Event.UP_PRESSED or event == self.button_events.Event.LEFT_PRESSED:
            self.selected = (self.selected - 1) % len(self.apps)
            self.show_preview()
        elif event == self.button_events.Event.DOWN_PRESSED or event == self.button_events.Event.RIGHT_PRESSED:
            self.selected = (self.selected + 1) % len(self.apps)
            self.show_preview()
        elif event == self.button_events.Event.A_PRESSED:
            self.apps[self.selected].run()
            self.show_preview()

    def show_preview(self):
        preview = self.apps[self.selected].get_preview()
        self.cube.draw(preview)
        self.cube.show()
