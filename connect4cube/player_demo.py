import logging
import random
from time import sleep

from connect4cube import EMPTY
from connect4cube.player_gpio import GpioPlayer


LOG = logging.getLogger(__name__)


class DemoInterrupted(RuntimeError):
    pass


class DemoPlayer(GpioPlayer):
    def sleep_or_die(self):
        if self.clicked:
            raise DemoInterrupted()
        sleep(0.2)

    def do_play(self) -> tuple:
        valid_moves = []
        for x in range(5):
            for y in range(5):
                if self.board.field(x, y, 4) == EMPTY:
                    valid_moves.append((x, y))
        x, y = random.choice(valid_moves)
        sx, sy = self.selected
        while sx != x:
            sx += 1 if x > sx else -1
            self.sleep_or_die()
            self.do_select(sx, sy)
        while sy != y:
            sy += 1 if y > sy else -1
            self.sleep_or_die()
            self.do_select(sx, sy)
        self.selected = (sx, sy)
        self.sleep_or_die()
        return x, y

    def axis_pressed(self, dx, dy):
        self.button_pressed()

    def button_pressed(self):
        with self.lock:
            LOG.debug("GPIO button pressed, interrupting demo")
            self.clicked = True
