from random import randint

import pygame

from src.settings import game_settings, paths


class Magic:
    def __init__(self, animation):
        self.animation = animation
        self.sounds = {
            "heal": pygame.mixer.Sound(paths.MAGIC_AUDIO_DIR / "heal.wav"),
            "flame": pygame.mixer.Sound(paths.MAGIC_AUDIO_DIR / "fire.wav"),
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds["heal"].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            self.animation.create_particles("aura", player.rect.center, groups)
            self.animation.create_particles("heal", player.rect.center, groups)

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost
            self.sounds["flame"].play()

            if player.status.split("_")[0] == "right":
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split("_")[0] == "left":
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split("_")[0] == "up":
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * game_settings.TILESIZE
                    x = (
                        player.rect.centerx
                        + offset_x
                        + randint(-game_settings.TILESIZE // 3, game_settings.TILESIZE // 3)
                    )
                    y = player.rect.centery + randint(
                        -game_settings.TILESIZE // 3, game_settings.TILESIZE // 3
                    )
                    self.animation.create_particles("flame", (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * game_settings.TILESIZE
                    x = player.rect.centerx + randint(
                        -game_settings.TILESIZE // 3, game_settings.TILESIZE // 3
                    )
                    y = (
                        player.rect.centery
                        + offset_y
                        + randint(-game_settings.TILESIZE // 3, game_settings.TILESIZE // 3)
                    )
                    self.animation.create_particles("flame", (x, y), groups)
