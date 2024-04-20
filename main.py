"""Le fichier principal du projet. Celui-ci consiste en plusieurs classes, chacune représentant une page de
l'application, exception faite de la classe 'App' qui sert ici de classe principale."""

import pyxel as px
from random import randint

from code import functions as fn, gameplay as gp, interface as ui


class App:
    """Classe permettant de lier toutes les classes (aka pages) de l'application.
    C'est également dans celle-ci que Pyxel fonctionne."""

    def __init__(self):
        px.init(128, 128, title="The Last Space Fighter", fps=60)
        px.load("ndc.pyxres")
        self.current_screen = 0  # 0 = Menu, 1 = Game, 2 = GameOver, 3 = Credits
        self.menu = Menu()
        self.game = Game()
        self.over = GameOver()
        self.credits = Credits()
        px.run(self.update, self.draw)

    def update(self):
        if self.current_screen == 1:  # Game
            self.game.update()
            if self.game.is_game_over:
                self.current_screen = 2
                self.over = GameOver(self.game.wave, self.game.score)
                self.game = Game()
                px.mouse(True)
        elif self.current_screen == 2:  # GameOver
            self.over.update()
            if self.over.btn_menu.is_pressed():
                self.current_screen = 0
            elif self.over.btn_restart.is_pressed():
                self.current_screen = 1
                px.mouse(False)
        elif self.current_screen == 3:  # Credits
            self.credits.update()
            if self.credits.btn_menu.is_pressed():
                self.current_screen = 0
        else:  # Menu
            self.menu.update()
            if self.menu.btn_play.is_pressed():
                self.current_screen = 1
                px.mouse(False)
            elif self.menu.btn_credits.is_pressed():
                self.current_screen = 3

    def draw(self):
        if self.current_screen == 1:
            self.game.draw()
        elif self.current_screen == 2:
            self.over.draw()
        elif self.current_screen == 3:
            self.credits.draw()
        else:
            self.menu.draw()


class Menu:
    """Classe représentant le menu d'accueil du jeu."""

    def __init__(self):
        self.btn_play = ui.Button(40, 68, 45, 11, "JOUER")
        self.btn_quit = ui.ClickableText(97, 119, "Quitter")
        self.btn_credits = ui.ClickableText(4, 119, "v1.0")
        px.mouse(True)

    def update(self):
        if self.btn_quit.is_pressed():
            px.quit()

    def draw(self):
        px.cls(0)
        px.blt(20, 15, 0, 0, 32, 87, 39, 0)
        self.btn_play.draw()
        self.btn_quit.draw()
        self.btn_credits.draw()


class GameOver:
    """Classe représentant l'écran de Game Over du jeu."""

    def __init__(self, wave: int = 0, score: int = 0):
        self.btn_menu = ui.Button(10, 80, 50, 11, "MENU")
        self.btn_restart = ui.Button(68, 80, 50, 11, "REESSAYER")
        self.col_game = 9
        self.col_over = 2
        self.wave = wave
        self.score = score
        self.__start_frame_count = px.frame_count
        px.mouse(True)

    def update(self):
        if not (px.frame_count - self.__start_frame_count) % 40:
            self.col_game, self.col_over = self.col_over, self.col_game

    def draw(self):
        px.cls(0)
        px.text(45, 12, "GAME", self.col_game)
        px.text(68, 12, "OVER", self.col_over)
        px.line(16, 30, 111, 30, 1)
        px.text(45, 44, "Wave", 7)
        px.text(68, 44, f"{self.wave:04}", 7)
        px.text(41, 54, "Score", 7)
        px.text(68, 54, f"{self.score:05}", 7)
        self.btn_menu.draw()
        self.btn_restart.draw()


class Credits:
    """Classe représentant la page des crédits du jeu."""

    def __init__(self):
        self.btn_menu = ui.ClickableText(69, 119, "Retour au menu")

    def update(self):
        pass

    def draw(self):
        px.cls(0)
        px.text(50, 4, "CREDITS", 9)
        px.line(4, 13, 123, 13, 1)
        px.text(4, 18, "Version : 1.0", 7)
        px.text(4, 27, "Developpement : Eraldor\n"
                       "                Magistro", 7)
        px.text(4, 42, "Graphismes : La Nuit du Code", 7)
        px.text(4, 75, "Ce projet a ete realise dans\n"
                       "le cadre de la Nuit du Code\n"
                       "2023 et cette version est une\n"
                       "evolution du travail rendu.\n"
                       "Le jeu originel est trouvable\n"
                       "via le depot GitHub du projet.", 7)
        px.line(4, 114, 123, 114, 1)
        self.btn_menu.draw()


class Game:
    """Classe représentant le jeu lui-même."""

    def __init__(self):
        self.player = gp.Player(60, 110)
        self.enemies = []
        self.bullets = []
        self.wave = 0
        self.score = -100
        self.is_game_over = False

    def update(self):
        if px.btnp(px.MOUSE_BUTTON_LEFT, repeat=5) and (self.player.x + 4 != px.mouse_x or self.player.y != px.mouse_y):
            self.bullets.append(gp.Bullet(self.player.x + 4, self.player.y, px.mouse_x, px.mouse_y))
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
            enemy.move()
            if enemy.y > 128:  # l'ennemi sort de l'écran et est ramené en haut
                enemy.y = enemy.hb.y = -enemy.h
                enemy.t = 0
                enemy.__origin = enemy.x, enemy.y
            elif self.player.hb & enemy.hb:  # l'ennemi touche le joueur
                self.player.hp -= 1
                enemy.hp = enemy.death_score = 0
        for bullet in self.bullets:
            bullet.move()
            for enemy in self.enemies:
                if not bullet.used and enemy.hb.contains(bullet.x, bullet.y):  # un tir touche un ennemi
                    enemy.hp -= 1
                    bullet.used = True
            if not (0 < bullet.x < 128 and 0 < bullet.y < 128):
                bullet.used = True
        self.is_game_over = self.player.hp < 1

    def draw(self):
        px.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for i in range(self.player.hp):
            px.blt(2 + 8 * i, 1, 0, 0, 18, 7, 6, 0)
        self.player.draw()
        px.text(107, 2, f"{self.score: 5}", 7)
        px.text(65 - 2 * int(fn.len_of_int(self.wave)), 2, str(self.wave), 7)
        px.text(px.mouse_x - 1, px.mouse_y - 2, "+", 7)

    def del_useless(self):
        """Méthode permettant de supprimer les objets inutiles tels que les ennemis morts ou les tirs sortis de l'écran."""
        i = len(self.bullets) - 1
        while i >= 0:
            if self.bullets[i].used:
                del self.bullets[i]
            i -= 1
        i = len(self.enemies) - 1
        while i >= 0:
            if self.enemies[i].is_dead:
                self.score += self.enemies[i].death_score
                del self.enemies[i]
            i -= 1

    def next_wave(self):
        """Méthode permettant de passer à la vague suivante. S'occupe également de créer les ennemis."""
        self.wave += 1
        self.score += 100
        new = fn.enemy_amount(self.wave)
        for model, amount in new.items():
            w, h = gp.Enemy.MODELS[model]["size"]
            for _ in range(amount):
                x = randint(2, 126 - w)
                y = randint(-2 * h, -h)
                self.enemies.append(gp.Enemy(x, y, x, y + 100, model))


App()
