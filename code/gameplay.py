"""File containing classes necessary to the game such as ennemies, bullets, the player, etc."""

import pyxel as px
from random import random, choice
from code import functions as fn
from code.interface import Hitbox


class _Enemy:
    """Class representing an abstract enemy. The distinction between types of enemies is done with subclasses.
    Warning: This class is only used for inheritance purposes. Use one of its subclasses instead."""

    def __init__(self, x: int, y: int, width: int, height: int, hp: int, skin: int = None):
        if skin is None:
            self.skin = choice(self.SKINS)
        else:
            self.skin = self.SKINS[skin]
        self.w = width
        self.h = height
        self.hb = Hitbox(x + 1, y + 1, width - 2, height - 2)  # The hitbox is smaller than the enemy itself to make it more fair
        self.speed = 1 / (1.2 + random())
        self.score = hp
        self.is_dead = False
        self.hp = hp
        self.__max_hp = hp
        self.__x = x
        self.__y = y

    def draw(self):
        """Draws the enemy depending on its current skin. The HP bar is also drawn."""
        if self.is_dead:
            return
        px.blt(self.x, self.y, 0, self.skin[0], self.skin[1], self.w, self.h, self.skin[2])
        diff = self.w // 10
        px.line(self.x + diff, self.y - 2, fn.remap(0, self.__max_hp, self.x + diff, self.x + self.w - diff, self.hp) - 1, self.y - 2, 8)

    def move(self, target_x: int, target_y: int):
        """Moves the enemy towards the point given in the arguments."""
        dist_x = target_x - self.x - self.w // 2
        dist_y = target_y - self.y - self.h // 2
        if abs(dist_x) > abs(dist_y):
            x = px.sgn(dist_x) * self.speed / 2
            self.__x += x
            self.hb.x = self.x
        y = px.sgn(dist_y) * self.speed
        self.__y += y
        self.hb.y = self.y

    def hurt(self, damage: int):
        """Reduces the enemy's HP by the amount given in the arguments."""
        self.hp -= damage
        if self.hp <= 0:
            self.is_dead = True

    def delete(self):
        """Removes the enemy from the game. Its death will not reward the player any points."""
        self.is_dead = True
        self.score = 0

    @property
    def x(self):
        return round(self.__x)

    @property
    def y(self):
        return round(self.__y)

    SKINS = []


class SmallEnemy(_Enemy):
    """Class representing a small enemy."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 11, 11, 2)

    SKINS = [(20, 0, 0), (32, 0, 0)]


class MediumEnemy(_Enemy):
    """Class representing a medium enemy."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 15, 15, 8)
        self.speed *= 0.8

    SKINS = [(60, 0, 0), (44, 0, 0)]


class LargeEnemy(_Enemy):
    """Class representing a large enemy."""

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 30, 30, 32)
        self.speed *= 0.6

    SKINS = [(0, 73, 11), (31, 73, 11), (0, 104, 11), (31, 104, 11)]


# + Boss class: hp=96 w=48 h=44 full=102,0 low=151,0 bg=0


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

    def draw(self):
        """Draws the bullet."""
        px.pset(self.x, self.y, self.col)

    def move(self):
        """Moves the bullet in the direction defined during instanciation."""
        self.x, self.y = fn.lerp_pts(self.__ox, self.__oy, self.__dx, self.__dy, self.t)
        self.t += self.step

    def delete(self):
        """Marks the bullet as deleted, meaning it will be removed from the list of bullets in the main loop."""
        self.is_deleted = True


class Player:
    """Class representing the player, aka the spaceship controlled by the player."""

    def __init__(self, start_x: int, start_y: int, hp: int = 3):
        self.x = start_x
        self.y = start_y
        self.w = 9
        self.h = 7
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
