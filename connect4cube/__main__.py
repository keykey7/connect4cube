import logging
import sys

from connect4cube.game import Game
from connect4cube.player_demo import DemoPlayer, DemoInterrupted
from connect4cube.viewer_led import LedViewer
from connect4cube.util import is_a_raspberry


logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))

if not is_a_raspberry():
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device
    Device.pin_factory = MockFactory()

# must come AFTER mocking gpio pins
from connect4cube.player_gpio import GpioPlayer  # noqa: E402


def human_player():
    viewer = LedViewer()
    player = GpioPlayer(viewer)
    player.play_both_sides = True
    Game(player, player, viewer).play()
    player.close()
    viewer.close()


def demo_player():
    stopped = False
    while not stopped:
        viewer = LedViewer()
        player = DemoPlayer(viewer)
        player.play_both_sides = True
        try:
            Game(player, player, viewer).play()
        except DemoInterrupted:
            stopped = True
        finally:
            player.close()
            viewer.close()


if __name__ == "__main__":
    while True:
        demo_player()
        human_player()
