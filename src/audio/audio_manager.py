import pygame

from settings import DEFAULT_VOLUME, WORLD_AUDIO_PATH


class AudioManager:
    def __init__(self):
        self.current_level_music = None
        self.main_sound = pygame.mixer.Sound(WORLD_AUDIO_PATH / "0.ogg")
        self.overworld_sound = pygame.mixer.Sound(WORLD_AUDIO_PATH / "overworld.ogg")
        self.main_sound.set_volume(DEFAULT_VOLUME)
        self.overworld_sound.set_volume(DEFAULT_VOLUME)

    def play_overworld_music(self):
        if self.current_level_music:
            self.current_level_music.stop()
        self.overworld_sound.play(loops=-1)

    def play_level_music(self, level_music_path):
        self.overworld_sound.stop()
        self.current_level_music = pygame.mixer.Sound(level_music_path)
        self.current_level_music.set_volume(DEFAULT_VOLUME)
        self.current_level_music.play(loops=-1)
