import pygame

from settings import WEAPONS_PATH


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = "weapon"
        direction = player.status.split("_")[0]

        # graphic
        full_path = WEAPONS_PATH / f"{player.weapon}" / f"{direction}.png"
        self.image = pygame.image.load(full_path).convert_alpha()

        # placement
        if direction == "right":
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + pygame.math.Vector2(-20, 16)
            )
        elif direction == "left":
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + pygame.math.Vector2(20, 16)
            )
        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + pygame.math.Vector2(-10, -10)
            )
        else:
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + pygame.math.Vector2(-10, 10)
            )
