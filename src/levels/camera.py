import pygame

from data.level_data import levels

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, stage):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Set stage
        self.stage = stage

        # use the ground image from level data
        self.floor_surf = pygame.image.load(levels[stage]["ground"]).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # draw sprites and speech bubbles:
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "npc":
                if hasattr(sprite, "speech_bubble"):  # Check if 'speech_bubble' attribute exists
                    bubble_pos = offset_pos - pygame.Vector2(
                        (sprite.speech_bubble.image.get_width() - sprite.rect.width) / 2,
                        sprite.speech_bubble.image.get_height(),
                    )
                    sprite.speech_bubble.draw(self.display_surface, bubble_pos)

    def update_enemy(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.update_enemy(player)

    def update_npc(self, player):
        npc_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "npc"
        ]
        for npc in npc_sprites:
            npc.update_npc(player)

    def update_companion(self, player):
        companion_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "companion"
        ]
        for companion in companion_sprites:
            companion.update_companion(player)
