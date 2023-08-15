import sys

import pygame

from levels.manager import LevelManager
from settings import BLACK_COLOR, FPS, HEIGHT, ICONS_PATH, WIDTH


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Archivist Adventure 2")
        icon = pygame.image.load(ICONS_PATH / "icon.ico")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        self.level_manager = LevelManager(self.screen)
        self.level_manager.load_overworld()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK_COLOR)
            self.level_manager.run_current_level()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
