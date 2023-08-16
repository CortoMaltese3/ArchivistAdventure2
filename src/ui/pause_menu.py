# pause_menu.py

import pygame
import sys

from settings import HEIGHT, WIDTH
from user.input_handler import InputHandler

class PauseMenu:
    def __init__(self, toggle_callback):
        self.font = pygame.font.Font(None, 36)
        self.options = ["Continue", "Main Menu", "Quit"]
        self.display_surface = pygame.display.get_surface()
        self.input_handler = InputHandler()
        self.toggle_callback = toggle_callback  # This callback will be used to toggle the game's pause state.

    def draw(self):
        for index, option in enumerate(self.options):
            color = (255, 255, 255) if index != self.input_handler.menu_option else (255, 0, 0)
            text = self.font.render(option, True, color)
            self.display_surface.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2 + index * 40,
                ),
            )

    def handle_input(self):
        actions = self.input_handler.handle_pause_input()
        if actions["next_option"]:
            self.input_handler.menu_option = (self.input_handler.menu_option + 1) % 3
        elif actions["previous_option"]:
            self.input_handler.menu_option = (self.input_handler.menu_option - 1) % 3
        elif actions["select_option"]:
            if self.input_handler.menu_option == 0:
                self.toggle_callback()
            elif self.input_handler.menu_option == 1:
                return "finished"
            elif self.input_handler.menu_option == 2:
                pygame.quit()
                sys.exit()

    def run(self):
        self.draw()
        return self.handle_input()
