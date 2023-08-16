# pause_menu.py

import pygame
from enum import Enum
import sys

from settings import HEIGHT, WIDTH


class MenuOption(Enum):
    CONTINUE = 0
    MAIN_MENU = 1
    QUIT = 2
    FINISHED = 3


class PauseMenu:
    def __init__(self, toggle_callback, input_handler):
        self.font = pygame.font.Font(None, 36)
        self.options = ["Continue", "Main Menu", "Quit"]
        self.option_list = [MenuOption.CONTINUE, MenuOption.MAIN_MENU, MenuOption.QUIT]
        self.display_surface = pygame.display.get_surface()
        self.input_handler = input_handler
        self.toggle_callback = toggle_callback

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
        option_actions = {
            MenuOption.CONTINUE: self.toggle_callback,
            MenuOption.MAIN_MENU: lambda: MenuOption.FINISHED,
            MenuOption.QUIT: lambda: sys.exit(),
        }

        if actions["next_option"]:
            current_index = self.option_list.index(MenuOption(self.input_handler.menu_option))
            self.input_handler.menu_option = self.option_list[
                (current_index + 1) % len(self.option_list)
            ].value
        elif actions["previous_option"]:
            current_index = self.option_list.index(MenuOption(self.input_handler.menu_option))
            self.input_handler.menu_option = self.option_list[
                (current_index - 1) % len(self.option_list)
            ].value
        elif actions["select_option"]:
            return option_actions[MenuOption(self.input_handler.menu_option)]()

    def run(self):
        self.draw()
        return self.handle_input()
