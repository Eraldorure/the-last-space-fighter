# <img src="./icon.ico"/> The Last Space Fighter

The evolved version of our submission from the 2023 edition of the *Nuit du Code*.


## The game

Your goal, as a player, is to simply get the best score possible.

### Gameplay

Contrary to a regular Space Fighter, the player can move in all directions using the WASD keys (or ZQSD if you're a fellow Azerty user).

To shoot, you simply need to left-click (no need to spam, keep holding works just as well).
The player has a limited amount of ammunition, represented by a gauge at the bottom right of the screen.
As soon as the gauge is empty, the player will have to wait for it to refill before being able to shoot again.
The amount of ammunition is 10, increases by 5 every wave and stops growing at 99.

You have 3 lives, but colliding with an enemy will remove one of them.
The game is over as soon as you lose all your lives, and you will have to restart from the beginning.

### Scoring system

The scoring system follows these few rules:
- You gain 100 every time you go on to the next wave.
- No points are removed when you lose a life (aka when you are touched by an enemy).
- When an enemy is killed, the amount of points you gain is equivalent to the enemy's initial HP.  
  *Enemies who touch you are automatically removed and award you no points.*


### Minimum requirements

To play this game, you will need:
- [Python](https://www.python.org/downloads/) (unknown minium version, but assuredly works with 3.10 and higher)
- [Pyxel](https://pypi.org/project/pyxel/) version 2.1.4 or higher (installable using the `pip install -U pyxel` command)
- A mouse and a keyboard; controllers aren't (yet?) supported

Of course, it isn't necessary to have an overpowered computer to run this game. A potato PC should suffice.


## Development

### Future versions

The current roadmap is the following (subject to change):
- `v1.0`: Current version of the game, with a relatively simple gameplay.
- `v1.1`: Option customization, pause screens and local leaderboards.
- `v1.2`: Sound system (SFX and potentially music).
- `v1.3`: Boss fights and buff/debuffs.

### Bugs and ideas

If you encounter any bugs or have any feature request/idea, don't hesitate to report them in the [project issues](https://github.com/Eraldorure/ndc-space-fighter/issues).

### Credits

This game was first made during the 2023 edition of the [Nuit du Code](https://nuitducode.net) (website in French), organized by the eponymous association.

This project belongs to:
- Thibaud C. ([@Eraldorure](https://github.com/Eraldorure))
- Romain G. ([@Poulouc](https://github.com/Poulouc))

#### Licensing

This game is licensed under the GNU General Public License v3.0 (or GPLv3).
This means that you can freely use, modify and distribute this game, as long as you respect the license's terms, which are, in short: credit where credit is due, and keep the same license for your modifications.
For more details, you can read the full license in the [LICENSE](https://raw.githubusercontent.com/Eraldorure/the-last-space-fighter/main/LICENSE) file.
