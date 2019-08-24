import logging
import sys

from connect4cube.ai.player_ai_demo import AiDemoPlayer
from connect4cube.game import Game
from connect4cube.player_demo import DemoInterrupted
from connect4cube.util import is_a_raspberry
from connect4cube.viewer_led import LedViewer, CYCLE, RAINBOW

LOG = logging.getLogger(__name__)
LOG.debug("sys.path=" + ":".join(sys.path))

if not is_a_raspberry():
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device

    Device.pin_factory = MockFactory()

# must come AFTER mocking gpio pins
from connect4cube.player_gpio import GpioPlayer, PlayerTimeoutError, PlayerResetError  # noqa: E402


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
