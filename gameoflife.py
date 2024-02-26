import argparse
import pygame
import logging
import random

# Configuration du système de logging pour capturer et enregistrer les événements d'exécution du programme.
logging.basicConfig(level=logging.INFO)

class Cell:
    """
    Classe représentant une cellule individuelle dans le jeu de la vie.
    
    Attributs:
        x (int): Position en x (horizontale) de la cellule sur la grille.
        y (int): Position en y (verticale) de la cellule sur la grille.
        alive (bool): État de la cellule, vivante (True) ou morte (False).
    """
    def __init__(self, x, y, alive=False):
        self.x = x
        self.y = y
        self.alive = alive

    def __str__(self):
        # Retourne une représentation en chaîne de caractères de la cellule.
        return f"Cell({self.x}, {self.y}, {self.alive})"

class GameOfLife:
    """
    Classe principale du jeu de la vie, gérant la grille de cellules et les règles du jeu.
    
    Attributs:
        width (int): Largeur de la grille (nombre de cellules).
        height (int): Hauteur de la grille (nombre de cellules).
        cells (list): Grille de cellules représentée par une liste de listes de Cell.
    """
    def __init__(self, width, height):
        # Initialisation de la grille avec des cellules mortes.
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y, False) for y in range(height)] for x in range(width)]

    def load_state(self, file_path):
        """
        Charge l'état initial de la grille à partir d'un fichier.
        
        Args:
            file_path (str): Chemin d'accès au fichier contenant l'état initial.
        """
        logging.info(f"Loading state from {file_path}")
        with open(file_path, "r") as file:
            lines = file.readlines()
            for x, line in enumerate(lines):
                for y, state in enumerate(line.strip()):
                    self.cells[x][y].alive = bool(int(state))

    def save_state(self, file_path):
        """
        Sauvegarde l'état actuel de la grille dans un fichier.
        
        Args:
            file_path (str): Chemin d'accès au fichier de sortie.
        """
        logging.info(f"Saving state to {file_path}")
        with open(file_path, "w") as file:
            for row in self.cells:
                line = "".join(str(int(cell.alive)) for cell in row)
                file.write(line + "\n")

    def update_state(self):
        """
        Met à jour l'état de la grille en appliquant les règles du jeu de la vie.
        """
        new_cells = [[Cell(x, y) for y in range(self.height)] for x in range(self.width)]
        for x in range(self.width):
            for y in range(self.height):
                neighbors = self.count_neighbors(x, y)
                if self.cells[x][y].alive:
                    new_cells[x][y].alive = neighbors in [2, 3]
                else:
                    new_cells[x][y].alive = neighbors == 3
        self.cells = new_cells

    def count_neighbors(self, x, y):
        """
        Compte le nombre de voisins vivants d'une cellule.
        
        Args:
            x (int): Position en x de la cellule.
            y (int): Position en y de la cellule.
            
        Returns:
            int: Nombre de voisins vivants.
        """
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                nx, ny = x + i, y + j
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    count += self.cells[nx][ny].alive
        return count

class PygameDisplay:
    """
    Gère l'affichage graphique du jeu de la vie en utilisant Pygame.
    
    Args:
        game_of_life (GameOfLife): L'instance du jeu de la vie à afficher.
        width (int): Largeur de la fenêtre d'affichage en pixels.
        height (int): Hauteur de la fenêtre d'affichage en pixels.
        fps (int): Le nombre de frames par seconde pour réguler la vitesse de l'animation.
        display_steps (bool): Indique si l'affichage doit être mis à jour à chaque étape de la simulation.
    """
    def __init__(self, game_of_life, width, height, fps, display_steps):
        # Initialisation de l'affichage avec les paramètres donnés et préparation de l'écran et de l'horloge.
        self.game_of_life = game_of_life
        self.width = width
        self.height = height
        self.fps = fps
        self.display_steps = display_steps
        self.screen = None  # Sera initialisé avec pygame.display.set_mode
        self.clock = None   # Sera initialisé avec pygame.time.Clock

    def initialize(self):
        # Initialisation de Pygame, création de la fenêtre d'affichage et configuration de l'horloge.
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        # Dessine la grille de cellules sur l'écran, en coloriant différemment les cellules vivantes et mortes.
        cell_size = min(self.width // self.game_of_life.width, self.height // self.game_of_life.height)
        for x in range(self.game_of_life.width):
            for y in range(self.game_of_life.height):
                color = (0, 0, 0) if self.game_of_life.cells[x][y].alive else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    def run_simulation(self, steps):
        # Exécute la simulation pour un nombre donné d'étapes, en mettant à jour l'affichage à chaque étape si demandé.
        for _ in range(steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.game_of_life.update_state()
            if self.display_steps:
                self.draw_grid()
                pygame.display.flip()
                self.clock.tick(self.fps)

        if not self.display_steps:
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def close(self):
        # Ferme correctement Pygame.
        pygame.quit()



def main():
    # Initialisation du parseur d'arguments pour configurer la simulation via la ligne de commande.
    parser = argparse.ArgumentParser(description="Game of Life simulation with Pygame")
    
    # Ajout des options configurables par l'utilisateur.
    parser.add_argument("-i", "--input", type=str, default="input.txt", help="Path to the initial pattern file")
    parser.add_argument("-o", "--output", type=str, default="output.txt", help="Path to the output file")
    parser.add_argument("-m", "--steps", type=int, default=10, help="Number of steps to run when display is off")
    parser.add_argument("-d", "--display", action="store_true", default=True, help="Enable display with Pygame")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Number of frames per second with Pygame")
    parser.add_argument("--width", type=int, default=800, help="Initial width of the Pygame screen")
    parser.add_argument("--height", type=int, default=600, help="Initial height of the Pygame screen")

    # Analyse des arguments fournis par l'utilisateur.
    args = parser.parse_args()

    # Création d'une instance du jeu de la vie avec les dimensions spécifiées.
    game_of_life = GameOfLife(args.width // 10, args.height // 10)
    
    # Chargement de l'état initial du jeu à partir du fichier spécifié, si présent.
    if args.input:
        game_of_life.load_state(args.input)

    # Si l'affichage est activé, initialise et exécute la simulation avec affichage graphique.
    if args.display:
        display = PygameDisplay(game_of_life, args.width, args.height, args.fps, args.display)
        display.initialize()
        display.run_simulation(args.steps)
        game_of_life.save_state(args.output)  # Sauvegarde de l'état final après l'exécution de la simulation.
    else:
        # Exécution de la simulation sans affichage graphique.
        for _ in range(args.steps):
            game_of_life.update_state()
        game_of_life.save_state(args.output)  # Sauvegarde de l'état final.

# Point d'entrée du script Python, exécute la fonction main si le script est exécuté directement.
if __name__ == "__main__":
    main()
