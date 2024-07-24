"""The project's main file. It consists of multiple classes, each one representing a screen from the game, except for
the 'App' class that is used to link all the other ones."""

import tomllib
import webbrowser
import pyxel as px
from random import randint
from configparser import ConfigParser
from code import gameplay as gp, interface as ui, update as up


def update_settings(*modifs: tuple[str, str, str]):
    """Updates the settings file with the given modifications."""

    for section, option, value in modifs:
        settings[section][option] = value
    with open("./data/config.ini", "w") as file:
        settings.write(file)


def load_language(var: dict):
    """Updates the language dictionary (the var argument) with the content of the language file."""

    def format_variables(value: dict):
        for key, val in value.items():
            if isinstance(val, dict):
                value[key] = format_variables(val)
            elif isinstance(val, str):
                value[key] = val.format(VER=settings["info"]["version"])
        return value

    try:
        with open(f"./data/languages/{settings['options']['language']}.toml", "rb") as file:
            var.update(format_variables(tomllib.load(file)))
    except FileNotFoundError:
        raise ValueError(f"unknown language '{settings['options']['language']}'")


class App:
    """The class tying all the other classes (aka pages or screens) so that it works as a unique application.
    This class is also the one running the Pyxel instance."""

    def __init__(self, skip_eula: bool = False):  # Arguments are for debug purposes only
        self.game_over = GameOver(0, 0)
        self.menu = Menu()
        self.credits = Credits()
        self.options = Options()
        self.game = Game()

        if settings["info"]["first_launch"] == "no" or skip_eula:
            self.screen = self.menu
        else:
            self.screen = LicenseAgreement()

    def launch(self):
        """Launches the Pyxel instance, and thus the game."""
        px.init(128, 128, title="The Last Space Fighter", fps=60)
        px.icon(["000000000", "000060000", "000070000", "B0076700B", "7067C7607", "796525697", "202999202", "000505000", "000000000"], 5, 0)
        px.load("./data/resources.pyxres")
        px.mouse(True)
        px.run(self.update, self.draw)

    def reload(self):
        """Reloads the application by reinitializing all the screens. Reloads the language as well."""
        load_language(lang)
        self.menu = Menu()
        self.credits = Credits()
        self.options = Options()
        self.game = Game()

    def end_game(self):
        """Ends the game by switching to the Game Over screen and resetting the game."""
        self.game_over = GameOver(self.game.wave, self.game.score)
        self.game = Game()
        self.screen = self.game_over
        px.mouse(True)

    def update(self):
        self.screen.update()

    def draw(self):
        self.screen.draw()


class Menu:
    """Classe representing the game's home menu."""

    def __init__(self):
        self.btn_play = ui.Button(41, 69, 47, 13, lang["menu"]["play"])
        self.btn_options = ui.ClickableText(64, 87, lang["menu"]["options"], h_align="center")
        self.btn_credits = ui.ClickableText(4, 124, up.Version.from_str(settings["info"]["version"]).shorten_str(2), v_align="bottom")
        self.btn_quit = ui.ClickableText(124, 124, lang["menu"]["exit"], h_align="right", v_align="bottom")

    def update(self):
        if self.btn_play.is_pressed():
            app.screen = app.game
            px.mouse(False)
        elif self.btn_credits.is_pressed():
            app.screen = app.credits
        elif self.btn_options.is_pressed():
            app.screen = app.options
        elif self.btn_quit.is_pressed():
            px.quit()

    def draw(self):
        px.cls(0)
        px.blt(21, 15, 0, 0, 32, 87, 40, 0)
        self.btn_play.draw()
        self.btn_credits.draw()
        self.btn_options.draw()
        self.btn_quit.draw()


class GameOver:
    """Classe representing the game's Game Over screen."""

    def __init__(self, wave: int, score: int):
        self.btn_menu = ui.Button(15, 90, 45, 11, lang["over"]["menu"])
        self.btn_restart = ui.Button(68, 90, 45, 11, lang["over"]["retry"])
        self.txt_wave = ui.Text(38, 57, lang["over"]["wave"], h_align="center")
        self.txt_wave_count = ui.Text(38, 67, str(wave), h_align="center")
        self.txt_score = ui.Text(91, 57, lang["over"]["score"], h_align="center")
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
        self.btn_menu = ui.ClickableText(124, 124, lang["credits"]["back"], h_align="right", v_align="bottom")
        self.btn_license = ui.ClickableText(4, 124, lang["credits"]["see_lic"], v_align="bottom")
        self.txt_title = ui.Text(64, 4, lang["credits"]["title"], h_align="center")
        self.txt_version = ui.Text(4, 18, lang["credits"]["ver"])
        self.txt_dev = ui.Text(4, 27, lang["credits"]["dev"])
        self.txt_visuals = ui.Text(4, 42, lang["credits"]["visu"])
        self.txt_content = ui.Text(4, 110, lang["credits"]["context"], 120, v_align="bottom")

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


