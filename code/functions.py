"""A few small functions used throughout the project."""

import math
from random import randint


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between two numbers."""
    return a * (1 - t) + b * t


def inv_lerp(a: float, b: float, x: float) -> float:
    """Inverse linear interpolation between two numbers."""
    return (x - a) / (b - a)


def remap(a: float, b: float, c: float, d: float, x: float) -> float:
    """Remaps a value x from a [a, b] interval to another interval [c, d]."""
    return c + (d - c) * inv_lerp(a, b, x)


def lerp_pts(xa: int, ya: int, xb: int, yb: int, t: float) -> tuple[int, int]:
    """Linear interpolation between two points."""
    return round(lerp(xa, xb, t)), round(lerp(ya, yb, t))


def t_step(xa: int, ya: int, xb: int, yb: int) -> float:
    """Calculates the step of t (which is the value by which t must be increased)."""
    return 1 / math.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)


def enemy_amount(wave: int) -> dict[str, int]:
    """Indicates the amount of enemies to be spawned in the specified wave."""
    return {"small": int((-4 / wave + 6 if wave < 4 else (wave + 2) / 3 + 3) * randint(1, 3) / 2),
            "normal": 0 if wave < 2 else int((math.sqrt(wave - 2) if wave < 11 else 0.2 * (11 - wave) ** 2 + 3) * randint(1, 3) / 2),
            "big": 0 if wave < 10 else int(0.8 * wave - 8 + randint(-1, 1))}


def len_of_int(number: int, include_sign: bool = False) -> int:
    """Returns the amount of digits that compose the specified integer.
    The 'include_sign' option indicates whether to count the sign as a digit when the number is negative."""
    if number == 0:
        return 1
    elif number > 0:
        return int(math.log10(number)) + 1
    else:
        return int(math.log10(-number)) + include_sign + 1


if __name__ == '__main__':  # Test zone
    print(remap(10, 20, 100, 200, 13))
