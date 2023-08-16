import sys

import pygame

from settings import HEIGHT, WIDTH


class PauseMenu:
    def __init__(self, display_surface, input_handler):
        self.display_surface = display_surface
        self.input_handler = input_handler
        self.game_paused = False
        self.finished = False

    def draw(self):
        font = pygame.font.Font(None, 36)
        options = ["Continue", "Main Menu", "Quit"]
        for index, option in enumerate(options):
            color = (255, 255, 255) if index != self.input_handler.menu_option else (255, 0, 0)
            text = font.render(option, True, color)
            self.display_surface.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2 + index * 40,
                ),
            )

    def handle(self):
        actions = self.input_handler.handle_pause_input()
        if actions["next_option"]:
            self.input_handler.menu_option = (self.input_handler.menu_option + 1) % 3
        elif actions["previous_option"]:
            self.input_handler.menu_option = (self.input_handler.menu_option - 1) % 3
        elif actions["select_option"]:
            # Continue game
            if self.input_handler.menu_option == 0:
                self.toggle()
            # Switch back to overworld view
            elif self.input_handler.menu_option == 1:
                self.game_paused = False
                self.finished = True
            # Quit game
            elif self.input_handler.menu_option == 2:
                pygame.quit()
                sys.exit()
