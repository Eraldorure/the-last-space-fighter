"""A few small functions used throughout the project."""

import math


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


def shorten_version(version: str, level: int) -> str:
    """Shortens the version string to the specified level."""

    temp = version.split(".")
    for i in range(1, len(temp)):
        temp[i] = "." + temp[i]
    if "-" in temp[-1]:
        temp.extend(temp.pop().split("-", 1))
        temp[-1] = "-" + temp[-1]
    if "+" in temp[-1]:
        temp.extend(temp.pop().split("+", 1))
        temp[-1] = "+" + temp[-1]
    return "".join(temp[:level])


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


def sign(number: float) -> int:
    """Returns the sign of the number (-1, 0 or 1)."""

    return (number > 0) - (number < 0)


if __name__ == '__main__':  # Test zone
    print(cut_max_text_width("Hey!\nThis is a test to see if the function works properly.\nThe good thing is that is apparently does!", 25))
