import sys

import pygame

from levels.manager import LevelManager
from settings import game_settings, paths


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((game_settings.WIDTH, game_settings.HEIGHT))
        pygame.display.set_caption(game_settings.CAPTION)
        icon = pygame.image.load(paths.FAVICON_PATH)
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

            self.screen.fill(game_settings.BLACK_COLOR)
            self.level_manager.run_current_level()
            pygame.display.update()
            self.clock.tick(game_settings.FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
