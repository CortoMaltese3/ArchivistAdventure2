from enum import Enum, auto

from src.audio.manager import AudioManager
from .base import Level
from .overworld import Overworld


class GameState(Enum):
    OVERWORLD = auto()
    LEVEL = auto()


class LevelManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameState.OVERWORLD
        self.audio_manager = AudioManager()

        self.current_level = None
        self.overworld = Overworld(0, 1, self.screen, self.load_level)

    def load_overworld(self):
        self.audio_manager.play_music("overworld")
        self.current_level = self.overworld
        self.state = GameState.OVERWORLD

    def load_level(self, level_number):
        self.current_level = Level(stage=level_number)
        self.audio_manager.play_music(str(level_number))
        self.state = GameState.LEVEL

    def run_current_level(self):
        self.current_level.run()
        if self.state == GameState.LEVEL and self.current_level.finished:
            self.load_overworld()
