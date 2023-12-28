# Basic implementation, mainly for testing. This should probably be an
# ABC which would be subclassed to create different kinds of viewports,
# e.g. a viewport for a terminal that updates its size when terminal
# is resized.
class Viewport:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new):
        self._x = new

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new):
        self._y = new

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new):
        self._width = new

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new):
        self._height = new
