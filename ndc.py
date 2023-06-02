import pyxel
import pyxel as px
import math


def lerp(a, b, t):
    """Fonction d'interpolation linéaire entre deux nombres."""
    return a * (1 - t) + b * t


def lerp_pts(xa, ya, xb, yb, t):
    """Fonction d'interpolation linéaire entre deux points."""
    return int(lerp(xa, xb, t)), int(lerp(ya, yb, t))


def t_step(xa, ya, xb, yb):
    """Permet de calculer le pas de t (c'est-à-dire la valeur par laquelle il faut incrémenter t)."""
    return 1 / px.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)


def enemy_amount(wave):
    """Permet d'indiquer le nombre d'ennemis à envoyer par vague."""
    return {"small": 2 * wave,
            "normal": int(math.log(wave)),
            "big": 0 if wave < 10 else (wave - 9) ** 2}


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
        """Renvoie un booléen indiquant si deux hitboxs se chevauchent.
        S'utilise comme suit : 'hitbox1 & hitbox2'."""
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)
        return (dx <= self.w or dx <= other.w) and (dy <= self.h or dy <= other.w)

    def is_inside(self, x, y):
        """Indique si deux coordonnées x et y se situent à l'intérieur de la hitbox."""
        return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h


class Button:
    """Une classe permettant de représenter un bouton et d'interagir avec."""

    def __init__(self, x, y, width, height, text="", enabled=True):
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.txt = text
        self.on = enabled
        self.__hb = Hitbox(x, y, width, height)

    def toggle(self):
        """Permet de (dés)activer le bouton. Une fois désactivé, le bouton ne sera plus dessiné"""
        self.on = not self.on

    def is_pressed(self, btn=px.MOUSE_BUTTON_LEFT):
        """Indique si la souris est située à l'intérieur de la hitbox du bouton et que la touche renseignée (par
        défaut le clic gauche de la souris) est pressée."""
        return self.on and px.btnp(btn) and self.__hb.is_inside(px.mouse_x, px.mouse_y)

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
        self.attr = self.MODELS[model]
        self.w, self.h = self.attr["size"]
        self.hp = self.attr["hp"]
        self.__half = self.hp // 2 + 1
        self.hb = Hitbox(x, y, self.w, self.h)

    def draw(self):
        """Dessine les ennemis. Leur design change en fonction de leur vie."""
        if self.hp < self.__half:
            px.blt(self.x, self.y, 0, *self.attr["full"], self.w, self.h)
        else:
            px.blt(self.x, self.y, 0, *self.attr["low"], self.w, self.h)

    MODELS = {"small": {"hp": 2, "size": (10, 10), "full": (20, 0), "low": (32, 0)},
              "normal": {"hp": 8, "size": (16, 16), "full": (44, 0), "low": (60, 0)},
              "big": {"hp": 32, "size": (48, 48), "full": (102, 0), "low": (151, 0)}}


class Bullet:
    def __init__(self, colors, position, x, y):
        self.couleurs = colors
        self.pos = position
        self.xy = (x, y)
        self.pas = t_step(*self.pos, *self.xy)
        self.t = 0
        self.hb = Hitbox(x, y, 1, 1)

    def deplacement(self):
        try:
            self.pos = lerp_pts(*self.pos, *self.xy, self.t)
        except OverflowError:
            self.pos = 0, 0
        self.t += self.pas
        self.hb.x, self.hb.y = self.pos

    def draw(self):
        px.rect(*self.pos, 1, 1, self.couleurs)


class Game:
    def __init__(self):
        self.hb = Hitbox(64, 100, 7, 6)
        self.play = Button(45, 64, 35, 10, "PLAY")
        self.balles = []
        self.direction = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.nb_vie = 3
        self.decor = []
        self.ennemie = []
        self.wave = 1
        px.init(128, 128, title="NDC 2023", fps=60)
        px.load("ndc.pyxres")
        px.mouse(True)
        px.run(self.update, self.draw)

    def deplacement(self,  d):
        if 0 < self.hb.x + self.direction[d][0] < 120 and 10 < self.hb.y + self.direction[d][1] < 125:
            self.hb.x += self.direction[d][0]
            self.hb.y += self.direction[d][1]

    def update(self):
        px.cls(0)
        if self.play.is_pressed():
            self.play.toggle()
            px.mouse(self.play.on)
        if not self.play.on:
            if px.btn(px.KEY_Z) or px.btn(px.KEY_UP):
                self.deplacement(3)
            if px.btn(px.KEY_Q) or px.btn(px.KEY_LEFT):
                self.deplacement(0)
            if px.btn(px.KEY_S) or px.btn(px.KEY_DOWN):
                self.deplacement(2)
            if px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
                self.deplacement(1)
            if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5):
                self.balles.append(Bullet(px.frame_count % 4 + 3, [self.hb.x, self.hb.y], px.mouse_x, px.mouse_y))

    def draw_bullet(self):
        for tir in self.balles:
            tir.deplacement()
            tir.draw()
        j = 0
        while j < len(self.balles):
            if not 0 <= self.balles[j].pos[0] <= 128 and not 0 <= self.balles[j].pos[1] <= 128:
                del self.balles[j]
            j += 1

    def draw_font(self):
        px.blt(43, 16, 0, 43, 16, 12, 12)
        if len(self.decor) < 3 and px.rndi(0, 2):
            planete = [[12, 0, 0, 0, 200, 15, 15], [110, 0, 0, 0, 224, 39, 39], [64, 0, 0, 192, 38, 63, 63]]
            a = px.rndi(0, 2)
            self.decor.append(planete[a])
        if not px.frame_count % 5:
            for planete in self.decor:
                planete[0], planete[1] = planete[0] + 1, planete[1] + 1
            for vaisseau in self.ennemie:
                vaisseau.y += 1

    def vague(self):
        if len(self.ennemie) == 0:
            self.wave += 1
            for t, n in enemy_amount(self.wave).items():
                for _ in range(n):
                    self.ennemie.append(Enemy(px.rndi(20, 108), px.rndi(4, 16), t))

    def draw(self):
        if self.play.on:  # menu
            px.blt(20, 15, 0, 0, 32, 87, 39)
            self.play.draw()
        else:
            self.draw_font()
            for j in self.decor:
                px.blt(*j)
            try:
                for g in range(len(self.ennemie)):
                    self.ennemie[g].draw()
                    if self.hb & self.ennemie[g].hb:
                        self.nb_vie -= 1
                        if self.nb_vie == 0:
                            self.nb_vie = 3
                            self.decor = []
                            self.ennemie = []
                            self.wave = 1
                            self.play.toggle()
                            self.balles = []
                            self.hb = Hitbox(64, 100, 7, 6)
                            pyxel.mouse(self.play.on)
                        del self.ennemie[g]
                    for k in range(len(self.balles)):
                        if self.balles[k].hb & self.ennemie[g].hb:
                            del self.ennemie[g], self.balles[k]
                for i in range(self.nb_vie):  # affiche le nb de vie
                    px.blt(1 + 8 * i, 1, 0, 0, 18, 7, 6)
            except IndexError:
                pass
            self.vague()
            px.text(px.mouse_x, px.mouse_y, '+', 7)
            self.draw_bullet()
            px.blt(self.hb.x + 4, self.hb.y + 3, 0, 0, 0, 9, 7) # affiche le joeur


Game()
