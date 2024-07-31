"""A few small functions used throughout the project."""

import math
from typing import Any, Iterable


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


def cut_max_text_width(text: str, max_width: int) -> list[str]:
    """Cuts the text to fit the specified width in multiple lines without cutting words while respecting line breaks.
    Returns a list containing all the lines."""

    lines = []
    for line in text.splitlines():
        if len(line) <= max_width:
            lines.append(line)
        else:
            temp = ""
            for word in line.split():
                if len(temp) + len(word) <= max_width:
                    temp += word + " "
                else:
                    lines.append(temp.rstrip())
                    temp = word + " "
            lines.append(temp.rstrip())
    return lines


def set_seq_length(seq: Iterable, value: Any, length: int) -> Iterable:
    """Sets the length of a sequence to the specified length by adding the specified value at the end. If the sequence
    is already longer than the specified length, it will be truncated. Returns the new sequence as a generator."""

    i = 0
    for el in seq:
        i += 1
        yield el
        if i == length:
            break
    while i < length:
        i += 1
        yield value


if __name__ == '__main__':
    print(*set_seq_length([1, 2, 3], 0, 5))
    print(*set_seq_length([1, 2, 3, 4, 5], 0, 3))
