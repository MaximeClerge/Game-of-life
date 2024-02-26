# Game of Life

## Règles

Le jeu évolue à chaque tour (appelé "génération"), avec tous les changements effectués simultanément selon les règles suivantes :

1. **Naissance** : Une cellule morte avec exactement trois voisins vivants devient vivante (reproduction).
2. **Survie** : Une cellule vivante avec deux ou trois voisins vivants reste vivante pour la prochaine génération (stabilité).
3. **Mort** : Une cellule vivante avec moins de deux voisins vivants meurt de solitude, et une cellule vivante avec plus de trois voisins vivants meurt de surpopulation.

## Objectif du Projet

Ce projet vise à implémenter le Game of Life en Python, permettant aux utilisateurs de définir l'état initial du jeu et d'observer son évolution au fil des générations. Il utilise la bibliothèque Pygame pour l'affichage graphique, offrant une visualisation interactive de la simulation.

## Fonctionnalités

- **Chargement et sauvegarde d'états** : Les utilisateurs peuvent charger des états initiaux à partir de fichiers et sauvegarder l'état final de la simulation.
- **Affichage dynamique avec Pygame** : Visualisation en temps réel de l'évolution du jeu avec la possibilité de contrôler le nombre de générations et la vitesse de la simulation.
- **Gestion des arguments de ligne de commande** : Les utilisateurs peuvent spécifier des options telles que le fichier d'entrée/sortie, le nombre de générations, et activer/désactiver l'affichage graphique via des arguments de ligne de commande.

## Comment Utiliser

Voici comment exécuter le Game of Life :

```
python game_of_life.py -i input.txt -o output.txt -m 100 -d -f 10
```

- `-i input.txt` : spécifie le fichier contenant l'état initial.
- `-o output.txt` : spécifie le fichier où sauvegarder l'état final de la simulation.
- `-m 100` : définit le nombre de générations à simuler.
- `-d` : active l'affichage dynamique avec Pygame.
- `-f 10` : définit le nombre de frames par seconde pour l'affichage Pygame.

Link : https://pktraining.gitlab.io/python/python-class/life.html
