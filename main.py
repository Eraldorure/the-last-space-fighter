"""The project's main file. It consists of multiple classes, each one representing a screen from the game, except for
the 'App' class that is used to link all the other ones."""

import pyxel as px
from random import randint

from code import functions as fn, gameplay as gp, interface as ui


class App:
    """The class tying all the other classes (aka pages or screens) so that it works as an unique application.
    This class is also the one running the Pyxel instance."""

    def __init__(self):
        self.menu = Menu()
        self.game_over = GameOver(0, 0)
        self.credits = Credits()
        self.game = Game()
        self.screen = self.menu

    def launch(self):
        px.init(128, 128, title="The Last Space Fighter", fps=60)
        px.load("resources/ndc.pyxres")
        px.mouse(True)
        px.run(self.update, self.draw)

    def update(self):
        self.screen.update()

    def draw(self):
        self.screen.draw()

    def end_game(self):
        self.game_over = GameOver(self.game.wave, self.game.score)
        self.game = Game()
        self.screen = self.game_over
        px.mouse(True)


class Menu:
    """Classe representing the game's home menu."""

    def __init__(self):
        self.btn_play = ui.Button(40, 70, 45, 11, "PLAY")
        self.btn_credits = ui.ClickableText(4, 119, "v1.0")
        self.btn_quit = ui.ClickableText(109, 119, "Quit")

    def update(self):
        if self.btn_play.is_pressed():
            app.screen = app.game
            px.mouse(False)
        elif self.btn_credits.is_pressed():
            app.screen = app.credits
        elif self.btn_quit.is_pressed():
            px.quit()

    def draw(self):
        px.cls(0)
        px.blt(20, 15, 0, 0, 32, 87, 40, 0)
        self.btn_play.draw()
        self.btn_quit.draw()
        self.btn_credits.draw()


class GameOver:
    """Classe representing the game's Game Over screen."""

    def __init__(self, wave: int, score: int):
        self.btn_menu = ui.Button(15, 90, 45, 11, "MENU")
        self.btn_restart = ui.Button(68, 90, 45, 11, "RETRY")
        self.wave = wave
        self.score = score

    def update(self):
        if self.btn_menu.is_pressed():
            app.screen = app.menu
        elif self.btn_restart.is_pressed():
            app.screen = app.game
            px.mouse(False)

    def draw(self):
        px.cls(0)
        px.blt(34, 18, 0, 0, 135, 60, 24, 0)
        px.text(30, 57, "Wave", 7)
        px.text(38 - fn.len_of_int(self.wave) * 2, 67, str(self.wave), 7)
        px.text(81, 57, "Score", 7)
        px.text(91 - fn.len_of_int(self.score) * 2, 67, str(self.score), 7)
        self.btn_menu.draw()
        self.btn_restart.draw()


class Credits:
    """Class representing the game's credit page."""

    def __init__(self):
        self.btn_menu = ui.ClickableText(77, 119, "Back to Menu")

    def update(self):
        if self.btn_menu.is_pressed():
            app.screen = app.menu

    def draw(self):
        px.cls(0)
        px.text(50, 4, "CREDITS", 9)
        px.line(4, 13, 123, 13, 5)
        px.text(4, 18, "Version : 1.0", 7)
        px.text(4, 27, "Development : Eraldor\n"
                       "              Magistro", 7)
        px.text(4, 42, "Visuals : The Nuit du Code\n"
                       "          Eraldor", 7)
        px.text(4, 69, "This project was realised\n"
                       "during the 2023 edition of the\n"
                       "Nuit du Code and this version\n"
                       "is an evolution of the\n"
                       "submitted work. The original\n"
                       "game can be found in the\n"
                       "project's GitHub repository.", 7)
        px.line(4, 114, 123, 114, 5)
        self.btn_menu.draw()


