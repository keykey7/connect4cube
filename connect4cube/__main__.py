import logging
import sys

from connect4cube.game import Game
from connect4cube.player import RandomPlayer, StdinPlayer
from connect4cube.player_gpio import GpioPlayer

logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))


def is_a_raspberry():
    try:
        import RPi.GPIO  # noqa: F401
        return True
    except (ImportError, RuntimeError):
        return False


def main():
    if is_a_raspberry():
        player = GpioPlayer()
        # TODO: Game(player, player, viewer=LedViewer)
        Game(player, player).play()
    else:
        Game(RandomPlayer(), StdinPlayer()).play()


if __name__ == "__main__":
    main()
