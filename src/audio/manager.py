import pygame

from settings import DEFAULT_VOLUME, WORLD_AUDIO_PATH


class AudioManager:
    def __init__(self):
        self.current_music = None
        self.music_paths = {
            "overworld": WORLD_AUDIO_PATH / "overworld.ogg",
            "0": WORLD_AUDIO_PATH / "0.ogg",
            "1": WORLD_AUDIO_PATH / "1.ogg",
        }
        self.music_objects = {
            key: pygame.mixer.Sound(path) for key, path in self.music_paths.items()
        }
        for sound in self.music_objects.values():
            sound.set_volume(DEFAULT_VOLUME)

    def _stop_current_music(self):
        if self.current_music:
            self.current_music.stop()

    def play_music(self, music_key):
        """Play a specific music based on the given key."""
        self._stop_current_music()
        self.current_music = self.music_objects.get(music_key)
        if not self.current_music:
            raise ValueError(f"No music found for the key: {music_key}")
        self.current_music.play(loops=-1)
