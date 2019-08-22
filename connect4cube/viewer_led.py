from queue import Queue, Empty
from threading import Thread, Event, current_thread
from time import sleep

from connect4cube import RED, BLUE, EMPTY
from connect4cube.cube import Cube
from connect4cube.viewer import BoardViewer

SELECT = 0
PLAY = 1
FINISH = 2


class LedViewer(BoardViewer):
    def __init__(self):
        super().__init__()
        self.cube = Cube()
        self.queue = Queue()
        self.animation_thread = StoppableThread(target=self.animation)
        self.animation_thread.setDaemon(True)
        self.animation_thread.start()

    def player_plays(self, x, y):
        self.queue.put((PLAY, x, y))

    def player_selects(self, x, y):
        self.queue.put((SELECT, x, y))

    def finish(self, winning_coords):
        self.queue.put((FINISH, winning_coords))

    def close(self):
        self.animation_thread.stop()
        self.animation_thread.join()

    def animation(self):
        animation_list = []
        animation_list.append(FieldColorsAnimation(self.board.field))
        while not current_thread().stopped() or animation_list[-1].is_blocking() or not self.queue.empty():
            if not animation_list[-1].is_blocking():
                try:
                    event = self.queue.get_nowait()
                    # some animations have to stop when a new one is started
                    animation_list[-1].new_animation_available()
                    if event[0] == PLAY:
                        super().player_plays(*event[1:3])
                        x = event[1]
                        y = event[2]
                        z = self.get_z(x, y)
                        c = RED
                        if self.board.next_color == RED:
                            c = BLUE
                        animation_list.append(PlayAnimation(x, y, z, c))
                        pass
                    elif event[0] == SELECT:
                        x = event[1]
                        y = event[2]
                        z = self.get_z(x, y)
                        c = self.board.next_color
                        animation_list.append(SelectAnimation(x, y, z, c))
                        pass
                    elif event[0] == FINISH:
                        c = RED
                        if self.board.next_color == RED:
                            c = BLUE
                        animation_list.append(FinishAnimation(event[1], c))
                except (Empty):
                    pass

            animation_cube = None
            for a in animation_list:
                animation_cube = a.animate(animation_cube)

            # remove completed animations from list
            animation_list[:] = [a for a in animation_list if not a.is_done()]

            # draw the completed cube
            self.cube.draw(animation_cube)
            self.cube.show()

            sleep(0.01)

    def get_z(self, x, y):
        z = 4
        while z > 0 and self.board.field(x, y, z - 1) == EMPTY:
            z -= 1
        return z


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


class AnimationBase():
    def animate(self, cube) -> list:
        # modify the cube with an animation
        return cube

    def is_done(self) -> bool:
        # animation is removed from the list once this is true
        return True

    def new_animation_available(self):
        # some animations must terminate when a new one arrives
        pass

    def is_blocking(self) -> bool:
        # blocking animations must be completed before a next animation is started
        return False


class SelectAnimation(AnimationBase):
    def __init__(self, x, y, z, c):
        super().__init__()
        self.done = False
        self.x = x
        self.y = y
        self.z = z
        self.c = c
        self.z_a = 5

    def animate(self, cube) -> list:
        if not self.done:
            color = None
            if self.c == RED:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)

            for z in range(self.z, 5):
                diff = abs(self.z_a - z)
                if diff <= 1:
                    c = tuple(map(lambda c: c * (1 - diff), color))
                    cube[self.x][self.y][z] = c
            self.z_a -= 0.1
            if self.z_a < self.z - 1:
                self.z_a = 5
        return cube

    def is_done(self) -> bool:
        return self.done

    def stop(self):
        pass

    def new_animation_available(self):
        self.done = True


class FinishAnimation(AnimationBase):
    class State():
        FLASH = 0
        BLINK = 1

    def __init__(self, winning_coords, c):
        super().__init__()
        self.done = False
        self.winning_coords = winning_coords
        self.c = c
        self.state = self.State.FLASH
        self.counter = 0

    def animate(self, cube) -> list:
        if not self.done:
            color = None
            if self.c == RED:
                color = (255, 0, 0)
            else:
                color = (0, 0, 255)
            if self.state == self.State.FLASH:
                color = tuple(map(lambda c: c - self.counter * 5, color))
                for x in range(5):
                    for y in range(5):
                        for z in range(5):
                            cube[x][y][z] = color
                if self.counter >= 60:
                    self.counter = -1
                    self.state = self.State.BLINK
            elif self.state == self.State.BLINK:
                color = tuple(map(lambda c: int(c - self.counter % 50 * (c / 50)), color))
                for c in self.winning_coords:
                    cube[c[0]][c[1]][c[2]] = color
                if self.counter >= 300:
                    self.done = True
            self.counter += 1
        return cube

    def is_done(self) -> bool:
        return self.done

    def stop(self):
        pass

    def is_blocking(self):
        return True


class PlayAnimation(AnimationBase):
    def __init__(self, x, y, z, c):
        super().__init__()

    def animate(self, cube) -> list:
        return cube

    def is_done(self) -> bool:
        return True

    def stop(self):
        pass

    def is_blocking(self):
        return True


class FieldColorsAnimation(AnimationBase):
    """
    Always the first animation, the cube provided to animate() is completely overwritten.
    """
    def __init__(self, field):
        super().__init__()
        self.field = field

    def animate(self, cube) -> list:
        cube = [[[(0, 0, 0) for _ in range(5)] for _ in range(5)] for _ in range(5)]
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    value = self.field(x, y, z)
                    if value == RED:
                        color = (255, 0, 0)
                    elif value == BLUE:
                        color = (0, 0, 255)
                    else:
                        color = (0, 0, 0)
                    cube[x][y][z] = color
        return cube

    def is_done(self) -> bool:
        return False
