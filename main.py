"""The project's main file. It consists of multiple classes, each one representing a screen from the game, except for
the 'App' class that is used to link all the other ones."""

import tomllib
import webbrowser
import pyxel as px
from random import randint
from configparser import ConfigParser
from code import functions as fn, gameplay as gp, interface as ui


class App:
    """The class tying all the other classes (aka pages or screens) so that it works as a unique application.
    This class is also the one running the Pyxel instance."""

    def __init__(self):
        self.game_over = GameOver(0, 0)
        self.menu = Menu()
        self.credits = Credits()
        self.game = Game()

        if settings["Info"]["first_launch"] == "True":
            self.screen = LicenseAgreement()
        else:
            self.screen = self.menu

    def launch(self):
        px.init(128, 128, title="The Last Space Fighter", fps=60)
        px.icon(["000000000", "000060000", "000070000", "B0076700B", "7067C7607", "796525697", "202999202", "000505000", "000000000"], 5, 0)
        px.load("./data/resources.pyxres")
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


def update_settings(*modifs: tuple[str, str, str]):
    for section, option, value in modifs:
        settings[section][option] = value
    with open("./data/config.ini", "w") as file:
        settings.write(file)


class Menu:
    """Classe representing the game's home menu."""

    def __init__(self):
        self.btn_play = ui.Button(40, 70, 45, 11, lang["Menu"]["play"])
        self.btn_credits = ui.ClickableText(4, 124, fn.shorten_version(settings["Info"]["version"], 2), v_align="bottom")
        self.btn_quit = ui.ClickableText(124, 124, lang["Menu"]["exit"], h_align="right", v_align="bottom")

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
        self.btn_credits.draw()
        self.btn_quit.draw()


class GameOver:
    """Classe representing the game's Game Over screen."""

    def __init__(self, wave: int, score: int):
        self.btn_menu = ui.Button(15, 90, 45, 11, lang["Over"]["menu"])
        self.btn_restart = ui.Button(68, 90, 45, 11, lang["Over"]["restart"])
        self.txt_wave = ui.Text(38, 57, lang["Over"]["wave"], h_align="center")
        self.txt_wave_count = ui.Text(38, 67, str(wave), h_align="center")
        self.txt_score = ui.Text(91, 57, lang["Over"]["score"], h_align="center")
        self.txt_score_count = ui.Text(91, 67, str(score), h_align="center")

    def update(self):
        if self.btn_menu.is_pressed():
            app.screen = app.menu
        elif self.btn_restart.is_pressed():
            app.screen = app.game
            px.mouse(False)

    def draw(self):
        px.cls(0)
        px.blt(34, 18, 0, 0, 135, 60, 24, 0)
        self.txt_wave.draw()
        self.txt_wave_count.draw()
        self.txt_score.draw()
        self.txt_score_count.draw()
        self.btn_menu.draw()
        self.btn_restart.draw()


class Credits:
    """Class representing the game's credit page."""

    def __init__(self):
        self.btn_menu = ui.ClickableText(124, 124, lang["Credits"]["menu"], h_align="right", v_align="bottom")
        self.btn_license = ui.ClickableText(4, 124, lang["Credits"]["license"], v_align="bottom")
        self.txt_title = ui.Text(64, 4, lang["Credits"]["title"], h_align="center")
        self.txt_version = ui.Text(4, 18, lang["Credits"]["version"].format(VER=settings["Info"]["version"]))
        self.txt_dev = ui.Text(4, 27, lang["Credits"]["dev"])
        self.txt_visuals = ui.Text(4, 42, lang["Credits"]["visuals"])
        self.txt_content = ui.Text(4, 110, lang["Credits"]["context"], 120, v_align="bottom")

    def update(self):
        if self.btn_menu.is_pressed():
            app.screen = app.menu
        elif self.btn_license.is_pressed():
            webbrowser.open("https://raw.githubusercontent.com/Eraldorure/the-last-space-fighter/main/LICENSE")

    def draw(self):
        px.cls(0)
        self.txt_title.draw(9)
        px.line(4, 13, 123, 13, 5)
        self.txt_version.draw()
        self.txt_dev.draw()
        self.txt_visuals.draw()
        self.txt_content.draw()
        px.line(4, 114, 123, 114, 5)
        self.btn_menu.draw()
        self.btn_license.draw()


