from enum import Enum

from connect4cube.player import Player, RandomPlayer, StdinPlayer
from connect4cube.simple_board import Board
from connect4cube import EMPTY

MAX_ROUND = 5*5*5 - 1


class Winner(Enum):
    RED = 0
    BLUE = 1
    DRAW = 2


class RuleViolation(Exception):
    pass


class Game:
    def __init__(self, player_red: Player, player_blue: Player):
        self.player_red = player_red
        self.player_blue = player_blue
        self.current = player_red

    def play(self) -> Winner:
        board = Board()
        last_x = None
        last_y = None
        while board.round <= MAX_ROUND:
            (x, y) = self.current.play(last_x, last_y)
            if 0 > x > 4 or 0 > y > 4:
                raise RuleViolation("out of bounds move")
            if board.field(x, y, 4) != EMPTY:
                raise RuleViolation("already full at {},{}".format(x, y))
            is_winning = board.move(x, y)
            if is_winning:
                return Winner.RED if self.current is self.player_red else Winner.BLUE
            self.current = self.player_red if self.current is self.player_blue else self.player_blue
            (last_x, last_y) = (x, y)
        return Winner.DRAW


if __name__ == "__main__":
    Game(RandomPlayer(), StdinPlayer()).play()
