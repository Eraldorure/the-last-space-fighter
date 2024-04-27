# Nuit du Code 2023 : Space Fighter


## Jeu

Le but du jeu est simplement d'avoir le meilleur score possible.

### Gameplay

Contrairement à un Space Fighter classique, le joueur peut se déplacer dans toutes les directions en utilisant les touches ZQSD.

Pour ce qui est de tirer, il suffit de cliquer (inutile de spammer, rester appuyé fonctionne tout aussi bien).
Le joueur possède une jauge de munitions qui se vide au fur et à mesure que celui-ci tire.
Dès que la jauge est vide, le joueur ne peut plus tirer et doit attendre qu'elle se recharge.
La quantité maximale de munitions présentes dans la jauge commence à 10, augmente de 5 à chaque vague et est majorée par 99.

Vous possédez 3 vies, mais entrer en collision avec des ennemis vous en fera perdre une à chaque fois.
Si vous perdez toutes vos vies, c'est le Game Over et la partie est terminée.

### Score

Le système de score fonctionne comme suit :
- Vous gagnez 100 points après chaque passage à la vague suivante.
- Aucun point n'est perdu lorsque le joueur se fait toucher par un ennemi.
- Lors de la mort d'un ennemi, les points récupérés sont équivalents aux PV de départ de cet ennemi.  
  *Les ennemis qui touchent le joueur sont automatiquement éliminés et ne rapportent aucun point.*


### Prérequis

Pour jouer à ce jeu, vous aurez besoin de :
- [Python](https://www.python.org/downloads/) (version minimale requise inconnue)
- [Pyxel](https://pypi.org/project/pyxel/) version 2.0.0 ou supérieure (installable via la commande `pip install pyxel`)
- Clavier et souris

Il n'est bien entendu pas nécessaire d'avoir un ordinateur performant, Pyxel étant un module léger et peu gourmand en ressources.


## Développement

### Versions futures

Une roadmap envisageable serait la suivante (sachant que l'ordre n'est pas fixe et les idées non définitives) :
- `v1.0` : Version actuelle du jeu, avec un gameplay relativement basique.
- `v1.1` : Système de paramètres, menu de pause, personnalisation des options et enregistrement du meilleur score.
- `v1.2` : Système de son (SFX et potentiellement musique).
- `v1.3` : Combats de boss, accompagné d'un système de buffs et débuffs.

### Bugs et idées

Si vous rencontrez des bugs ou avez des idées d'améliorations, n'hésitez pas à les signaler dans les [issues du projet](https://github.com/Eraldorure/ndc-space-fighter/issues).

### Crédits

Ce projet a été réalisé dans le cadre de l'édition 2023 de la [Nuit du Code](https://nuitducode.net), organisée par l'association éponyme.
Conséquemment, ce jeu est la propriété des personnes et entités suivantes :
- Thibaud C. ([@Eraldorure](https://github.com/Eraldorure))
- Romain G. ([@Poulouc](https://github.com/Poulouc))
- La [Nuit du Code](https://nuitducode.net)
