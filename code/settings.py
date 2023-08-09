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
CODE_PATH = BASE_PATH / "code"
GRAPHICS_PATH = BASE_PATH / "graphics"
LEVEL_PATH = BASE_PATH / "levels"

# Get secondary directories of the application
ICONS_PATH = GRAPHICS_PATH / "icons"
MONSTERS_PATH = GRAPHICS_PATH / "monsters"
PARTICLES_PATH = GRAPHICS_PATH / "particles"
PLAYER_PATH = GRAPHICS_PATH / "player"
WEAPONS_PATH = GRAPHICS_PATH / "weapons"

# game setup
WIDTH = 1280
HEIGTH = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {"player": -26, "object": -40, "grass": -10, "invisible": 0}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = GRAPHICS_PATH / "font" / "joystix.ttf"
UI_FONT_SIZE = 18

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

# upgrade menu
TEXT_COLOR_SELECTED = "#111111"
BAR_COLOR = "#EEEEEE"
BAR_COLOR_SELECTED = "#111111"
UPGRADE_BG_COLOR_SELECTED = "#EEEEEE"

# weapons
weapon_data = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "graphic": WEAPONS_PATH / "sword" / "full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "graphic": WEAPONS_PATH / "lance" / "full.png",
    },
}

# magic
magic_data = {
    "flame": {
        "strength": 5,
        "cost": 20,
        "graphic": PARTICLES_PATH / "flame" / "fire.png",
    },
    "heal": {
        "strength": 20,
        "cost": 10,
        "graphic": PARTICLES_PATH / "heal" / "heal.png",
    },
}

# enemy
monster_data = {
    "scarab": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "slash",
        "attack_sound": AUDIO_PATH / "attack" / "slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
    "book": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "thunder",
        "attack_sound": AUDIO_PATH / "attack" / "fireball.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
