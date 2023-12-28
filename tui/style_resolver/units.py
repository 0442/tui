from abc import ABC
from typing import Union, Literal

Axis = Literal["x", "Y"]


class Unit(ABC):
    def __init__(self, value: Union[int, float, str]) -> None:
        self._value = value

    @staticmethod
    def _parse_percentage(value_str: str) -> float:
        value_str = value_str.strip()
        number_part = value_str.removesuffix("%")

        try:
            percentage_scalar = float(number_part)
        except ValueError as e:
            raise ValueError(
                f"Invalid string format for {__class__.__name__}: '{value_str}'"
            ) from e

        return percentage_scalar / 100

    @staticmethod
    def _parse_number_str(value_str: str) -> int | float:
        """Converts string to int or float.
        """

        try:
            if value_str.count(".") == 0 and value_str.count(",") == 0:
                return int(value_str)
            return float(value_str)
        except ValueError as e:
            raise ValueError(
                f"Invalid string format for {__class__.__name__}: '{value_str}'"
            ) from e


class Position(Unit):
    def resolve(self, reference_pos: int, reference_size: int) -> int:
        if not isinstance(self._value, str):
            return int(reference_pos + self._value)

        if self._value.endswith("%"):
            percentage = self._parse_percentage(self._value)
            return int(reference_pos + reference_size * percentage)

        return int(reference_pos + self._parse_number_str(self._value))


class Size(Unit):
    def resolve(self, parent_size: int) -> int:
        if not isinstance(self._value, str):
            return int(self._value)

        if not parent_size:
            return 0

        if self._value.endswith("%"):
            percentage = self._parse_percentage(self._value)
            return int(parent_size * percentage)

        return int(self._parse_number_str(self._value))
