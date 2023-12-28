class RGBA:
    def __init__(self, r, g, b, a):
        self._validate_rgb(r)
        self._validate_rgb(g)
        self._validate_rgb(b)
        self._validate_alpha(a)

        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def _validate_rgb(self, value):
        if not 0 <= value <= 255:
            raise ValueError("RGB values must be in the range 0-255")

    def _validate_alpha(self, value):
        if not 0 <= value <= 1:
            raise ValueError("Alpha value must be in the range 0-1")

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, new_value):
        self._validate_rgb(new_value)
        self._r = new_value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, new_value):
        self._validate_rgb(new_value)
        self._g = new_value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, new_value):
        self._validate_rgb(new_value)
        self._b = new_value

    @property
    def a(self):
        return self._b

    @a.setter
    def a(self, new_value):
        self._validate_alpha(new_value)
        self._a = new_value


class HSL:
    ...


class HSV:
    ...
