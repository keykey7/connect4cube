import sys
from random import Random
from time import sleep

from connect4cube.board import Board
from connect4cube import EMPTY


class Player:
    def play(self, other_x, other_y) -> tuple:
        """
        :param other_x: x-coordinate of the previous opponents move or None
        :param other_y: see x
        :return: a tuple (x, y) of the location to play to
        """
        raise NotImplementedError


class BasePlayer(Player):
    """ Abstract player backed by a simple board """
    def __init__(self, board_viewer=None):
        self.board = Board()
        self.board_viewer = board_viewer

    def play(self, other_x, other_y) -> tuple:
        assert self.board.round < 5 * 5 * 5
        if other_x is not None:
            self.board.move(other_x, other_y)
        (x, y) = self.do_play()
        self.board.move(x, y)
        return x, y

    def do_select(self, x, y):
        if self.board_viewer is None:
            return
        self.board_viewer.player_selects(x, y)

    def do_play(self) -> tuple:
        raise NotImplementedError


class RandomPlayer(BasePlayer):
    def __init__(self, seed=None, sleep_sec=0):
        super().__init__()
        self.rand = Random(seed)
        self.sleep_sec = sleep_sec

    def do_play(self) -> tuple:
        while True:
            # yeah, alternatively we could collect all valid moves and then pick a random one
            x = self.rand.randint(0, 4)
            y = self.rand.randint(0, 4)
            if self.board.field(x, y, 4) == EMPTY:
                sleep(self.sleep_sec/2)
                self.do_select(x, y)
                sleep(self.sleep_sec/2)
                return x, y


class StdinPlayer(BasePlayer):
    def do_play(self) -> tuple:
        switcher = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, '0': 0, '1': 1, '2': 2, '3': 3, '4': 4}
        while True:
            s = input("move> ").lower()
            if len(s) != 2:
                sys.stderr.write("expected 2 digits, like 'A0', retry\n")
                continue
            x = switcher.get(s[0], -1)
            y = switcher.get(s[1], -1)
            if x < 0 or y < 0:
                sys.stderr.write("invalid digit, try something like 'A0', retry\n")
                continue
            if self.board.field(x, y, 4) != EMPTY:
                sys.stderr.write("invalid move, column is already full, retry\n")
                continue
            return x, y
