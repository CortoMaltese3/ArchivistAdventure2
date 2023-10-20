from dataclasses import dataclass
from pathlib import Path
import sys

# Get the base path of the application
if getattr(sys, "frozen", False):
    # If the application is run as a bundle/exe with PyInstaller,
    # use the right path
    BASE_PATH = Path(sys._MEIPASS)
else:
    # Else use the path of the script being run
    BASE_PATH = Path(__file__).parent.parent


@dataclass(frozen=True)
class Paths:
    # Get the main directories of the application
    AUDIO_DIR: Path = BASE_PATH / "audio"
    BASE_PATH: Path = BASE_PATH
    CODE_DIR: Path = BASE_PATH / "src"
    GRAPHICS_DIR: Path = BASE_PATH / "graphics"
    LEVEL_DIR: Path = BASE_PATH / "maps"

    # Get secondary graphics directories of the application
    ENTITIES_GRAPH_DIR: Path = GRAPHICS_DIR / "entities"
    UI_GRAPH_DIR: Path = GRAPHICS_DIR / "ui"
    WORLD_GRAPH_DIR: Path = GRAPHICS_DIR / "world"

    COMPANION_DIR: Path = ENTITIES_GRAPH_DIR / "companions"
    ICONS_DIR: Path = UI_GRAPH_DIR / "icons"
    MONSTERS_DIR: Path = ENTITIES_GRAPH_DIR / "monsters"
    NPC_DIR: Path = ENTITIES_GRAPH_DIR / "npc"
    OVERWORLD_DIR: Path = WORLD_GRAPH_DIR / "overworld"
    PARTICLES_DIR: Path = GRAPHICS_DIR / "particles"
    PLAYER_DIR: Path = ENTITIES_GRAPH_DIR / "player"
    WEAPONS_DIR: Path = GRAPHICS_DIR / "weapons"

    # Get secondary audio directories of the application
    ENTITIES_AUDIO_DIR: Path = AUDIO_DIR / "entities"
    ENEMY_AUDIO_DIR: Path = ENTITIES_AUDIO_DIR / "enemy"

    MAGIC_AUDIO_DIR: Path = AUDIO_DIR / "magic"
    WEAPONS_AUDIO_DIR: Path = AUDIO_DIR / "weapons"
    WORLD_AUDIO_DIR: Path = AUDIO_DIR / "world"

    FAVICON_PATH = ICONS_DIR / "icon.ico"
    UI_FONT_PATH = UI_GRAPH_DIR / "font" / "joystix.ttf"

    OVERWORLD_BG_PATH: Path = OVERWORLD_DIR / "background.png"


# game setup
@dataclass(frozen=True)
class GameSettings:
    WIDTH: int = 1280
    HEIGHT: int = 720
    FPS: int = 60
    TILESIZE: int = 64
    HITBOX_OFFSET = {
        "player": -26,
        "object": -40,
        "grass": -10,
        "invisible": 0,
        "npc": -26,
        "companion": -26,
    }

    # ui
    BAR_HEIGHT: int = 20
    HEALTH_BAR_WIDTH: int = 200
    ENERGY_BAR_WIDTH: int = 140
    ITEM_BOX_SIZE: int = 80

    # general colors
    WATER_COLOR: str = "#71ddee"
    UI_BG_COLOR: str = "#222222"
    UI_BORDER_COLOR: str = "#111111"
    TEXT_COLOR: str = "#EEEEEE"

    # ui colors
    HEALTH_COLOR: str = "red"
    ENERGY_COLOR: str = "blue"
    UI_BORDER_COLOR_ACTIVE: str = "gold"
    BLACK_COLOR: str = "black"

    # text
    CAPTION: str = "Archivist Adventure 2"
    LINE_SPACING: int = 5

    UI_FONT_SIZE: int = 18
    UI_FONT_WIDTH: int = 15

    # sound
    MAIN_VOLUME: float = 0.2
    SFX_VOLUME: float = 0.2


# Create module-level instances
game_settings = GameSettings()
paths = Paths()
