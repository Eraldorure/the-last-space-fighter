import pyxel as px

import functions as func


class Hitbox:
    """Une classe abstraite représentant une hitbox.
    Cette classe est utilisée par la totalité des objets qui possède une quelconque interaction."""

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def __repr__(self):
        return f"Hitbox({self.x}, {self.y}, {self.w}, {self.h})"

    def __contains__(self, co):
        """Semblable à la méthode is_inside, à la différence près que cette version s'utilise
        comme ceci : '(x, y) in hitbox'."""
        return self.is_inside(*co)

    def __and__(self, other):
        """Renvoie un booléen indiquant si deux hitboxes se chevauchent.
        S'utilise comme suit : 'hitbox1 & hitbox2'."""
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return (dx < self.w or dx < other.w) and (dy < self.h or dy < other.w)

    def is_inside(self, x, y):
        """Indique si deux coordonnées x et y se situent à l'intérieur de la hitbox."""
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h

    def draw(self, col):
        """Méthode permettant de dessiner la hitbox. À n'utiliser qu'à des fins de débug."""
        px.rect(self.x, self.y, self.w, self.h, col)


class Button:
    """Une classe permettant de représenter un bouton et d'interagir avec."""

    def __init__(self, x, y, width, height, text="", enabled=True):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.txt = text
        self.on = enabled
        self.hb = Hitbox(x, y, width, height)

    def toggle(self):
        """Permet de (dés)activer le bouton. Une fois désactivé, le bouton ne sera plus dessiné"""
        self.on = not self.on

    def is_pressed(self, btn=px.MOUSE_BUTTON_LEFT):
        """Indique si la souris est située à l'intérieur de la hitbox du bouton et que la touche renseignée (par
        défaut le clic gauche de la souris) est pressée."""
        return self.on and px.btnp(btn) and self.hb.is_inside(px.mouse_x, px.mouse_y)

    def draw(self, force=False):
        """Permet de dessiner le bouton.
        Le paramètre 'force' permet de forcer le dessin du bouton même si ce dernier est désactivé."""
        if self.on or force:
            px.rect(self.x, self.y, self.w, self.h, 9)
            px.rectb(self.x, self.y, self.w, self.h, 2)
            px.text(x=self.x + self.w // 2 - 2 * len(self.txt) + 1,
                    y=self.y + self.h // 2 - 2,
                    s=self.txt, col=7)


class Enemy:
    """Classe représentant un ennemi (de tout types)."""

    def __init__(self, x, y, model="normal"):
        if model not in self.MODELS:
            raise ValueError(f"unknown model '{model}', you must choose between between {', '.join(self.MODELS.keys())}")
        self.x = x
        self.y = y
        self.__attr = self.MODELS[model]
        self.w, self.h = self.__attr["size"]
        self.hp = self.__attr["hp"]
        self.__half_hp = self.hp // 2 + 1
        self.hb = Hitbox(x, y, self.w, self.h)

    def draw(self):
        """Dessine les ennemis. Leur design change en fonction de leur vie."""
        if self.is_injured:
            px.blt(self.x, self.y, 0, *self.__attr["full"], self.w, self.h, 0)
        else:
            px.blt(self.x, self.y, 0, *self.__attr["low"], self.w, self.h, 0)

    def harm(self, dmg: int):
        """Permet d'infliger des dégâts à l'ennemi.
        Modifie automatiquement les attributs 'dead' et 'injured'."""
        self.hp -= dmg

    @property
    def is_injured(self):
        return self.hp < self.__half_hp

    @property
    def is_dead(self):
        return self.hp < 1

    MODELS = {"small": {"hp": 2, "size": (11, 11), "full": (20, 0), "low": (32, 0)},
              "normal": {"hp": 8, "size": (16, 16), "full": (44, 0), "low": (60, 0)},
              "big": {"hp": 32, "size": (48, 48), "full": (102, 0), "low": (151, 0)}}


class Bullet:
    def __init__(self, colors, x, y, dir_x, dir_y):
        self.origin = x, y
        self.x = x
        self.y = y
        self.dx = dir_x
        self.dy = dir_y
        self.t = 0
        self.couleurs = colors
        self.step = func.t_step(x, y, dir_x, dir_y)
        self.hb = Hitbox(x, y, 1, 1)

    def move(self):
        try:
            self.x, self.y = func.lerp_pts(*self.origin, self.dx, self.dy, self.t)
        except OverflowError:
            self.x, self.y = 0, 0
        self.t += self.step

    def draw(self):
        px.rect(self.x, self.y, 1, 1, self.couleurs)


class Player:
    def __init__(self, start_x: int, start_y: int, hp: int = 3):
        self.x = start_x
        self.y = start_y
        self.hp = hp

    def move_up(self, step: int = 1):
        self.y -= step

    def move_down(self, step: int = 1):
        self.y += step

    def move_left(self, step: int = 1):
        self.x -= step

    def move_right(self, step: int = 1):
        self.x += step
