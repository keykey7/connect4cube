import logging

from connect4cube.app import App
from connect4cube.hardware.cube import Cube
from connect4cube.connect4.ai.player_ai_demo import AiDemoPlayer
from connect4cube.connect4.game import Game
from connect4cube.connect4.player_demo import DemoInterrupted
from connect4cube.connect4.player_gpio import GpioPlayer, PlayerTimeoutError, PlayerResetError
from connect4cube.connect4.viewer_led import LedViewer, CYCLE, RAINBOW

LOG = logging.getLogger(__name__)


class Connect4Demo(App):
    def run(self):
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

    def get_preview(self):
        preview = Cube().get_empty_cube_buffer()
        preview[0, 0, 0] = 255, 0, 0
        return preview

    def get_description(self) -> str:
        return "connect4demo"


class Connect4Human(App):
    def run(self):
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

    def get_preview(self):
        preview = Cube().get_empty_cube_buffer()
        preview[0, 0, 0] = 0, 255, 0
        return preview

    def get_description(self) -> str:
        return "connect4human"