class LicenseAgreement:
    """Class representing the game's license agreement page.
    This page is only triggered when the game is launched for the first time."""

    def __init__(self):
        self.btn_agree = ui.Button(4, 104, 120, 11, lang["License"]["agree"])
        self.btn_refuse = ui.ClickableText(124, 124, lang["License"]["refuse"], h_align="right", v_align="bottom")
        self.btn_license = ui.ClickableText(4, 124, lang["License"]["license"], v_align="bottom")
        self.txt_title = ui.Text(64, 4, lang["License"]["title"], h_align="center")
        self.txt_parag1 = ui.Text(4, 18, lang["License"]["parag1"], 120)
        self.txt_parag2 = ui.Text(4, 33, lang["License"]["parag2"], 120)
        self.txt_parag3 = ui.Text(4, 78, lang["License"]["parag3"], 120)

    def update(self):
        if self.btn_agree.is_pressed():
            app.screen = app.menu
            update_settings(("Info", "first_launch", "False"))
        elif self.btn_refuse.is_pressed():
            px.quit()
        elif self.btn_license.is_pressed():
            webbrowser.open("https://raw.githubusercontent.com/Eraldorure/the-last-space-fighter/main/LICENSE")

    def draw(self):
        px.cls(0)
        self.txt_title.draw(9)
        px.line(4, 13, 123, 13, 5)
        self.txt_parag1.draw()
        self.txt_parag2.draw()
        self.txt_parag3.draw()
        px.line(4, 99, 123, 99, 5)
        self.btn_agree.draw()
        self.btn_refuse.draw()
        self.btn_license.draw()


class Game:
    """Class representing the game itself."""

    def __init__(self):
        self.player = gp.Player(60, 110)
        self.enemies = []
        self.bullets = []
        self.ammo = 0
        self.max_ammo = 5
        self.wave = 0
        self.score = -100
        self.is_reloading = True
        self.txt_wave_count = ui.Text(64, 2, "1", h_align="center")
        self.txt_score_count = ui.Text(126, 2, "0", h_align="right")

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5) and (self.player.x + 4 != px.mouse_x or self.player.y != px.mouse_y) and self.ammo > 0 and not self.is_reloading:
            self.bullets.append(gp.Bullet(self.player.x + 4, self.player.y, px.mouse_x, px.mouse_y))
            self.ammo -= 1
        if (px.btn(px.KEY_Q) or px.btn(px.KEY_A)) and self.player.x > 2:
            self.player.move_left(1)
        if px.btn(px.KEY_D) and self.player.x < 108:
            self.player.move_right(1)
        if (px.btn(px.KEY_Z) or px.btn(px.KEY_W)) and self.player.y > 9:
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
        self.txt_wave_count.draw()
        self.txt_score_count.draw()
        px.text(px.mouse_x - 1, px.mouse_y - 2, "+", 7)

    def change_score(self, value: int):
        """Adds the given value to the score. If the value is negative, the score will be decreased."""
        self.score += value
        self.txt_score_count = ui.Text(126, 2, str(self.score), h_align="right")

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
                self.change_score(self.enemies[i].death_score)
                del self.enemies[i]
            i -= 1

    def next_wave(self):
        """Methods making all the necessary steps to change wave, such as increasing the ammo, the score, the wave and
        generating enemies (following the fn.enemy_amount function)."""
        self.wave += 1
        self.txt_wave_count = ui.Text(64, 2, str(self.wave), h_align="center")
        self.change_score(100)
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


if __name__ == '__main__':
    settings = ConfigParser(allow_no_value=True, comment_prefixes="/")
    settings.read("./data/config.ini")

    with open(f"./data/languages/{settings['Options']['language']}.toml", "rb") as file:
        lang = tomllib.load(file)

    app = App()
    app.launch()
