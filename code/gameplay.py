"""File containing classes necessary to the game such as ennemies, bullets, the player, etc."""

import pyxel as px
from random import randint
import code.functions as fn
from code.interface import Hitbox


class Enemy:
    """Class representing an enemy (of all types)."""

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

    def draw(self):
        """Draws the enemy. Its design changes based on both its model and its health."""
        if self.is_injured:
            px.blt(self.x, self.y, 0, *self.__attr["low"], self.w, self.h, self.__attr["bg"])
        else:
            px.blt(self.x, self.y, 0, *self.__attr["full"], self.w, self.h, self.__attr["bg"])

    def move(self, speed: float = 1):
        """Moves the enemy in the direction defined during instanciation.
        The 'speed' parameter is a coefficient that changes the moving speed of the unit."""
        self.t += self.step * speed
        self.x, self.y = fn.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        self.hb.x = self.x
        self.hb.y = self.y

    @property
    def is_injured(self) -> bool:
        """Indicates whether the enemy is injured, i.e. if its current HP are below half of its maximum HP."""
        return self.hp < self.__half_hp

    @property
    def is_dead(self) -> bool:
        """Indicates whether the enemy is dead, i.e. if its current HP are equal to or below 0."""
        return self.hp <= 0

    MODELS = {"small": {"hp": 2, "size": (11, 11), "full": (32, 0), "low": (20, 0), "bg": 0},
              "normal": {"hp": 8, "size": (15, 15), "full": (44, 0), "low": (60, 0), "bg": 0},
              "big": {"hp": 32, "size": (30, 30), "full": (31, 73), "low": (31, 104), "bg": 11},
              "boss": {"hp": 96, "size": (48, 44), "full": (102, 0), "low": (151, 0), "bg": 0}}


class Bullet:
    """Class representing a bullet. Works using linear interpolations to move in a straight line."""

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

    def move(self):
        """Moves the bullet in the direction defined during instanciation."""
        self.x, self.y = fn.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        self.t += self.step

    def delete(self):
        """Marks the bullet as deleted, meaning it will be removed from the list of bullets in the main loop."""
        self.is_deleted = True
        self.col = 2

    def draw(self):
        """Draws the bullet."""
        px.pset(self.x, self.y, self.col)


class Player:
    """Class representing the player, aka the spaceship controlled by the player."""

    def __init__(self, start_x: int, start_y: int, hp: int = 3):
        self.x = start_x
        self.y = start_y
        self.hp = hp
        self.hb = Hitbox(start_x, start_y, 9, 7)

    def draw(self):
        """Draws the player (or more precisely the spaceship)."""
        px.blt(self.x, self.y, 0, 0, 0, 9, 7, 0)

    def move_up(self, step: int = 1):
        """Moves the player up by 'step' pixels."""
        self.y -= step
        self.hb.y -= step

    def move_down(self, step: int = 1):
        """Moves the player down by 'step' pixels."""
        self.y += step
        self.hb.y += step

    def move_left(self, step: int = 1):
        """Moves the player to the left by 'step' pixels."""
        self.x -= step
        self.hb.x -= step

    def move_right(self, step: int = 1):
        """Moves the player to the right by 'step' pixels."""
        self.x += step
        self.hb.x += step

    @property
    def is_dead(self) -> bool:
        """Indicates whether the player is dead, i.e. if its current HP are equal to or below 0."""
        return self.hp <= 0
