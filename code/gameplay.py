"""Fichier contenant les classes nécessaires au bon fonctionnement du jeu, comme les ennemis, les tirs, le joueur, etc."""

import pyxel as px
from random import randint

import code.functions as fn
from code.interface import Hitbox


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
        self.step = fn.t_step(x, y, dir_x, dir_y) * randint(3, 5) / 10
        self.__model = model
        self.__attr = self.MODELS[model]
        self.w, self.h = self.__attr["size"]
        self.hp = self.__attr["hp"]
        self.death_score = self.hp
        self.__half_hp = self.hp // 2 + 1
        self.hb = Hitbox(x + 1, y + 1, self.w - 2, self.h - 2)

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
        self.x, self.y = fn.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        self.hb.x = self.x
        self.hb.y = self.y

    @property
    def is_injured(self) -> bool:
        """Indique si l'ennemi est blessé, c'est-à-dire si ses PV actuels sont inférieurs à la moitié de ses PV de départ."""
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
        self.step = 2 * fn.t_step(x, y, dir_x, dir_y)
        self.is_deleted = False
        # self.hb = Hitbox(x, y, 1, 1)  # Inutile à l'heure actuelle

    def __repr__(self):
        return f"Bullet({self.x}, {self.y}, {self.__dx}, {self.__dy}, {self.col})"

    def move(self):
        """Permet de déplacer le tir automatiquement dans la direction fournie lors de l'instanciation."""
        self.x, self.y = fn.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        # self.hb.x = self.x
        # self.hb.y = self.y
        self.t += self.step

    def delete(self):
        """Permet d'indiquer que le tir doit être supprimé, ou du moins qu'il est ineffectif."""
        self.is_deleted = True
        self.col = 2

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
