import pyxel as px

import objects as obj
import functions as func


class App:
    def __init__(self):
        px.init(128, 128, title="Space Shooté", fps=60)
        px.load("ndc.pyxres")
        self.current = "menu"
        self.menu = Menu()
        self.game = Game()
        px.run(self.update, self.draw)

    def update(self):
        if px.btn(px.KEY_CTRL) and px.btnp(px.KEY_TAB):
            self.switch_mode()
        if self.current == "menu":
            self.menu.update()
            if self.menu.launch:
                self.switch_mode()
        else:
            self.game.update()
            # if player_death then switch_mode()

    def draw(self):
        if self.current == "menu":
            self.menu.draw()
        else:
            self.game.draw()

    def switch_mode(self):
        if self.current == "menu":
            self.current = "game"
            self.menu.launch = False
            # px.mouse(False)
        else:
            self.current = "menu"
            self.game = Game()
            px.mouse(True)


class Menu:
    def __init__(self):
        self.launch = False
        self.play = obj.Button(45, 64, 35, 11, "PLAY")
        px.mouse(True)

    def update(self):
        if self.play.is_pressed():
            self.launch = True

    def draw(self):
        px.cls(0)
        px.blt(20, 15, 0, 0, 32, 87, 39, 0)
        self.play.draw()


class Game:
    def __init__(self):
        self.player = obj.Player(60, 110)
        self.enemies = [obj.Enemy(5, 5, "small"), obj.Enemy(35, 5, "normal"), obj.Enemy(75, 5, "big")]
        self.bullets = []
        self.wave = 1
        self.hb = obj.Hitbox(0, 0, 128, 128)

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5) and (self.player.x + 4 != px.mouse_x or self.player.y != px.mouse_y):
            self.bullets.append(obj.Bullet(7, self.player.x + 4, self.player.y, px.mouse_x, px.mouse_y))
        if px.btnp(px.KEY_R):
            self.bullets.clear()
        if px.btn(px.KEY_Q):
            self.player.move_left(1)
        if px.btn(px.KEY_D):
            self.player.move_right(1)
        if px.btn(px.KEY_Z):
            self.player.move_up(1)
        if px.btn(px.KEY_S):
            self.player.move_down(1)

        for bullet in self.bullets:
            bullet.move()
            for enemy in self.enemies:
                if not bullet.used and enemy.hb.contains(bullet.x, bullet.y):
                    enemy.harm(1)
                    bullet.used = True
            if not self.hb.contains(bullet.x, bullet.y):
                bullet.used = True
        self.del_useless()

    def draw(self):
        px.cls(0)
        for enemy in self.enemies:
            # enemy.hb.draw(8)
            enemy.draw()
        for bullet in self.bullets:
            # bullet.hb.draw(10)
            bullet.draw()
        # self.player.hb.draw(1)
        self.player.draw()
        px.text(5, 30, " ".join(str(enemy.hp) for enemy in self.enemies), 7)

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


App()
