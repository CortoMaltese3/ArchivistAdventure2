import pygame
import sys
from level import Level
from overworld import Overworld 
from settings import WIDTH, HEIGHT, ICONS_PATH, AUDIO_PATH, BLACK_COLOR, FPS

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
        self.max_level = 2
        self.current_level = 0

        # sound
        main_sound = pygame.mixer.Sound(AUDIO_PATH / "desert.ogg")
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

        # overworld creation
        self.overworld = Overworld(self.current_level, self.max_level, self.screen, self.create_level)
        self.status = 'overworld'

    def create_level(self, selected_level):
        self.level = Level(stage=selected_level)
        self.status = 'level'

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill(BLACK_COLOR)

            if self.status == 'overworld':
                self.overworld.run()
            else:
                self.level.run()

            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
