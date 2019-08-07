import typing
from enum import Enum

from connect4cube.simple_board import POS_DIRECTIONS, Board, EMPTY


MAX_ROUND = 5*5*5 - 1


class Winner(Enum):
    RED = 0
    BLUE = 1
    DRAW = 2


class RuleViolation(Exception):
    pass


class Player:
    def __init__(self, board: Board):
        self.board = board

    def play(self, other_move: typing.Optional[tuple]) -> tuple:
        raise NotImplementedError


class Game:
    def __init__(self, player_red: Player, player_blue: Player):
        self.player_red = player_red
        self.player_blue = player_blue
        self.current = player_red

    def play(self) -> Winner:
        board = Board()
        last_move = None
        while board.round <= MAX_ROUND:
            move = self.current.play(last_move)
            if 0 > move[0] > 4 or 0 > move[1] > 4:
                raise RuleViolation("out of bounds move")
            if board.field(move[0], move[1], 4) != EMPTY:
                raise RuleViolation("already full at {},{}".format(move))
            is_winning = board.move(move)
            if is_winning:
                return Winner.RED if self.current is self.player_red else Winner.BLUE
            self.current = self.player_red if self.current is self.player_blue else self.player_red
        return Winner.DRAW
