
def clamp(min_value: int | None, value: int, max_value: int | None) -> int:
    """Clamps `value` between `min_value` and `max_value`, i.e. returns `value`
    unless it is outside the range of `min_value`-`max_value`, in which case
    the closer one of the limits is chosen.

    Args:
        min_value (int | None): Smalles allowed value. If None, is set to -inf.
        value (int): The value to be clamped.
        max_value (int | None): Largest allowed value. If None, is set to +inf.

    Returns:
        (int): The resulting, clamped value.
    """
    if min_value is None:
        min_value = float('-inf')
    if max_value is None:
        max_value = float('inf')
    return min(max(min_value, value), max_value)
