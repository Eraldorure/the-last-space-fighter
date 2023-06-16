import pyxel as px

import objects as obj
import functions as func


class Game:
    def __init__(self):
        self.hb = obj.Hitbox(64, 100, 7, 6)
        self.play = obj.Button(45, 64, 35, 10, "PLAY")
        self.bullets = []
        self.direction = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.hp = 3
        self.background = []
        self.ennemies = []
        self.wave = 1
        px.init(128, 128, title="NDC 2023", fps=60)
        px.load("ndc.pyxres")
        px.mouse(True)
        px.run(self.update, self.draw)

    def move(self, d):
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
                self.move(3)
            if px.btn(px.KEY_Q) or px.btn(px.KEY_LEFT):
                self.move(0)
            if px.btn(px.KEY_S) or px.btn(px.KEY_DOWN):
                self.move(2)
            if px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
                self.move(1)
            if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5):
                self.bullets.append(obj.Bullet(px.frame_count % 4 + 3, [self.hb.x, self.hb.y], px.mouse_x, px.mouse_y))

    def draw_bullet(self):
        for tir in self.bullets:
            tir.move()
            tir.draw()
        j = 0
        while j < len(self.bullets):
            if not 0 <= self.bullets[j].pos[0] <= 128 and not 0 <= self.bullets[j].pos[1] <= 128:
                del self.bullets[j]
            j += 1

    def draw_font(self):
        px.blt(43, 16, 0, 43, 16, 12, 12)
        if len(self.background) < 3 and px.rndi(0, 2):
            planete = [[12, 0, 0, 0, 200, 15, 15], [110, 0, 0, 0, 224, 39, 39], [64, 0, 0, 192, 38, 63, 63]]
            a = px.rndi(0, 2)
            self.background.append(planete[a])
        if not px.frame_count % 5:
            for planete in self.background:
                planete[0], planete[1] = planete[0] + 1, planete[1] + 1
            for vaisseau in self.ennemies:
                vaisseau.y += 1

    def vague(self):
        if len(self.ennemies) == 0:
            self.wave += 1
            for t, n in func.enemy_amount(self.wave).items():
                for _ in range(n):
                    self.ennemies.append(obj.Enemy(px.rndi(20, 108), px.rndi(4, 16), t))

    def draw(self):
        if self.play.on:  # menu
            px.blt(20, 15, 0, 0, 32, 87, 39)
            self.play.draw()
        else:
            self.draw_font()
            for j in self.background:
                px.blt(*j)
            try:
                for g in range(len(self.ennemies)):
                    self.ennemies[g].draw()
                    if self.hb & self.ennemies[g].hb:
                        self.hp -= 1
                        if self.hp == 0:
                            self.hp = 3
                            self.background = []
                            self.ennemies = []
                            self.wave = 1
                            self.play.toggle()
                            self.bullets = []
                            self.hb = obj.Hitbox(64, 100, 7, 6)
                            px.mouse(self.play.on)
                        del self.ennemies[g]
                    for k in range(len(self.bullets)):
                        if self.bullets[k].hb & self.ennemies[g].hb:
                            del self.ennemies[g], self.bullets[k]
                for i in range(self.hp):  # affiche le nb de vie
                    px.blt(1 + 8 * i, 1, 0, 0, 18, 7, 6)
            except IndexError:
                pass
            self.vague()
            px.text(px.mouse_x, px.mouse_y, '+', 7)
            self.draw_bullet()
            px.blt(self.hb.x + 4, self.hb.y + 3, 0, 0, 0, 9, 7) # affiche le joeur


Game()
