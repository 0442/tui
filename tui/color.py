class RGB:
    def __init__(self, r, g, b):
        self._validate_value(r)
        self._validate_value(g)
        self._validate_value(b)

        self._r = r
        self._g = g
        self._b = b

    def _validate_value(self, value):
        if not (0 <= value <= 255):
            raise ValueError("RGB values must be in the range 0-255")

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, new_value):
        self._validate_value(new_value)
        self._r = new_value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, new_value):
        self._validate_value(new_value)
        self._g = new_value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, new_value):
        self._validate_value(new_value)
        self._b = new_value


class HSL:
    ...


class HSV:
    ...
