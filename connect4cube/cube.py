from connect4cube.util import is_a_raspberry

if is_a_raspberry():
    from connect4cube.cube_led import LedCube
else:
    from connect4cube.cube_vpython import VPythonCube


class Cube():
    """
    Singleton class of an LED cube. Depending on the target the real LED cube or a vpython mochup is used.
    """
    instance = None

    class __Cube:
        cube = None

        def __init__(self):
            if is_a_raspberry():
                self.cube = LedCube()
            else:
                self.cube = VPythonCube()

        def set_color(self, x, y, z, r, g, b):
            self.cube.set_color(x, y, z, r, g, b)

        def show(self):
            self.cube.show()

    def __init__(self):
        if not Cube.instance:
            Cube.instance = Cube.__Cube()

    def __getattr__(self, name):
        return getattr(self.instance, name)
