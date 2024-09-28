"""The project's main file. It consists of multiple classes, each one representing a screen from the game, except for
the 'App' class that is used to link all the other ones."""

import tomllib
import webbrowser
from random import randint
from configparser import ConfigParser

try:
    import pyxel as px
    from code import gameplay as gp, interface as ui, update as up
except ImportError as e:
    raise RuntimeError("some packages are lacking. Please run launch.py instead of directly calling game.py") from e


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

    def __init__(self, *, skip_eula: bool = False):  # Arguments are for debug purposes only
        self.game_over = GameOver(0, 0)
        self.menu = Menu()
        self.credits = Credits()
        self.options = Options()
        self.game = Game()

        if settings["info"]["accepted_eula"] == "yes" or skip_eula:
            self.screen = self.menu
        else:
            self.screen = LicenseAgreement()

    def launch(self):
        """Launches the Pyxel instance, and thus the game."""
        px.init(128, 128, title="The Last Space Fighter", fps=60)
        px.icon(["000000000", "000060000", "000070000", "B0076700B", "7067C7607", "796525697", "202999202", "000505000", "000000000"], 5, 0)
        px.load("./data/assets.pyxres")
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
        content = lang["menu"]
        self.btn_play = ui.Button(41, 69, 47, 13, content["play"])
        self.btn_options = ui.ClickableText(64, 87, content["options"], h_align="center")
        self.btn_credits = ui.ClickableText(4, 124, up.Version.from_str(settings["info"]["version"]).shorten_str(2), v_align="bottom")
        self.btn_quit = ui.ClickableText(124, 124, content["exit"], h_align="right", v_align="bottom")

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
        content = lang["over"]

        self.txt_wave = ui.Text(38, 57, content["wave"], h_align="center")
        self.txt_wave_count = ui.Text(38, 67, str(wave), h_align="center")

        self.txt_score = ui.Text(91, 57, content["score"], h_align="center")
        self.txt_score_count = ui.Text(91, 67, str(score), h_align="center")

        self.btn_menu = ui.Button(15, 90, 45, 11, content["menu"])
        self.btn_restart = ui.Button(68, 90, 45, 11, content["retry"])

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
        content = lang["credits"]
        self.txt_title = ui.Text(64, 4, content["title"], h_align="center")

        self.txt_version = ui.Text(4, 18, content["ver"])
        self.txt_dev = ui.Text(4, 27, content["dev"])
        self.txt_visuals = ui.Text(4, 42, content["visu"])
        self.txt_context = ui.Text(4, 110, content["context"], 120, v_align="bottom")

        self.btn_menu = ui.ClickableText(124, 124, content["back"], h_align="right", v_align="bottom")
        self.btn_license = ui.ClickableText(4, 124, content["see_lic"], v_align="bottom")

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
        self.txt_context.draw()
        px.line(4, 114, 123, 114, 5)
        self.btn_menu.draw()
        self.btn_license.draw()


class Options:
    """Class representing the customization screen.
    Currently, it allows to change the language and update the game, but there probably will be more options in the future."""

    def __init__(self):
        content = lang["options"]
        self.txt_title = ui.Text(64, 4, content["title"], h_align="center")

        self.txt_lang = ui.Text(4, 18, content["lang"]["lang"])
        self.drop_lang = ui.DropdownSelector(64, 18, content["lang"]["lang_select"], settings["options"]["language"])

        self.btn_check = ui.ClickableText(124, 110, content["update"]["check"], h_align="right", v_align="bottom")
        self.popup_yes = ui.Popup(14, 40, 100, 48, content["update"]["popup_yes"]["msg"],
                                  option_l=content["update"]["popup_yes"]["no"], option_r=content["update"]["popup_yes"]["yes"])
        self.popup_no = ui.Popup(14, 46, 100, 36, content["update"]["popup_no"]["msg"],
                                 option_r=content["update"]["popup_no"]["ok"])
        self.updater = up.Updater(up.Version.from_str(settings["info"]["version"]))

        self.btn_apply = ui.ClickableText(124, 124, content["apply"], h_align="right", v_align="bottom")
        self.btn_cancel = ui.ClickableText(4, 124, content["cancel"], v_align="bottom")

    def update(self):
        if self.popup_yes.visible:
            self.popup_yes.update()
            if self.popup_yes.btn_r.is_pressed():
                self.updater.install_update()
        elif self.popup_no.visible:
            self.popup_no.update()
        elif self.btn_cancel.is_pressed():
            app.screen = app.menu
            app.options = Options()
        elif self.btn_apply.is_pressed():
            update_settings(("options", "language", self.drop_lang.selected))
            app.reload()
            app.screen = app.menu
        elif self.btn_check.is_pressed():
            if self.updater.check_updates():
                self.popup_yes.toggle()
            else:
                self.popup_no.toggle()
        else:
            self.drop_lang.update()

    def draw(self):
        px.cls(0)
        self.txt_title.draw(9)
        px.line(4, 13, 123, 13, 5)
        self.txt_lang.draw()
        self.drop_lang.draw()
        self.btn_check.draw()
        self.popup_yes.draw()
        self.popup_no.draw()
        px.line(4, 114, 123, 114, 5)
        self.btn_apply.draw()
        self.btn_cancel.draw()


class LicenseAgreement:
    """Class representing the game's license agreement page.
    This page is only triggered when the game is launched for the first time."""

    def __init__(self):
        content = lang["license"]
        self.txt_title = ui.Text(64, 4, content["title"], h_align="center")

        self.txt_parag1 = ui.Text(4, 18, content["p1"], 120)
        self.txt_parag2 = ui.Text(4, 33, content["p2"], 120)
        self.txt_parag3 = ui.Text(4, 78, content["p3"], 120)

        self.btn_agree = ui.Button(4, 104, 120, 11, content["yes"])
        self.btn_refuse = ui.ClickableText(124, 124, content["no"], h_align="right", v_align="bottom")
        self.btn_license = ui.ClickableText(4, 124, content["see_lic"], v_align="bottom")

    def update(self):
        if self.btn_agree.is_pressed():
            app.screen = app.menu
            update_settings(("info", "accepted_eula", "yes"))
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
        self.txt_score_count.set_content(str(self.score))

    def del_useless(self):
        """Method removing bullets marked as deleted as well as dead enemies."""
        for i in range(len(self.bullets) - 1, -1, -1):
            if self.bullets[i].is_deleted:
                del self.bullets[i]
        for i in range(len(self.enemies) - 1, -1, -1):
            if self.enemies[i].is_dead:
                self.change_score(self.enemies[i].score)
                del self.enemies[i]

    def next_wave(self):
        """This method makes all the necessary steps to change wave, such as increasing the score, the wave counter and
        generating enemies."""
        self.wave += 1
        self.txt_wave_count.set_content(str(self.wave))
        self.change_score(100)

        for _ in range(0 if self.wave < 10 else int(1.2 * px.sqrt(self.wave - 10)) + randint(-1, 1)):
            self.enemies.append(gp.LargeEnemy(randint(2, 57), randint(-60, -30)))
        for _ in range(int(1.5 - 1.5 * px.cos(25 * self.wave) + self.wave / randint(8, 16))):
            self.enemies.append(gp.MediumEnemy(randint(2, 102), randint(-30, -15)))
        for _ in range(int(6 - 9 / (self.wave + 1))):
            self.enemies.append(gp.SmallEnemy(randint(2, 106), randint(-22, -11)))


settings = ConfigParser(allow_no_value=True, comment_prefixes="/")
settings.read("./data/config.ini")

lang = {}
load_language(lang)

app = App()
app.launch()
