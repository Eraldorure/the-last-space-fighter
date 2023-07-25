"""Fichier contenant les classes nécessaires au bon fonctionnement du jeu, comme les ennemis, les tirs, le joueur, etc."""

import pyxel as px
from random import randint

import functions as func


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

    def __contains__(self, co):
        """Semblable à la méthode '.contains', à la différence près que cette version s'utilise
        comme ceci : '(x, y) in hitbox'."""
        return self.contains(*co)

    def __and__(self, other):
        """Renvoie un booléen indiquant si deux hitboxes se chevauchent.
        S'utilise comme suit : 'hitbox1 & hitbox2'."""
        ax = self.x + self.w
        ay = self.y + self.h
        bx = other.x + other.w
        by = other.y + other.h
        return other.contains(self.x, self.y) or other.contains(self.x, ay) or other.contains(ax, self.y) or other.contains(ax, ay) \
            or self.contains(other.x, other.y) or self.contains(other.x, by) or self.contains(bx, other.y) or self.contains(bx, by)

    def contains(self, x, y) -> bool:
        """Indique si deux coordonnées x et y se situent à l'intérieur de la hitbox."""
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    def draw(self, col: int):
        """Méthode permettant de dessiner la hitbox. À n'utiliser qu'à des fins de débug."""
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
        """Permet de dessiner le bouton.
        Le paramètre 'force' permet de forcer le dessin du bouton même si ce dernier est désactivé."""
        px.rect(self.x, self.y, self.w, self.h, 9)
        px.rectb(self.x, self.y, self.w, self.h, 2 - self.mouse_over())
        px.text(x=self.x + self.w // 2 - 2 * len(self.txt) + 1,
                y=self.y + self.h // 2 - 2,
                s=self.txt, col=7)


class Enemy:
    """Classe représentant un ennemi (de tout types)."""

    def __init__(self, x: int, y: int, dir_x: int, dir_y: int, model: str = "normal"):
        if model not in self.MODELS:
            raise ValueError(f"unknown model '{model}', you must choose between between {', '.join(self.MODELS.keys())}")
        self.x = x
        self.y = y
        self.__ox = x
        self.__oy = y
        self.__dx = dir_x
        self.__dy = dir_y
        self.t = 0
        self.step = func.t_step(x, y, dir_x, dir_y) * randint(3, 5) / 10
        self.__model = model
        self.__attr = self.MODELS[model]
        self.w, self.h = self.__attr["size"]
        self.hp = self.__attr["hp"]
        self.death_score = self.hp
        self.__half_hp = self.hp // 2 + 1
        self.hb = Hitbox(x, y, self.w, self.h)

    def __repr__(self):
        return f"Enemy({self.x}, {self.y}, {self.__dx}, {self.__dy}, {self.__model}"

    def draw(self):
        """Dessine les ennemis. Leur design change en fonction de leur vie."""
        if self.is_injured:
            px.blt(self.x, self.y, 0, *self.__attr["low"], self.w, self.h, self.__attr["bg"])
        else:
            px.blt(self.x, self.y, 0, *self.__attr["full"], self.w, self.h, self.__attr["bg"])

    def move(self, speed: float = 1):
        """Permet de déplacer l'ennemi automatiquement dans la direction fournie lors de l'instanciation.
        L'attribut 'speed' est un coefficient qui permet d'altérer la vitesse de déplacement en venant se multiplier à cette dernière."""
        self.t += self.step * speed
        self.x, self.y = func.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        self.hb.x = self.x
        self.hb.y = self.y

    @property
    def is_injured(self) -> bool:
        """Indique si l'ennemi est blessé, c'est-à-dire si ses PV actuels sont inférieurs à ses PV de départ."""
        return self.hp < self.__half_hp

    @property
    def is_dead(self) -> bool:
        """Indique si l'ennemi est mort, c'est-à-dire si ses PV inférieurs ou égaux à 0."""
        return self.hp < 1

    MODELS = {"small": {"hp": 2, "size": (11, 11), "full": (32, 0), "low": (20, 0), "bg": 0},
              "normal": {"hp": 8, "size": (15, 15), "full": (44, 0), "low": (60, 0), "bg": 0},
              "big": {"hp": 32, "size": (30, 30), "full": (31, 73), "low": (31, 104), "bg": 11},
              "boss": {"hp": 96, "size": (48, 44), "full": (102, 0), "low": (151, 0), "bg": 0}}


class Bullet:
    """Classe représentant un tir (qu'il soit allié ou ennemi).
    Fonctionne grâce à des interpolations linéaires (aka lerp)."""

    def __init__(self, x: int, y: int, dir_x: int, dir_y: int, color: int = 7):
        self.x = x
        self.y = y
        self.__dx = dir_x
        self.__dy = dir_y
        self.__ox = x
        self.__oy = y
        self.t = 0
        self.col = color
        self.step = 2 * func.t_step(x, y, dir_x, dir_y)
        self.used = False
        self.hb = Hitbox(x, y, 1, 1)

    def __repr__(self):
        return f"Bullet({self.x}, {self.y}, {self.__dx}, {self.__dy}, {self.col})"

    def move(self):
        """Permet de déplacer le tir automatiquement dans la direction fournie lors de l'instanciation."""
        self.x, self.y = func.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        self.hb.x = self.x
        self.hb.y = self.y
        self.t += self.step

    def draw(self):
        """Permet de dessiner le tir."""
        px.pset(self.x, self.y, self.col)


class Player:
    """Classe représentant le joueur, c'est-à-dire le vaisseau que le joueur contrôle."""

    def __init__(self, start_x: int, start_y: int, hp: int = 3):
        self.x = start_x
        self.y = start_y
        self.hp = hp
        self.hb = Hitbox(start_x, start_y, 9, 7)

    def __repr__(self):
        return f"Player({self.x}, {self.y}, {self.hp})"

    def draw(self):
        """Permet de dessiner le joueur, c'est-à-dire son vaisseau."""
        px.blt(self.x, self.y, 0, 0, 0, 9, 7, 0)

    def move_up(self, step: int = 1):
        """Déplace le joueur vers le haut de 'step' pixels."""
        self.y -= step
        self.hb.y -= step

    def move_down(self, step: int = 1):
        """Déplace le joueur vers le bas de 'step' pixels."""
        self.y += step
        self.hb.y += step

    def move_left(self, step: int = 1):
        """Déplace le joueur vers la gauche de 'step' pixels."""
        self.x -= step
        self.hb.x -= step

    def move_right(self, step: int = 1):
        """Déplace le joueur vers la droite de 'step' pixels."""
        self.x += step
        self.hb.x += step

    @property
    def is_dead(self) -> bool:
        """Indique si le joueur est mort, c'est-à-dire si ses PV sont inférieurs ou égaux à 0."""
        return self.hp < 1
