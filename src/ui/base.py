import pygame

from src.data.magic_data import magic_data
from src.data.weapon_data import weapon_data
from src.settings import game_settings, paths


class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(paths.UI_FONT_PATH, game_settings.UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(
            10, 10, game_settings.HEALTH_BAR_WIDTH, game_settings.BAR_HEIGHT
        )
        self.energy_bar_rect = pygame.Rect(
            10, 34, game_settings.ENERGY_BAR_WIDTH, game_settings.BAR_HEIGHT
        )

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon_name in weapon_data:
            weapon_info = weapon_data.get(weapon_name)
            path = weapon_info.get("graphic")
            weapon = {weapon_name: pygame.image.load(path).convert_alpha()}
            self.weapon_graphics.append(weapon)

        # convert magic dictionary
        self.magic_graphics = []
        for magic_name in magic_data:
            magic_info = magic_data.get(magic_name)
            path = magic_info.get("graphic")
            magic = {magic_name: pygame.image.load(path).convert_alpha()}
            self.magic_graphics.append(magic)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw bg
        pygame.draw.rect(self.display_surface, game_settings.UI_BG_COLOR, bg_rect)

        # converting stat to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, game_settings.UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, game_settings.TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, game_settings.UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(
            self.display_surface, game_settings.UI_BORDER_COLOR, text_rect.inflate(20, 20), 3
        )

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, game_settings.ITEM_BOX_SIZE, game_settings.ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, game_settings.UI_BG_COLOR, bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, game_settings.UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, game_settings.UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect

    def weapon_overlay(self, weapon, has_switched):
        if not weapon:
            return
        weapon_name = list(weapon.keys())[0]
        bg_rect = self.selection_box(10, 630, has_switched)
        weapon_surf = next(
            (weapon[weapon_name] for weapon in self.weapon_graphics if weapon_name in weapon), None
        )
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic, has_switched):
        if not magic:
            return
        magic_name = list(magic.keys())[0]
        bg_rect = self.selection_box(80, 635, has_switched)
        magic_surf = next(
            (magic[magic_name] for magic in self.magic_graphics if magic_name in magic), None
        )
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(
            player.health, player.stats["health"], self.health_bar_rect, game_settings.HEALTH_COLOR
        )
        self.show_bar(
            player.energy, player.stats["energy"], self.energy_bar_rect, game_settings.ENERGY_COLOR
        )

        self.show_exp(player.exp)

        self.weapon_overlay(player.current_weapon, not player.can_switch_weapon)
        self.magic_overlay(player.current_magic, not player.can_switch_magic)
