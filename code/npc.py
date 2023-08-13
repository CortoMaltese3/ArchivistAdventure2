import pygame

from entity import Entity
from npc_data import npcs
from settings import HITBOX_OFFSET, NPC_PATH
from support import import_folder


class NPC(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites):
        # General setup
        super().__init__(groups)
        self.sprite_type = "npc"

        # graphics setup
        self.import_graphics(name)
        self.status = "down"
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["npc"])
        self.obstacle_sprites = obstacle_sprites

        # info
        self.name = name
        npc_info = npcs[self.name]
        self.notice_radius = npcs["notice_radius"]

    def import_graphics(self, name):
        self.animations = {
            "idle": [],
            "move": [],
        }
        main_path = NPC_PATH / f"{name}"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path / animation)

    def update(self):
        pass  # No update logic needed for a static NPC
