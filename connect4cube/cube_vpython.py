from vpython import sphere, vector, canvas, color


class VPythonCube():
    """
    A Mockup class for local pingpong LED debugging
    """
    no_color = color.white * 0.25

    def __init__(self):
        c = canvas()
        self.pixels = [None] * 125
        for x in range(5):
            for y in range(5):
                for z in range(5):
                    pxid = self.xyz2pxid(x, y, z)
                    led = sphere(canvas=c,
                                 pos=vector(x - 2, z - 2, y - 2),
                                 radius=0.2,  # pingpong ball diameter is 40mm, distance between 'em 100mm
                                 color=self.no_color)
                    # noinspection PyTypeChecker
                    self.pixels[pxid] = led

    def xyz2pxid(self, x, y, z) -> int:
        return x + y * 5 + z * 25

    def set_color(self, x, y, z, r, g, b):
        pxid = self.xyz2pxid(x, y, z)
        self.pixels[pxid].color = vector(r / 200.0, g / 200.0, b / 200.0) * 0.75 + self.no_color

    def show(self):
        pass