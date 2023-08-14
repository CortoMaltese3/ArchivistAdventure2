import pygame

from companion_data import companions, COMPANION_NAMES
from entity import Entity
from settings import COMPANION_PATH, FPS, HITBOX_OFFSET
from speech_bubble import SpeechBubble
from support import import_folder


class Companion(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites):
        # General setup
        super().__init__(groups)
        self.sprite_type = "companion"
        # graphics setup
        self.import_graphics(name)
        self.status = "down"
        self.image = self.animations[self.status][self.frame_index]

        self.follow_distance = 50  # distance at which the companion will follow the player
        self.close_distance = 20

        # movement
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["companion"])
        self.obstacle_sprites = obstacle_sprites
        self.animation_speed = 250
        self.animation_timer = 0

        # info
        companion_id = [
            id for id, companion_name in COMPANION_NAMES.items() if companion_name == name
        ][0]
        companion_info = companions[companion_id]
        self.name = name

        # speech
        self.speech = companion_info["speech"]
        self.clock = pygame.time.Clock()

    def import_graphics(self, name):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
        }
        for animation in self.animations.keys():
            full_path = COMPANION_PATH / name / animation
            self.animations[animation] = import_folder(full_path)

    def handle_speech(self, player):
        distance, _ = self.get_player_distance_direction(player)
        if distance <= self.notice_radius:
            if not hasattr(self, "speech_bubble"):
                self.speech_bubble = SpeechBubble(self.speech[0], (self.rect.x, self.rect.y - 30))
            self.speech_bubble.update(self.clock.tick(FPS))  # Update the speech bubble
        elif hasattr(self, "speech_bubble"):
            delattr(self, "speech_bubble")  # Remove the speech bubble if player is out of range

    def get_player_distance_direction(self, player):
        companion_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - companion_vec).magnitude()

        if distance > 0:
            direction = (player_vec - companion_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance, direction = self.get_player_distance_direction(player)

        # If the companion is far from the player, make it follow
        if distance <= self.follow_distance:
            if not "idle" in self.status:
                self.status = self.status + "_idle"
        else:
            move_speed = 3  # adjust the speed as needed
            move = direction * move_speed

            # Check if the next position will collide with obstacles or get too close to the player
            new_rect = self.rect.move(move.x, move.y)
            if (
                not any(new_rect.colliderect(obstacle) for obstacle in self.obstacle_sprites)
                and distance > self.close_distance
            ):
                self.rect = new_rect

            # Determine the facing direction
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

        # Handle the animation frames using animation_speed
        elapsed_time = self.clock.tick(FPS)
        self.animation_timer += elapsed_time
        if self.animation_timer > self.animation_speed:
            self.frame_index += 1
            self.animation_timer = 0

        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]

    def update_companion(self, player):
        self.get_status(player)

    def update(self):
        pass
