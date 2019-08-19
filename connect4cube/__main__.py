import logging
import sys

from connect4cube.game import Game
from connect4cube.viewer_led import LedViewer
from connect4cube.util import is_a_raspberry



logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))

if is_a_raspberry():
    from connect4cube.player_gpio import GpioPlayer
    player = GpioPlayer()
    player.play_both_sides = True
    Game(player, player, viewer=LedViewer).play()
else:
    from connect4cube.player import RandomPlayer, StdinPlayer
    if len(sys.argv) == 2 and sys.argv[1] == '--vpython':
        Game(RandomPlayer(), StdinPlayer(), viewer=LedViewer).play()
    else:
        Game(RandomPlayer(), StdinPlayer()).play()

if __name__ == "__main__":
    pass  # only here for the play button
