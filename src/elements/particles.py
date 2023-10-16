from random import choice

import pygame

from src.settings import paths
from src.utils.support import import_folder


class Animation:
    def __init__(self):
        self.frames = {
            # magic
            "flame": import_folder(paths.PARTICLES_DIR / "flame" / "frames"),
            "aura": import_folder(paths.PARTICLES_DIR / "aura"),
            "heal": import_folder(paths.PARTICLES_DIR / "heal" / "frames"),
            # attacks
            "claw": import_folder(paths.PARTICLES_DIR / "claw"),
            "slash": import_folder(paths.PARTICLES_DIR / "slash"),
            "sparkle": import_folder(paths.PARTICLES_DIR / "sparkle"),
            "leaf_attack": import_folder(paths.PARTICLES_DIR / "leaf_attack"),
            "thunder": import_folder(paths.PARTICLES_DIR / "thunder"),
            # monster deaths
            "squid": import_folder(paths.PARTICLES_DIR / "smoke_orange"),
            "spirit": import_folder(paths.PARTICLES_DIR / "nova"),
            "scarab": import_folder(paths.PARTICLES_DIR / "scarab"),
            "book": import_folder(paths.PARTICLES_DIR / "book"),
            # leafs
            "leaf": (
                import_folder(paths.PARTICLES_DIR / "leaf1"),
                import_folder(paths.PARTICLES_DIR / "leaf2"),
                import_folder(paths.PARTICLES_DIR / "leaf3"),
                import_folder(paths.PARTICLES_DIR / "leaf4"),
                import_folder(paths.PARTICLES_DIR / "leaf5"),
                import_folder(paths.PARTICLES_DIR / "leaf6"),
                self.reflect_images(import_folder(paths.PARTICLES_DIR / "leaf1")),
                self.reflect_images(import_folder(paths.PARTICLES_DIR / "leaf2")),
                self.reflect_images(import_folder(paths.PARTICLES_DIR / "leaf3")),
                self.reflect_images(import_folder(paths.PARTICLES_DIR / "leaf4")),
                self.reflect_images(import_folder(paths.PARTICLES_DIR / "leaf5")),
                self.reflect_images(import_folder(paths.PARTICLES_DIR / "leaf6")),
            ),
        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        animation_frames = choice(self.frames["leaf"])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
