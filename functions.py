"""Quelques petites fonctions utilisées partout dans le projet."""

import math
from random import randint


def lerp(a: int, b: int, t: float) -> float:
    """Fonction d'interpolation linéaire entre deux nombres."""
    return a * (1 - t) + b * t


def lerp_pts(xa: int, ya: int, xb: int, yb: int, t: float) -> tuple[int, int]:
    """Fonction d'interpolation linéaire entre deux points."""
    return round(lerp(xa, xb, t)), round(lerp(ya, yb, t))


def t_step(xa: int, ya: int, xb: int, yb: int) -> float:
    """Permet de calculer le pas de t (c'est-à-dire la valeur par laquelle il faut l'incrémenter)."""
    return 1 / math.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)


def enemy_amount(wave: int) -> dict[str, int]:
    """Permet d'indiquer le nombre d'ennemis à envoyer par vague."""
    return {"small": int((-4 / wave + 6 if wave < 4 else (wave + 2) / 3 + 3) * randint(1, 3) / 2),
            "normal": 0 if wave < 2 else int((math.sqrt(wave - 2) if wave < 11 else 0.2 * (11 - wave) ** 2 + 3) * randint(1, 3) / 2),
            "big": 0 if wave < 10 else int(0.8 * wave - 8 + randint(-1, 1))}


def len_of_int(number: int, include_sign: bool = False) -> int:
    """Renvoie le nombre de chiffres qui composent un nombre entier.
    Le paramètre 'include_sign' indique s'il faut également compter le signe comme un chiffre si le nombre est négatif."""
    if number == 0:
        return 1
    elif number > 0:
        return int(math.log10(number)) + 1
    else:
        return int(math.log10(-number)) + 1 + include_sign
