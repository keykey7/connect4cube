import logging
import sys

from connect4cube.game import Game
from connect4cube.viewer_led import LedViewer
from connect4cube.util import is_a_raspberry


logger = logging.getLogger(__name__)
logger.debug("sys.path=" + ":".join(sys.path))

if not is_a_raspberry():
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device
    Device.pin_factory = MockFactory()

# must come AFTER mocking gpio pins
# noqa: E402
from connect4cube.player_gpio import GpioPlayer
viewer = LedViewer()
player1 = GpioPlayer(viewer)
player1.play_both_sides = True
player2 = player1
Game(player1, player2, viewer).play()

if __name__ == "__main__":
    pass  # only here for the play button
