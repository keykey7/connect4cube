import typing
from random import randint, Random, random

from connect4cube.simple_board import Board, EMPTY


class Player:
    def play(self, other_x, other_y) -> tuple:
        raise NotImplementedError


class BasePlayer(Player):
    def __init__(self):
        self.board = Board()

    def play(self, other_x, other_y) -> tuple:
        assert self.board.round < 5 * 5 * 5
        if other_x is not None:
            self.board.move(other_x, other_y)
        (x, y) = self.do_play()
        self.board.move(x, y)
        return x, y

    def do_play(self) -> tuple:
        raise NotImplementedError


class RandomPlayer(BasePlayer):
    def __init__(self, seed=None):
        super().__init__()
        self.rand = Random(seed)

    def do_play(self) -> tuple:
        while True:
            x = self.rand.randint(0, 4)
            y = self.rand.randint(0, 4)
            if self.board.field(x, y, 4) == EMPTY:
                return x, y
