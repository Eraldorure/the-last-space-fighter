"""The file containing all the ui elements (such as buttons)."""

import pyxel as px


class Hitbox:
    """A class representing a hitbox.
    The class is used by all objects that can be interacted with."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def __bool__(self):
        """Returns either True if the hitbox is valid (aka if both its width and height are strictly positive) or False."""
        return self.w > 0 and self.h > 0

    def __contains__(self, co: tuple[int, int]):
        """Similar to the 'contains' method, with the exception that this one is used like : `(x, y) in hitbox`."""
        return self.contains(*co)

    def __and__(self, other):
        """Returns the overlapping area between two hitboxes.
        To be used as follows : `hitbox1 & hitbox2`."""
        if not (self and other):
            return Hitbox(0, 0, 0, 0)
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        w = min(self.x + self.w, other.x + other.w) - x
        h = min(self.y + self.h, other.y + other.h) - y
        return Hitbox(x, y, w, h)

    def contains(self, x: int, y: int) -> bool:
        """Indicates if two coordinates x and y are situated inside the hitbox."""
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def draw(self, col: int):
        """Method to draw the hitbox. To be used for debugging purposes."""
        px.rect(self.x, self.y, self.w, self.h, col)


class Button:
    """A class representing a button that you can interact with."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str = ""):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.txt = text
        self.hb = Hitbox(x, y, width, height)

    def is_pressed(self, btn: int = px.MOUSE_BUTTON_LEFT) -> bool:
        """Indicates whether the mouse is inside the button and the given key (left click by default) is pressed.
        If it's the case, the button is considered as pressed."""
        return px.btnp(btn) and self.mouse_over()

    def mouse_over(self) -> bool:
        """Returns either True if the mouse hovers over the button or False."""
        return self.hb.contains(px.mouse_x, px.mouse_y)

    def draw(self):
        """Draws the button."""
        if self.mouse_over():
            px.rectb(self.x - 1, self.y - 1, self.w + 2, self.h + 2, 2)
            px.rect(self.x, self.y, self.w, self.h, 10)
        else:
            px.rectb(self.x, self.y, self.w, self.h, 1)
            px.rect(self.x + 1, self.y + 1, self.w - 2, self.h - 2, 9)
        px.text(self.x + self.w // 2 - 2 * len(self.txt) + 1,
                self.y + self.h // 2 - 2,
                self.txt, 1)


class ClickableText(Button):
    """A class representing a clickable text. Works the exact same way a button does"""

    def __init__(self, x: int, y: int, text: str):
        self.txt = text
        temp = text.splitlines()
        super().__init__(x, y, max(len(line) for line in temp) * 4 - 1, len(temp) * 6 - 1, text)

    def draw(self):
        """Writes the text. When the mouse hovers over the text, it underlines it."""
        if self.mouse_over():
            px.text(self.x, self.y, self.txt, 1)
            px.line(self.x, y := self.y + self.h + 1, self.x + self.w - 1, y, 5)
        else:
            px.text(self.x, self.y, self.txt, 7)
