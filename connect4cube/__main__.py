import logging
import sys

from connect4cube.game import Game
from connect4cube.player import StdinPlayer, RandomPlayer

logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))

if __name__ == "__main__":
    Game(RandomPlayer(), StdinPlayer()).play()
