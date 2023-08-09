import sys

import pygame

from level import Level
from settings import WIDTH, HEIGTH, ICONS_PATH, AUDIO_PATH, BLACK_COLOR, FPS


class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption("Archivist Adventure 2")
        self.clock = pygame.time.Clock()
        icon = pygame.image.load(ICONS_PATH / "icon.ico")
        pygame.display.set_icon(icon)

        self.level = Level(stage=1)

        # sound
        main_sound = pygame.mixer.Sound(AUDIO_PATH / "desert.ogg")
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
