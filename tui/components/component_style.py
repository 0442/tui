from __future__ import annotations
from dataclasses import dataclass, field, fields
from typing import Union, TypeAlias, Literal

from ..color import RGBA

Unit: TypeAlias = Union[int, float, str, None]


# pylint: disable=too-many-instance-attributes
@dataclass(eq=True, kw_only=True)
class Style:
    position: Literal["absolute", "relative"] = field(default="relative")

    x: Unit = field(default=None)
    y: Unit = field(default=None)

    width: Unit = field(default=None)
    height: Unit = field(default=None)
    min_width: Unit = field(default=None)
    min_height: Unit = field(default=None)
    max_width: Unit = field(default=None)
    max_height: Unit = field(default=None)

    color: RGBA = field(default=RGBA(255, 255, 255, 1))
    background_color: RGBA = field(default=RGBA(0, 0, 0, 0))

    padding_left: int = field(default=None)
    padding_right: int = field(default=None)
    padding_top: int = field(default=None)
    padding_bottom: int = field(default=None)

    margin_left: int = field(default=None)
    margin_right: int = field(default=None)
    margin_top: int = field(default=None)
    margin_bottom: int = field(default=None)

    border_color: RGBA = field(default=RGBA(255, 255, 255, 1))
    border: int = field(default=None)

    text_align: str = field(default=None)

    layout_direction: str = field(default="x")
    gap: Union[int, float, str] = field(default=0)

    def __add__(self, other: object) -> Style:
        """
        Combine two instances of Style.
        If an attribute is None in self, take the value from other.
        """
        if not isinstance(other, Style):
            raise TypeError(
                f"Unsupported operand type for +: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

        result = Style()

        for f in fields(self):
            new_value = getattr(self, f.name) or getattr(other, f.name)
            setattr(result, f.name, new_value)

        return result

    def __matmul__(self, other: object) -> Style:
        """Use this operation to overwrite.
        All values that are not none in the second
        style will overwrite the values of the first style.
        """
        if not isinstance(other, Style):
            raise TypeError(
                f"Unsupported operand type for @: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

        result = Style()

        for f in fields(self):
            new_value = getattr(other, f) or getattr(self, f)
            setattr(result, f, new_value)

        return result
