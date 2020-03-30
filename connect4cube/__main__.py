import logging
import sys

from connect4cube.connect4.ai.player_ai_demo import AiDemoPlayer
from connect4cube.connect4.game import Game
from connect4cube.connect4.player_demo import DemoInterrupted
from connect4cube.connect4.player_gpio import GpioPlayer, PlayerTimeoutError, PlayerResetError  # noqa: E402
from connect4cube.connect4.viewer_led import LedViewer, CYCLE, RAINBOW
from connect4cube.hardware.util import is_a_raspberry

LOG = logging.getLogger(__name__)
LOG.debug("sys.path=" + ":".join(sys.path))


def human_player():
    stopped = False
    while not stopped:
        viewer = LedViewer(mode=CYCLE)
        player = GpioPlayer(viewer)
        player.play_both_sides = True
        try:
            Game(player, player, viewer).play()
        except PlayerTimeoutError:
            viewer.finish([])
            LOG.warning("player idle for too long")
            stopped = True
        except PlayerResetError:
            viewer.finish([])
            LOG.debug("reset game")
        player.close()
        viewer.close()


def demo_player():
    stopped = False
    while not stopped:
        viewer = LedViewer(mode=RAINBOW)
        player = AiDemoPlayer(viewer)
        player.play_both_sides = True
        try:
            Game(player, player, viewer).play()
        except DemoInterrupted:
            stopped = True
        player.close()
        viewer.close()


if __name__ == "__main__":
    while True:
        demo_player()
        human_player()
