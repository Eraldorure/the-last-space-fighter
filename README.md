# <img src="./icon.ico"/> The Last Space Fighter

The evolved version of our submission from the 2023 edition of the *Nuit du Code*.


## The game

Your goal, as a player, is to simply get the best score possible.

### Gameplay

Contrary to a regular Space Fighter, the player can move in all directions using the WASD keys (or ZQSD if you're a fellow Azerty user).
To shoot, you simply need to left-click (no need to spam, holding down works just as well).

You have 3 lives, but colliding with an enemy will remove one of them.
The game is over as soon as you lose all your lives, and you will have to restart from the beginning.

### Scoring system

The scoring system follows these few rules:
- You gain 100 points every time you go on to the next wave.
- When an enemy is killed, the amount of points you gain is equivalent to the enemy's initial HP.  
- Enemies who touch you are automatically removed and award you no points.
- No points are removed when you lose a life (aka when you are touched by an enemy).


### Minimum requirements

It isn't necessary to have an overpowered computer to run this game. A potato PC should suffice.

However, you will still need a few things for it to work:
- [Python](https://www.python.org/downloads/) version 3.11 or higher with at least *pip* and *venv* installed
- An internet connection to download the necessary libraries (only for the first launch) or to update the game
- A mouse and a keyboard since controllers aren't (yet?) supported


## Development

### Future versions

The current roadmap is the following (subject to change):
- `v1.0`: Current version of the game, with a relatively simple gameplay.
- `v1.1`: Further customization, pause screens and local leaderboards.
- `v1.2`: Visual effects, sound effects and potentially music.
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
The full license can be found in the [LICENSE](https://raw.githubusercontent.com/Eraldorure/the-last-space-fighter/main/LICENSE) file.

    Copyright (C) 2024  Thibaud C. and Romain G.
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
