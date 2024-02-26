import argparse
import pygame
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)


class Cell:
    def __init__(self, x, y, alive=False):
        self.x = x
        self.y = y
        self.alive = alive

    def __str__(self):
        return f"Cell({self.x}, {self.y}, {self.alive})"


class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y, False) for y in range(height)] for x in range(width)]

    def load_state(self, file_path):
        logging.info(f"Loading state from {file_path}")
        with open(file_path, "r") as file:
            lines = file.readlines()
            for x, line in enumerate(lines):
                for y, state in enumerate(line.strip()):
                    self.cells[x][y].alive = bool(int(state))

    def save_state(self, file_path):
        logging.info(f"Saving state to {file_path}")
        with open(file_path, "w") as file:
            for row in self.cells:
                line = "".join(str(int(cell.alive)) for cell in row)
                file.write(line + "\n")

    def update_state(self):
        new_cells = [[Cell(x, y) for y in range(self.height)] for x in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                neighbors = self.count_neighbors(x, y)
                if self.cells[x][y].alive:
                    new_cells[x][y].alive = 2 <= neighbors <= 3
                else:
                    new_cells[x][y].alive = neighbors == 3

        self.cells = new_cells

    def count_neighbors(self, x, y):
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
    def __init__(self, game_of_life, width, height, fps, display_steps):
        self.game_of_life = game_of_life
        self.width = width
        self.height = height
        self.fps = fps
        self.display_steps = display_steps
        self.screen = None
        self.clock = None

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        self.clock = pygame.time.Clock()

    def draw_grid(self):
        cell_size = min(self.width // self.game_of_life.width, self.height // self.game_of_life.height)
        for x in range(self.game_of_life.width):
            for y in range(self.game_of_life.height):
                color = (0, 0, 0) if self.game_of_life.cells[x][y].alive else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

    def run_simulation(self, steps):
        for _ in range(steps):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

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
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Game of Life simulation with Pygame")
    parser.add_argument("-i", "--input", type=str, default="input.txt", help="Path to the initial pattern file")
    parser.add_argument("-o", "--output", type=str, default="output.txt", help="Path to the output file")
    parser.add_argument("-m", "--steps", type=int, default=10, help="Number of steps to run when display is off")
    parser.add_argument("-d", "--display", action="store_true",  default=True, help="Enable display with Pygame")
    parser.add_argument("-f", "--fps", type=int, default=10, help="Number of frames per second with Pygame")
    parser.add_argument("--width", type=int, default=800, help="Initial width of the Pygame screen")
    parser.add_argument("--height", type=int, default=600, help="Initial height of the Pygame screen")

    args = parser.parse_args()

    game_of_life = GameOfLife(args.width // 10, args.height // 10)
    if args.input:
        game_of_life.load_state(args.input)

    if args.display:
        display = PygameDisplay(game_of_life, args.width, args.height, args.fps, args.display)
        display.initialize()
        display.run_simulation(args.steps)
        game_of_life.save_state(args.output)
    else:
        for _ in range(args.steps):
            game_of_life.update_state()
        game_of_life.save_state(args.output)


if __name__ == "__main__":
    main()
