import logging
import sys

from connect4cube.game import Game
from connect4cube.player import RandomPlayer, StdinPlayer
from connect4cube.player_gpio import GpioPlayer

logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))


def is_a_raspberry():
    try:
        import RPi.GPIO
        return True
    except (ImportError, RuntimeError):
        return False


def main():
    if is_a_raspberry():
        player1 = GpioPlayer()
        player1.play_both_sides = True
        player2 = player1
    else:
        player1 = RandomPlayer()
        player2 = StdinPlayer()
    Game(player1, player2).play()


if __name__ == "__main__":
    main()