class Game:
    """Classe représentant le jeu lui-même."""

    def __init__(self):
        self.player = gp.Player(60, 110)
        self.enemies = []
        self.bullets = []
        self.ammo = 0
        self.max_ammo = 5
        self.wave = 0
        self.score = -100
        self.is_reloading = True

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5) and (self.player.x + 4 != px.mouse_x or self.player.y != px.mouse_y) and self.ammo > 0 and not self.is_reloading:
            self.bullets.append(gp.Bullet(self.player.x + 4, self.player.y, px.mouse_x, px.mouse_y))
            self.ammo -= 1
        if px.btn(px.KEY_Q) and self.player.x > 2:
            self.player.move_left(1)
        if px.btn(px.KEY_D) and self.player.x < 108:
            self.player.move_right(1)
        if px.btn(px.KEY_Z) and self.player.y > 9:
            self.player.move_up(1)
        if px.btn(px.KEY_S) and self.player.y < 119:
            self.player.move_down(1)

        if self.ammo < 1 and not self.is_reloading:
            self.is_reloading = True
        if self.is_reloading and self.ammo < self.max_ammo and px.frame_count % 1.5:
            self.ammo += 1
        elif self.ammo == self.max_ammo:
            self.is_reloading = False

        self.del_useless()
        if not self.enemies:
            self.next_wave()
        for enemy in self.enemies:
            enemy.move()
            if enemy.y > 128:  # The enemy goes out of the screen and is brought back to the top
                enemy.y = enemy.hb.y = -enemy.h
                enemy.t = 0
                enemy.__origin = enemy.x, enemy.y
            elif self.player.hb & enemy.hb:  # The enemy touches the player
                self.player.hp -= 1
                enemy.hp = enemy.death_score = 0
        for bullet in self.bullets:
            bullet.move()
            for enemy in self.enemies:
                if not bullet.is_deleted and enemy.hb.contains(bullet.x, bullet.y):  # A bullet touches an enemy
                    enemy.hp -= 1
                    bullet.delete()
            if not (0 < bullet.x < 128 and 0 < bullet.y < 128):
                bullet.delete()

        if self.player.hp < 1:
            app.end_game()

    def draw(self):
        px.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for i in range(self.player.hp):
            px.blt(2 + 8 * i, 1, 0, 0, 18, 7, 6, 0)
        self.player.draw()
        px.rectb(119, 64, 7, 62, 7)
        px.rect(120, 65, 5, round(fn.remap(0, self.max_ammo, 0, 60, self.ammo)), 10)
        px.text(119, 57, f"{self.ammo:02}", 7)
        px.text(107, 2, f"{self.score: 5}", 7)
        px.text(65 - 2 * int(fn.len_of_int(self.wave)), 2, str(self.wave), 7)
        px.text(px.mouse_x - 1, px.mouse_y - 2, "+", 7)

    def del_useless(self):
        """Method removing bullets marked as deleted as well as dead enemies."""
        i = len(self.bullets) - 1
        while i >= 0:
            if self.bullets[i].is_deleted:
                del self.bullets[i]
            i -= 1
        i = len(self.enemies) - 1
        while i >= 0:
            if self.enemies[i].is_dead:
                self.score += self.enemies[i].death_score
                del self.enemies[i]
            i -= 1

    def next_wave(self):
        """Methods making all the necessary steps to change wave, such as increasing the ammo, the score, the wave and
        generating enemies (following the fn.enemy_amount function)."""
        self.wave += 1
        self.score += 100
        if self.max_ammo < 95:
            self.max_ammo += 5
        elif self.max_ammo != 99:
            self.max_ammo = 99
        self.is_reloading = True
        new = fn.enemy_amount(self.wave)
        for model, amount in new.items():
            w, h = gp.Enemy.MODELS[model]["size"]
            for _ in range(amount):
                x = randint(2, 117 - w)
                y = randint(-2 * h, -h)
                self.enemies.append(gp.Enemy(x, y, x, y + 100, model))


app = App()
app.launch()
