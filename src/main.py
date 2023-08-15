import sys

import pygame

from audio.audio_manager import AudioManager
from data.level_data import levels
from levels.base import Level
from levels.overworld import Overworld
from settings import AUDIO_PATH, BLACK_COLOR, FPS, HEIGHT, ICONS_PATH, WIDTH


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Archivist Adventure 2")
        icon = pygame.image.load(ICONS_PATH / "icon.ico")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        # game attributes
        self.max_level = 1
        self.current_level = 0

        # sound
        self.audio_manager = AudioManager()
        self.audio_manager.play_overworld_music()

        # overworld creation
        self.overworld = Overworld(
            self.current_level, self.max_level, self.screen, self.create_level
        )
        self.status = "overworld"

    def create_level(self, selected_level):
        self.level = Level(stage=selected_level)
        self.status = "level"
        level_music_path = levels[selected_level]["bg_music"]
        self.audio_manager.play_level_music(level_music_path)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK_COLOR)

            if self.status == "overworld":
                self.overworld.run()
            else:
                self.level.run()
                if self.level.finished:
                    self.audio_manager.play_overworld_music()
                    self.status = "overworld"
                    del self.level

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
