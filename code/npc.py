import pygame

from settings import NPC_PATH
from support import import_folder
from entity import Entity
from npc_data import npcs


class NPC(Entity):
    def __init__(self, pos, groups, num):
        super().__init__(groups)

        # Load NPC data from npc_data.py
        self.npc_info = npcs[num]

        # Graphics setup
        self.image = self.npc_info["sprite"].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.import_npc_assets()
        self.status = "down"

        # Other properties
        self.speech = self.npc_info["speech"]

    def import_npc_assets(self):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
        }

        for animation in self.animations.keys():
            full_path = NPC_PATH / self.npc_type / animation
            self.animations[animation] = import_folder(full_path)

    def get_status(self):
        # Implement logic to determine the current status of the NPC
        # This can be based on AI behavior, movement patterns, etc.
        pass

    def animate(self):
        animation = self.animations[self.status]

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_player_distance_direction(self, player):
        npc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - npc_vec).magnitude()

        if distance > 0:
            direction = (player_vec - npc_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def turn_towards_player(self):
        for player in self.player_sprites:
            distance, _ = self.get_player_distance_direction(player)
            if distance <= self.interaction_radius:
                # Code to change the image or orientation of the NPC
                # based on the direction to the player.
                pass

    def update(self):
        self.get_status()
        self.animate()
        self.turn_towards_player()
