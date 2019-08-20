from threading import Thread, Event, current_thread
from time import sleep

from connect4cube import RED, BLUE, EMPTY
from connect4cube.cube import Cube
from connect4cube.viewer import BoardViewer


class LedViewer(BoardViewer):
    def __init__(self, board):
        super().__init__(board)
        self.select_animation_thread = None
        self.cube = Cube()

    def paint(self):
        self.set_board_colors()
        self.cube.show()

    def player_plays(self, x, y):
        if self.select_animation_thread is not None:
            self.select_animation_thread.stop()
            self.select_animation_thread.join()
        z = 4
        while z >= 0 and self.board.field(x, y, z) == EMPTY:
            z -= 1
        value = self.board.field(x, y, z)
        if value == RED:
            color = (255, 0, 0)
        elif value == BLUE:
            color = (0, 0, 255)
        else:
            raise AssertionError()
        z = 4
        while self.board.field(x, y, z) != value:
            self.cube.set_color(x, y, z, *color)
            self.cube.show()
            self.cube.set_color(x, y, z, 0, 0, 0)
            sleep(0.1)
            z -= 1
        self.set_board_colors()
        self.cube.show()
        sleep(0.2)

    def player_selects(self, x, y):
        if self.select_animation_thread is not None:
            self.select_animation_thread.stop()
            self.select_animation_thread.join()
        self.set_board_colors()
        if self.board.field(x, y, 4) != EMPTY:
            # unplayable
            self.cube.set_color(x, y, 4, 0, 50, 0)
        else:
            z = 4
            while z >= 0 and self.board.field(x, y, z) == EMPTY:
                self.cube.set_color(x, y, z, 0, 155, 0)
                z -= 1
            z += 1
            self.cube.set_color(x, y, z, 0, 255, 0)
        self.cube.show()
        self.select_animation_thread = StoppableThread(target=self.select_animation, args=(x, y))
        self.select_animation_thread.daemon = True
        self.select_animation_thread.start()

    def finish(self, winning_coords):
        self.set_board_colors()
        for _ in range(5):
            for c in winning_coords:
                self.cube.set_color(*c, 0, 0, 0)
            self.cube.show()
            sleep(0.2)
            self.set_board_colors()
            self.cube.show()
            sleep(0.2)

    def set_board_colors(self):
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    value = self.board.field(x, y, z)
                    if value == RED:
                        color = (255, 0, 0)
                    elif value == BLUE:
                        color = (0, 0, 255)
                    else:
                        color = (0, 0, 0)
                    self.cube.set_color(x, y, z, *color)

    def select_animation(self, x, y):
        on = True
        delay = 0
        while not current_thread().stopped():
            if delay < 5:
                delay += 1
            else:
                delay = 0
                if on:
                    if self.board.next_color == RED:
                        color = (255, 0, 0)
                    elif self.board.next_color == BLUE:
                        color = (0, 0, 255)
                    else:
                        raise AssertionError()
                else:
                    if self.board.field(x, y, 4) == EMPTY:
                        color = (0, 255, 0)
                    else:
                        color = (100, 0, 100)
                self.cube.set_color(x, y, 4, *color)
                self.cube.show()
                on = not on
            # use a smallish delay to make Thread.join() more responsive
            sleep(0.1)


class StoppableThread(Thread):
    """
    A normal thread with a stop event.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stop_event = Event()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()
