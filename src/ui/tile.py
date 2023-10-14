import pygame

from settings import game_settings


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        groups,
        sprite_type,
        surface=pygame.Surface((game_settings.TILESIZE, game_settings.TILESIZE)),
    ):
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = game_settings.HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - game_settings.TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)
