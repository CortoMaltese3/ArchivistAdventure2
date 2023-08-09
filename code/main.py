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
        self.main_sound = pygame.mixer.Sound(AUDIO_PATH / "desert.ogg")
        self.overworld_sound = pygame.mixer.Sound(AUDIO_PATH / "overworld.ogg")  # Overworld music
        self.main_sound.set_volume(0.5)
        self.overworld_sound.set_volume(0.5)
        self.play_overworld_music()

        # overworld creation
        self.overworld = Overworld(self.current_level, self.max_level, self.screen, self.create_level)
        self.status = 'overworld'

    def play_overworld_music(self):
        self.main_sound.stop()  # Stop the level music
        self.overworld_sound.play(loops=-1)  # Play overworld music

    def play_level_music(self):
        self.overworld_sound.stop()  # Stop overworld music
        self.main_sound.play(loops=-1)  # Play level music

    def create_level(self, selected_level):
        self.level = Level(stage=selected_level)
        self.status = 'level'
        self.play_level_music()  # Switch to level music

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
