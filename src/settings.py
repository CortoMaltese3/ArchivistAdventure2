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

# Get the main directories of the application
AUDIO_PATH = BASE_PATH / "audio"
CODE_PATH = BASE_PATH / "src"
GRAPHICS_PATH = BASE_PATH / "graphics"
LEVEL_PATH = BASE_PATH / "maps"

# Get secondary graphics directories of the application
ENTITIES_GRAPH_PATH = GRAPHICS_PATH / "entities"
UI_GRAPH_PATH = GRAPHICS_PATH / "ui"
WORLD_GRAPH_PATH = GRAPHICS_PATH / "world"

COMPANION_PATH = ENTITIES_GRAPH_PATH / "companions"
ICONS_PATH = UI_GRAPH_PATH / "icons"
MONSTERS_PATH = ENTITIES_GRAPH_PATH / "monsters"
NPC_PATH = ENTITIES_GRAPH_PATH / "npc"
OVERWORLD_PATH = WORLD_GRAPH_PATH / "overworld"
PARTICLES_PATH = GRAPHICS_PATH / "particles"
PLAYER_PATH = ENTITIES_GRAPH_PATH / "player"
WEAPONS_PATH = GRAPHICS_PATH / "weapons"

# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    "player": -26,
    "object": -40,
    "grass": -10,
    "invisible": 0,
    "npc": -26,
    "companion": -26,
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80

# general colors
WATER_COLOR = "#71ddee"
UI_BG_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"

# ui colors
HEALTH_COLOR = "red"
ENERGY_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"
BLACK_COLOR = "black"

# text
LINE_SPACING = 5
UI_FONT = UI_GRAPH_PATH / "font" / "joystix.ttf"
UI_FONT_SIZE = 18
UI_FONT_WIDTH = 15


