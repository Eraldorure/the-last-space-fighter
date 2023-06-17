import math


def lerp(a: int, b: int, t: float):
    """Fonction d'interpolation linéaire entre deux nombres."""
    return a * (1 - t) + b * t


def lerp_pts(xa: int, ya: int, xb: int, yb: int, t: float):
    """Fonction d'interpolation linéaire entre deux points."""
    return int(lerp(xa, xb, t)), int(lerp(ya, yb, t))


def t_step(xa: int, ya: int, xb: int, yb: int):
    """Permet de calculer le pas de t (c'est-à-dire la valeur par laquelle il faut l'incrémenter)."""
    return 1 / math.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)


def enemy_amount(wave: int):
    """Permet d'indiquer le nombre d'ennemis à envoyer par vague."""
    return {"small": 2 * wave,
            "normal": int(math.log(wave)),
            "big": 0 if wave < 10 else (wave - 9) ** 2}


def normalize(x: int, y: int):
    """Fonction permettant de normaliser un vecteur (ici représenté par les arguments x et y), c'est-à-dire de le
    redimensionner afin que sa norme soit égale à 1."""
    length = math.sqrt(x ** 2 + y ** 2)
    return x / length, y / length