class Options:
    """Class representing the customization screen.
    For now, it only allows for changing the language, but expect more to come."""

    def __init__(self):
        self.btn_apply = ui.ClickableText(124, 124, lang["options"]["apply"], h_align="right", v_align="bottom")
        self.btn_cancel = ui.ClickableText(4, 124, lang["options"]["cancel"], v_align="bottom")
        self.drop_lang = ui.DropdownSelector(64, 18, lang["options"]["lang"]["lang_select"], settings["options"]["language"])
        self.txt_title = ui.Text(64, 4, lang["options"]["title"], h_align="center")
        self.txt_lang = ui.Text(4, 18, lang["options"]["lang"]["lang"])

    def update(self):
        self.drop_lang.update()
        if self.btn_cancel.is_pressed():
            app.screen = app.menu
            app.options = Options()
        elif self.btn_apply.is_pressed():
            update_settings(("options", "language", self.drop_lang.selected))
            app.reload()
            app.screen = app.menu

    def draw(self):
        px.cls(0)
        self.txt_title.draw(9)
        px.line(4, 13, 123, 13, 5)
        self.txt_lang.draw()
        self.drop_lang.draw()
        px.line(4, 114, 123, 114, 5)
        self.btn_apply.draw()
        self.btn_cancel.draw()


class LicenseAgreement:
    """Class representing the game's license agreement page.
    This page is only triggered when the game is launched for the first time."""

    def __init__(self):
        self.btn_agree = ui.Button(4, 104, 120, 11, lang["license"]["yes"])
        self.btn_refuse = ui.ClickableText(124, 124, lang["license"]["no"], h_align="right", v_align="bottom")
        self.btn_license = ui.ClickableText(4, 124, lang["license"]["see_lic"], v_align="bottom")
        self.txt_title = ui.Text(64, 4, lang["license"]["title"], h_align="center")
        self.txt_parag1 = ui.Text(4, 18, lang["license"]["p1"], 120)
        self.txt_parag2 = ui.Text(4, 33, lang["license"]["p2"], 120)
        self.txt_parag3 = ui.Text(4, 78, lang["license"]["p3"], 120)

    def update(self):
        if self.btn_agree.is_pressed():
            app.screen = app.menu
            update_settings(("info", "first_launch", "no"))
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
        self.wave = 0
        self.score = -100  # So the score is 0 at the beginning (since new wave = +100)
        self.txt_wave_count = ui.Text(64, 2, "1", h_align="center")
        self.txt_score_count = ui.Text(126, 2, "0", h_align="right")

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5) and (self.player.x + 4 != px.mouse_x or self.player.y != px.mouse_y):
            self.bullets.append(gp.Bullet(self.player.x + 4, self.player.y, px.mouse_x, px.mouse_y))
        if (px.btn(px.KEY_Q) or px.btn(px.KEY_A)) and self.player.x > 2:
            self.player.move_left()
        if px.btn(px.KEY_D) and self.player.x < 117:
            self.player.move_right()
        if (px.btn(px.KEY_Z) or px.btn(px.KEY_W)) and self.player.y > 9:
            self.player.move_up()
        if px.btn(px.KEY_S) and self.player.y < 119:
            self.player.move_down()

        self.del_useless()
        if not self.enemies:
            self.next_wave()
        for enemy in self.enemies:
            enemy.move(self.player.x + 4, self.player.y + 3)
            if self.player.hb & enemy.hb:  # The enemy touches the player
                self.player.hp -= 1
                enemy.delete()
        for bullet in self.bullets:
            bullet.move()
            for enemy in self.enemies:
                if not bullet.is_deleted and enemy.hb.contains(bullet.x, bullet.y):  # A bullet touches an enemy
                    enemy.hurt(1)
                    bullet.delete()
            if not (0 < bullet.x < 128 and 0 < bullet.y < 128):
                bullet.delete()

        if self.player.is_dead:
            app.end_game()  # Will change screen and reset the game

    def draw(self):
        px.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for i in range(self.player.hp):
            px.blt(2 + 8 * i, 1, 0, 0, 18, 7, 6, 0)  # The hearts symbolising the player's health
        self.player.draw()
        self.txt_wave_count.draw()
        self.txt_score_count.draw()
        px.blt(px.mouse_x - 2, px.mouse_y - 2, 0, 8, 19, 5, 5, 3)

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
                self.change_score(self.enemies[i].score)
                del self.enemies[i]
            i -= 1

    def next_wave(self):
        """This method makes all the necessary steps to change wave, such as increasing the score, the wave counter and
        generating enemies."""
        self.wave += 1
        self.txt_wave_count = ui.Text(64, 2, str(self.wave), h_align="center")
        self.change_score(100)

        for _ in range(0 if self.wave < 10 else int(1.2 * px.sqrt(self.wave - 10)) + randint(-1, 1)):
            self.enemies.append(gp.LargeEnemy(randint(2, 57), randint(-60, -30)))
        for _ in range(int(1.5 - 1.5 * px.cos(25 * self.wave) + self.wave / randint(8, 16))):
            self.enemies.append(gp.MediumEnemy(randint(2, 102), randint(-30, -15)))
        for _ in range(int(6 - 8 / (self.wave + 1))):
            self.enemies.append(gp.SmallEnemy(randint(2, 106), randint(-22, -11)))


settings = ConfigParser(allow_no_value=True, comment_prefixes="/")
settings.read("./data/config.ini")

lang = {}
load_language(lang)

app = App()

if __name__ == '__main__':
    app.launch()
