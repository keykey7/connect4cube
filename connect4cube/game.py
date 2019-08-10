from enum import Enum

from connect4cube.player import Player, RandomPlayer, StdinPlayer
from connect4cube.board import Board
from connect4cube import EMPTY, RED, BLUE
from connect4cube.viewer import StdoutViewer

MAX_ROUND = 5*5*5 - 1


class RuleViolation(Exception):
    pass


class Game:
    def __init__(self, player_red: Player, player_blue: Player):
        self.players = [player_red, player_blue]

    def play(self) -> int:
        board = Board()
        viewer = StdoutViewer(board)
        viewer.draw()
        last_x = None
        last_y = None
        while board.round <= MAX_ROUND:
            current_color = board.next_color
            (x, y) = self.players[current_color].play(last_x, last_y)
            if 0 > x > 4 or 0 > y > 4:
                raise RuleViolation("out of bounds move")
            if board.field(x, y, 4) != EMPTY:
                raise RuleViolation("already full at {},{}".format(x, y))
            is_winning = board.move(x, y)
            viewer.player_plays(x, y)
            if is_winning:
                viewer.finish(board.winning_coords())
                return current_color
            (last_x, last_y) = (x, y)
        return EMPTY


if __name__ == "__main__":
    Game(RandomPlayer(), StdinPlayer()).play()
