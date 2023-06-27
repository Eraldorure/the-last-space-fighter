import pyxel as px
from random import randint

import objects as obj
import functions as func


class App:
    def __init__(self):
        px.init(128, 128, title="Space Shooté", fps=60)
        px.load("ndc.pyxres")
        self.current = "menu"
        self.menu = Menu()
        self.game = Game()
        self.over = GameOver()
        px.run(self.update, self.draw)

    def update(self):
        if self.current == "menu":
            self.menu.update()
            if self.menu.launch:
                self.current = "game"
                self.menu.launch = False
                px.mouse(False)
        elif self.current == "over":
            self.over.update()
            if self.over.menu:
                self.current = "menu"
            elif self.over.restart:
                self.current = "game"
                px.mouse(False)
        else:  # self.current == "game"
            self.game.update()
            if self.game.game_over:
                self.current = "over"
                self.over = GameOver(self.game.wave)
                self.game = Game()
                px.mouse(True)


    def draw(self):
        if self.current == "menu":
            self.menu.draw()
        elif self.current == "over":
            self.over.draw()
        else:
            self.game.draw()



class Menu:
    def __init__(self):
        self.launch = False
        self.play_btn = obj.Button(40, 68, 45, 11, "JOUER")
        px.mouse(True)

    def update(self):
        if self.play_btn.is_pressed():
            self.launch = True

    def draw(self):
        px.cls(0)
        px.blt(20, 15, 0, 0, 32, 87, 39, 0)
        self.play_btn.draw()
        px.text(91, 121, "v1.0-beta", 7)


class GameOver:
    def __init__(self, score: int = 0):
        self.menu = False
        self.restart = False
        self.menu_btn = obj.Button(10, 68, 50, 11, "MENU")
        self.restart_btn = obj.Button(68, 68, 50, 11, "RECOMMENCER")
        self.score = score
        px.mouse(True)

    def update(self):
        if self.restart_btn.is_pressed():
            self.restart = True
        elif self.menu_btn.is_pressed():
            self.menu = True

    def draw(self):
        px.cls(0)
        px.text(45, 16, "GAME", 9)
        px.text(68, 16, "OVER", 2)
        txt = f"Score  {self.score}"
        px.text(64 - 2 * len(txt) + 1, 35, txt, 7)
        self.menu_btn.draw()
        self.restart_btn.draw()


class Game:
    def __init__(self):
        self.player = obj.Player(60, 110)
        self.enemies = []
        self.bullets = []
        self.wave = 0
        self.game_over = False

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5) and (self.player.x + 4 != px.mouse_x or self.player.y != px.mouse_y):
            self.bullets.append(obj.Bullet(7, self.player.x + 4, self.player.y, px.mouse_x, px.mouse_y))
        if px.btn(px.KEY_Q) and self.player.x > 2:
            self.player.move_left(1)
        if px.btn(px.KEY_D) and self.player.x < 117:
            self.player.move_right(1)
        if px.btn(px.KEY_Z) and self.player.y > 9:
            self.player.move_up(1)
        if px.btn(px.KEY_S) and self.player.y < 119:
            self.player.move_down(1)

        self.del_useless()
        if not self.enemies:
            self.next_wave()
        for enemy in self.enemies:
            if self.player.hb & enemy.hb:
                self.player.hp -= 1
                enemy.hp = 0
        for bullet in self.bullets:
            bullet.move()
            for enemy in self.enemies:
                if not bullet.used and enemy.hb.contains(bullet.x, bullet.y):
                    enemy.harm(1)
                    bullet.used = True
            if not (0 < bullet.x < 128 and 0 < bullet.y < 128):
                bullet.used = True
        self.game_over = self.player.hp < 1

    def draw(self):
        px.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for i in range(self.player.hp):
            px.blt(2 + 8 * i, 1, 0, 0, 18, 7, 6, 0)
        self.player.draw()
        px.text(119, 2, f"{self.wave :2}", 7)
        px.text(px.mouse_x - 1, px.mouse_y - 2, "+", 7)

    def del_useless(self):
        i = len(self.bullets) - 1
        while i >= 0:
            if self.bullets[i].used:
                del self.bullets[i]
            i -= 1
        i = len(self.enemies) - 1
        while i >= 0:
            if self.enemies[i].is_dead:
                del self.enemies[i]
            i -= 1

    def next_wave(self):
        self.wave += 1
        new = func.enemy_amount(self.wave)
        for model, amount in new.items():
            width = obj.Enemy.MODELS[model]["size"][0]
            for _ in range(amount):
                self.enemies.append(obj.Enemy(randint(2, 126 - width), randint(9, 15), model))


App()
