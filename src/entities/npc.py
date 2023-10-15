import pygame

from src.data.npc_data import npcs, NPC_NAMES
from .entity import Entity
from src.settings import game_settings, paths
from src.ui.speech_bubble import SpeechBubble
from src.utils.support import import_folder


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
        self.hitbox = self.rect.inflate(-6, game_settings.HITBOX_OFFSET["npc"])
        self.obstacle_sprites = obstacle_sprites

        # info
        npc_id = [id for id, npc_name in NPC_NAMES.items() if npc_name == name][0]
        npc_info = npcs[npc_id]
        self.id = npc_id
        self.name = name
        self.notice_radius = npc_info["notice_radius"]

        # speech
        self.speech = npc_info["speech"]
        self.clock = pygame.time.Clock()

    def import_graphics(self, name):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
        }
        npc_path = paths.NPC_DIR / f"{name}"
        for animation in self.animations.keys():
            full_path = npc_path / animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        npc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - npc_vec).magnitude()

        if distance > 0:
            direction = (player_vec - npc_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def grant_to_player(self, player):
        if self.get_player_distance_direction(player)[0] <= self.notice_radius:
            weapon = npcs[self.id].get("weapon")
            magic = npcs[self.id].get("magic")

            # Checks if the NPC has a weapon available for the player
            if weapon:
                player.add_weapon(weapon)
            # Checks if the NPC has a magic available for the player
            if magic:
                player.add_magic(magic)

    def get_status(self, player):
        distance, direction = self.get_player_distance_direction(player)
        if distance <= self.notice_radius:
            # Determine the facing direction based on the direction vector
            # Example: if direction points mostly up, set status to "up"
            if abs(direction.x) > abs(direction.y):
                if direction.x > 0:
                    self.status = "right"
                else:
                    self.status = "left"
            else:
                if direction.y > 0:
                    self.status = "down"
                else:
                    self.status = "up"
        else:
            # Default to facing downwards if the player is outside the notice radius
            self.status = "down"

        self.image = self.animations[self.status][self.frame_index]

    def handle_speech(self, player):
        distance, _ = self.get_player_distance_direction(player)
        if distance <= self.notice_radius:
            if not hasattr(self, "speech_bubble"):
                self.speech_bubble = SpeechBubble(self.speech[0], (self.rect.x, self.rect.y - 30))
            self.speech_bubble.update(
                self.clock.tick(game_settings.FPS)
            )  # Update the speech bubble
        elif hasattr(self, "speech_bubble"):
            delattr(self, "speech_bubble")  # Remove the speech bubble if player is out of range

    def update_npc(self, player):
        self.get_status(player)
        self.handle_speech(player)
        self.grant_to_player(player)

    def update(self):
        pass
