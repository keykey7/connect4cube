import logging
import sys

from connect4cube.game import Game
from connect4cube.player import RandomPlayer, StdinPlayer

is_a_raspberry = False
try:
    import RPi.GPIO  # noqa: F401
    is_a_raspberry = True
except (ImportError, RuntimeError):
    pass

if is_a_raspberry:
    from connect4cube.player_gpio import GpioPlayer
    from connect4cube.viewer_led import LedViewer

logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))


def main():
    if is_a_raspberry:
        player = GpioPlayer()
        player.play_both_sides = True
        Game(player, player, viewer=LedViewer).play()
    else:
        Game(RandomPlayer(), StdinPlayer()).play()


if __name__ == "__main__":
    main()
