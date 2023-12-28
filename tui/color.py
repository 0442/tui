class RGBA:
    def __init__(self, r: int, g: int, b: int, a: int) -> None:
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
        return self._b

    @a.setter
    def a(self, new_value) -> None:
        self._validate_alpha(new_value)
        self._a = new_value

    def __eq__(self, other) -> bool:
        if isinstance(other, RGBA):
            return all(getattr(self,name) == getattr(other,name) for name in vars(self))
        return False

    def __hash__(self) -> int:
        return hash(tuple(getattr(self,name) for name in vars(self)))

class HSL:
    ...


class HSV:
    ...
