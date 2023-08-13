from entity import Entity
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

    def import_graphics(self, name):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
        }
        npc_path = NPC_PATH / f"{name}"
        for animation in self.animations.keys():
            full_path = npc_path / animation
            self.animations[animation] = import_folder(full_path)

    def update(self):
        pass  # No update logic needed for a static NPC
