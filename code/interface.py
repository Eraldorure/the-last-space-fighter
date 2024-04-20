"""Fichier contenant tous les éléments d'interface utilisateur tels que les boutons."""

import pyxel as px


class Hitbox:
    """Une classe abstraite représentant une hitbox.
    Cette classe est utilisée par la totalité des objets possédant une quelconque interaction."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def __repr__(self):
        return f"Hitbox({self.x}, {self.y}, {self.w}, {self.h})"

    def __contains__(self, co: tuple[int, int]):
        """Semblable à la méthode '.contains', à la différence près que cette version s'utilise comme ceci : `(x, y) in hitbox`."""
        return self.contains(*co)

    def __and__(self, other):
        """Renvoie un booléen indiquant si deux hitboxes se chevauchent.
        S'utilise comme suit : `hitbox1 & hitbox2`."""
        ax = self.x + self.w
        ay = self.y + self.h
        bx = other.x + other.w
        by = other.y + other.h
        return other.contains(self.x, self.y) or other.contains(self.x, ay) or other.contains(ax, self.y) or other.contains(ax, ay) \
            or self.contains(other.x, other.y) or self.contains(other.x, by) or self.contains(bx, other.y) or self.contains(bx, by)

    def contains(self, x: int, y: int) -> bool:
        """Indique si deux coordonnées x et y se situent à l'intérieur de la hitbox."""
        return self.x <= x < self.x + self.w and self.y <= y < self.y + self.h

    def draw(self, col: int):
        """Méthode permettant de dessiner la hitbox. N'est utilisée qu'à des fins de débogage."""
        px.rect(self.x, self.y, self.w, self.h, col)


class Button:
    """Une classe permettant de représenter un bouton et d'interagir avec."""

    def __init__(self, x: int, y: int, width: int, height: int, text: str = ""):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.txt = text
        self.hb = Hitbox(x, y, width, height)

    def __repr__(self):
        return f"Button({self.x}, {self.y}, {self.w}, {self.h}, {self.txt})"

    def is_pressed(self, btn: int = px.MOUSE_BUTTON_LEFT) -> bool:
        """Indique si la souris est située à l'intérieur de la hitbox du bouton et que la touche renseignée (par
        défaut le clic gauche de la souris) est pressée."""
        return px.btnp(btn) and self.mouse_over()

    def mouse_over(self) -> bool:
        """Renvoie True si la souris est en train de survoler le bouton et False sinon."""
        return self.hb.contains(px.mouse_x, px.mouse_y)

    def draw(self):
        """Permet de dessiner le bouton."""
        px.rect(self.x, self.y, self.w, self.h, 9)
        px.rectb(self.x, self.y, self.w, self.h, 2 - self.mouse_over())
        px.text(x=self.x + self.w // 2 - 2 * len(self.txt) + 1,
                y=self.y + self.h // 2 - 2,
                s=self.txt, col=7)


class ClickableText(Button):
    """Une classe permettant de représenter un texte cliquable. Fonctionne de la même manière qu'un bouton."""

    def __init__(self, x: int, y: int, text: str):
        self.txt = text
        temp = text.splitlines()
        super().__init__(x, y, max(len(line) for line in temp) * 4 - 1, len(temp) * 6 + 1, text)

    def __repr__(self):
        return f"ClickableText({self.x}, {self.y}, {self.txt})"

    def draw(self):
        col = 1 if self.mouse_over() else 7
        px.text(self.x, self.y, self.txt, col)
        if self.mouse_over():
            px.line(self.x, y := self.y + self.h - 1, self.x + self.w - 1, y, col)
