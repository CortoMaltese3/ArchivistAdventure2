import pygame

from src.data.magic_data import magic_data
from src.data.npc_data import npcs, NPC_NAMES
from src.data.weapon_data import weapon_data
from .entity import Entity
from src.settings import game_settings, paths
from src.ui.speech_bubble import SpeechBubble
from src.user.input_handler import InputHandler
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

        # input setup
        self.input_handler = InputHandler()

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
        self.speaking = False
        self.speech = npc_info["speech"]
        self.current_speech_index = 0
        self.speech_cooldown_timer = 0
        self.speech_cooldown_duration = 500

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
                weapon_info = {weapon: weapon_data.get(weapon)}
                player.add_weapon(weapon_info)
            # Checks if the NPC has a magic available for the player
            if magic:
                magic_info = {magic: magic_data.get(magic)}
                player.add_magic(magic_info)

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
        actions = self.input_handler.get_input()
        distance, _ = self.get_player_distance_direction(player)

        if distance <= self.notice_radius:
            # If the player presses the "attack" action
            if actions["attack"] and self.speech_cooldown_timer <= 0:
                # If NPC is not currently speaking, start the speech
                if not self.speaking:
                    self.start_speech()
                # If NPC is speaking and has an active speech bubble
                elif hasattr(self, "speech_bubble"):
                    # If the current message is still typing, reset the typing
                    if not self.speech_bubble.is_finished_typing():
                        self.speech_bubble.reset_typing()
                    # If the current message has finished typing, move to the next one
                    elif self.speech_bubble.is_finished():
                        self.current_speech_index = (self.current_speech_index + 1) % len(
                            self.speech
                        )
                        self.start_speech()

                # Reset the cooldown timer
                self.speech_cooldown_timer = self.speech_cooldown_duration
            # If player uses the "magic" action, stop the speech and remove the speech bubble
            elif actions["magic"] and hasattr(self, "speech_bubble"):
                self.speaking = False
                delattr(self, "speech_bubble")
            # If NPC is speaking and has an active speech bubble, update the speech bubble
            elif self.speaking and hasattr(self, "speech_bubble"):
                self.speech_bubble.update(self.clock.tick(game_settings.FPS))
        # If player is out of the notice radius, stop the speech and remove the speech bubble
        else:
            self.speaking = False
            if hasattr(self, "speech_bubble"):
                delattr(self, "speech_bubble")

    def start_speech(self):
        self.speaking = True

        # Check if there's more text in the list after the current one
        indicator = None
        if (self.current_speech_index + 1) < len(self.speech):
            indicator = "triangle"
        else:
            indicator = "exit"

        self.speech_bubble = SpeechBubble(
            self.speech[self.current_speech_index],
            (self.rect.x, self.rect.y - 30),
            show_indicator=indicator,  # Pass the indicator type here
        )
        self.speech_cooldown_timer = self.speech_cooldown_duration

    def update_npc(self, player):
        self.get_status(player)
        self.handle_speech(player)
        self.grant_to_player(player)

        # Reduce the cooldown timer
        if self.speech_cooldown_timer > 0:
            self.speech_cooldown_timer -= self.clock.tick(game_settings.FPS)

    def update(self):
        pass
