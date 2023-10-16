import pygame

from src.settings import game_settings, paths


class AudioManager:
    def __init__(self):
        self.current_music = None
        self.music_paths = {
            "overworld": paths.WORLD_AUDIO_DIR / "overworld.ogg",
            "0": paths.WORLD_AUDIO_DIR / "0.ogg",
            "1": paths.WORLD_AUDIO_DIR / "1.ogg",
        }
        self.music_objects = {
            key: pygame.mixer.Sound(path) for key, path in self.music_paths.items()
        }
        for sound in self.music_objects.values():
            sound.set_volume(game_settings.MAIN_VOLUME)

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
