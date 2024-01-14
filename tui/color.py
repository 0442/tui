class RGBA:
    def __init__(self, r: int, g: int, b: int, a: int = 1) -> None:
        self._validate_rgb(r)
        self._validate_rgb(g)
        self._validate_rgb(b)
        self._validate_alpha(a)

        self._r = r
        self._g = g
        self._b = b
        self._a = a

    def _validate_rgb(self, value) -> None:
        if not 0 <= value <= 255:
            raise ValueError("RGB values must be in the range 0-255")

    def _validate_alpha(self, value) -> None:
        if not 0 <= value <= 1:
            raise ValueError("Alpha value must be in the range 0-1")

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, new_value) -> None:
        self._validate_rgb(new_value)
        self._r = new_value

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, new_value) -> None:
        self._validate_rgb(new_value)
        self._g = new_value

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, new_value) -> None:
        self._validate_rgb(new_value)
        self._b = new_value

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, new_value) -> None:
        self._validate_alpha(new_value)
        self._a = new_value

    def __eq__(self, other) -> bool:
        if self is other:
            return True
        return isinstance(other, RGBA) and self.r == other.r and self.g == other.g and self.b == other.b and self.a == other.a

    def __hash__(self) -> int:
        return hash((self._r, self._g, self._b, self._a))

    def __add__(self, other: 'RGBA') -> 'RGBA':
        oa = other.a
        r = other.r * oa + int(self._r * (1-oa))
        g = other.g * oa + int(self._g * (1-oa))
        b = other.b * oa + int(self._b * (1-oa))
        return RGBA(r, g, b)

    def merge(self, other: 'RGBA'):
        oa = other.a
        if oa == 1:
            self = other
        self._r = other.r * oa + int(self._r * (1-oa))
        self._g = other.g * oa + int(self._g * (1-oa))
        self._b = other.b * oa + int(self._b * (1-oa))

    def __str__(self):
        return f"RGBA: ({self._r}, {self._g}, {self._b}, {self._a})"


class HSL:
    ...


class HSV:
    ...
