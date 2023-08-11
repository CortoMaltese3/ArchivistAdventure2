import pygame
from entity import Entity
from settings import HITBOX_OFFSET, NPC_PATH


class NPC(Entity):
    def __init__(self, pos, groups, sprite_path):
        super().__init__(groups)
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["npc"])

    def update(self):
        pass  # No update logic needed for a static NPC
