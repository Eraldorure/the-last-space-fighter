"""The file containing all the ui elements (such as buttons)."""

import pyxel as px
from code.functions import cut_max_text_width


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


class Text:
    """A class representing a text object.
    The text represented by this object is static, meaning its position will stay the same when any modification are
    made. Consequently, the appropriate way to modify anything is to recreate a whole new instance."""

    class Line:
        """A class representing a line of text."""

        def __init__(self, x: int, y: int, text: str, h_align: str):
            self.w = len(text) * 4 - 1
            self.h = 5
            if h_align == "left":
                self.x = x
            elif h_align == "center":
                self.x = x - self.w // 2
            else:
                self.x = x - self.w
            self.y = y
            self.txt = text
            self.hb = Hitbox(self.x, self.y, self.w, self.h + 1)

        def draw(self, color: int):
            """Draws the line of text."""
            px.text(self.x, self.y, self.txt, color)

        def draw_underline(self, color: int):
            """Draws a line under the text."""
            px.line(self.x, y := self.y + self.h + 1, self.x + self.w - 1, y, color)

    def __init__(self, x: int, y: int, text: str, max_width: int = None,
                 *, h_align: str = "left", v_align: str = "top"):
        if h_align not in ("left", "center", "right"):
            raise ValueError("invalid horizontal alignment, choose between 'left', 'center' and 'right'")
        if v_align not in ("top", "center", "bottom"):
            raise ValueError("invalid vertical alignment, choose between 'top', 'center' and 'bottom'")
        self.x = x
        self.y = y
        self.w = 0
        self.h = 0
        self.lines = []
        self.__txt = text
        self.__def_x = x
        self.__def_y = y
        self.__max_w = max_width
        self.__h_align = h_align
        self.__v_align = v_align
        self.hb = Hitbox(x, y, 0, 0)
        self.set_content(text)

    def __str__(self):
        return self.__txt

    def set_content(self, text: str, max_width: int = None):
        """Changes the content of the text. If 'max_width' is not specified, the previous one will be kept."""
        if max_width is not None:
            self.__max_w = max_width
        if self.__max_w is None:
            lines = text.splitlines()
        else:
            lines = cut_max_text_width(text, (self.__max_w + 1) // 4)
        self.__txt = text
        self.w = 0
        self.h = len(lines) * 6 - 1

        self.x = self.__def_x
        self.y = self.__def_y
        if self.__v_align == "center":
            self.y -= self.h // 2
        elif self.__v_align == "bottom":
            self.y -= self.h

        self.lines = []
        for i in range(len(lines)):
            line = self.Line(self.x, self.y + i * 6, lines[i], self.__h_align)
            self.lines.append(line)
            if line.w > self.w:
                self.x = line.x
                self.w = line.w
        self.hb = Hitbox(self.x, self.y, self.w, self.h)

    def draw(self, color: int = 7):
        """Draws the text. The default color is white."""
        for line in self.lines:
            line.draw(color)


class Button:
    """A class representing a button that you can interact with."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.txt = Text(x + width // 2, y + height // 2, text.upper(), width - 2, h_align="center", v_align="center")
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
        self.txt.draw(1)


class Button2(Button):
    """Same as a Button, but with a different style."""

    def draw(self):
        """Draws the button."""
        px.rectb(self.x, self.y, self.w, self.h, 3)
        if self.mouse_over():
            px.rect(self.x + 1, self.y + 1, self.w - 2, self.h - 2, 12)
            self.txt.draw(7)
        else:
            px.rect(self.x + 1, self.y + 1, self.w - 2, self.h - 2, 5)
            self.txt.draw(6)


class ClickableText(Text, Button):
    """A class representing a clickable text.
    It could be considered as text reacting the exact same way a button would."""

    def mouse_over(self) -> bool:
        """Returns either True if the mouse hovers over the text or False."""
        return any((line.hb & self.hb).contains(px.mouse_x, px.mouse_y) for line in self.lines)

    def draw(self, color: int = 7):
        """Writes the text. When the mouse hovers over the text, it underlines it."""
        if self.mouse_over():
            super().draw(1)
            self.lines[-1].draw_underline(5)
        else:
            super().draw(color)


class DropdownSelector:
    """A class representing a dropdown selector.
    It allows the user to select an option from a list of options."""

    def __init__(self, x: int, y: int, options: dict[str, str], default_opt: str):
        """The options argument should be a dict associating the effective value of the option with its display name."""
        self.options = {}
        self.__exp_w = 0
        self.__exp_h = 0
        for opt, val in options.items():
            txt = Text(x, y + self.__exp_h, val)
            self.__exp_h += txt.h + 3
            if txt.w > self.__exp_w:
                self.__exp_w = txt.w
            self.options[opt] = txt
        self.__exp_h -= 3
        self.selected = default_opt
        self.txt_selected = Text(x, y, options[default_opt])
        self.x = x
        self.y = y
        self.w = self.txt_selected.w
        self.h = self.txt_selected.h
        self.expanded = False
        self.hb1 = Hitbox(x, y, self.w, self.h)

    def mouse_over_which(self) -> str:
        """Returns the index of the option the mouse is over, or an empty string if it's not over any."""
        if self.expanded:
            for i, opt in enumerate(self.options):
                if self.options[opt].hb.contains(px.mouse_x, px.mouse_y):
                    return opt
        elif self.hb1.contains(px.mouse_x, px.mouse_y):
            return self.selected
        return ""

    def which_pressed(self) -> str:
        """Returns the index of the option that was pressed, or an empty string if no option was pressed."""
        if px.btnp(px.MOUSE_BUTTON_LEFT):
            return self.mouse_over_which()
        return ""

    def toggle_expand(self):
        """Toggles the expanded status of the dropdown selector."""
        self.expanded = not self.expanded
        if self.expanded:
            self.w = self.__exp_w
            self.h = self.__exp_h
        else:
            self.hb1.w = self.w = self.txt_selected.w
            self.hb1.h = self.h = self.txt_selected.h

    def update(self):
        """Updates the dropdown selector."""
        opt = self.which_pressed()
        if opt:
            if self.expanded:
                self.selected = opt
                self.txt_selected.set_content(str(self.options[opt]))
            self.toggle_expand()

    def draw(self):
        """Draws the dropdown selector."""
        mouse_over = self.mouse_over_which()
        px.line(x := self.x - 3, self.y - 1, x, self.y + self.h, 1)
        if self.expanded:
            px.rect(self.x - 2, self.y - 1, self.w + 3, self.h + 2, 0)
            for opt, txt in self.options.items():
                if opt == mouse_over:
                    txt.draw(2)
                elif opt == self.selected:
                    txt.draw(1)
                else:
                    txt.draw()
        elif mouse_over:
            self.txt_selected.draw(2)
        else:
            self.txt_selected.draw()


class Popup:
    """A class representing a popup window.
    It is used to display messages to the user as well as confirmation window."""

    mouse_over = Button.mouse_over

    def __init__(self, x: int, y: int, width: int, height: int, message: str, *,
                 option_l: str = "", option_r: str = "OK", show: bool = False):
        """The 'option_l' and 'option_r' arguments allows the user to customize the text of the buttons. If an empty
        string is given, the button will not be displayed.
        The 'show' parameter allows the Popup to be visible or not after instanciation."""
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.visible = show
        self.msg = Text(x + 5, y + 5, message, width - 10)
        self.btn_l = Button2(x + 5, y + height - 14, 31, 9, option_l) if option_l else None
        self.btn_r = Button2(x + width - 36, y + height - 14, 31, 9, option_r) if option_r else None
        self.hb = Hitbox(x, y, width, height)

    def toggle(self):
        """Toggles the visibility of the popup window."""
        self.visible = not self.visible

    def set_options(self, option_l: str | None = None, option_r: str | None = None):
        """Changes the text of the buttons.
        Give an empty string to hide the button, or None to keep the previous text."""
        if option_l == "":
            self.btn_l = None
        elif option_l is not None:
            if self.btn_l is None:
                self.btn_l = Button2(self.x + 5, self.y + self.h - 14, 31, 9, option_l)
            else:
                self.btn_l.txt.set_content(option_l)

        if option_r == "":
            self.btn_r = None
        elif option_r is not None:
            if self.btn_r is None:
                self.btn_r = Button2(self.x + self.w - 36, self.y + self.h - 14, 31, 9, option_r)
            else:
                self.btn_r.txt.set_content(option_l)

    def update(self):
        """Updates the popup window."""
        if self.visible:
            if px.btnp(px.MOUSE_BUTTON_LEFT) and not self.mouse_over() or \
                    self.btn_l is not None and self.btn_l.is_pressed() or \
                    self.btn_r is not None and self.btn_r.is_pressed():
                self.visible = False

    def draw(self):
        """Draws the popup window."""
        if not self.visible:
            return
        px.rect(self.x, self.y, self.w, self.h, 1)
        px.rectb(self.x, self.y, self.w, self.h, 6)
        self.msg.draw()
        if self.btn_l is not None:
            self.btn_l.draw()
        if self.btn_r is not None:
            self.btn_r.draw()
