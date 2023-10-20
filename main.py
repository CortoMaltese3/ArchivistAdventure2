import sys

import pygame

from src.data.manager import DatabaseManager
from src.data.provider import MagicDataProvider
from src.data.provider import WeaponDataProvider
from src.levels.manager import LevelManager
from src.settings import game_settings, paths


class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((game_settings.WIDTH, game_settings.HEIGHT))
        pygame.display.set_caption(game_settings.CAPTION)
        icon = pygame.image.load(paths.FAVICON_PATH)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        # Database setup
        self.db_manager = DatabaseManager()

        # Level setup
        self.level_manager = LevelManager(self.screen)
        self.level_manager.load_overworld()

    def initialize_db(self):
        db_manager = DatabaseManager()

        weapon_provider = WeaponDataProvider(db_manager)
        weapon_provider.initialize_data()

        magic_provider = MagicDataProvider(db_manager)
        magic_provider.initialize_data()

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
    # game.initialize_db()
    game.run()
