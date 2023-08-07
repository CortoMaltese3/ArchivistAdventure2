from pathlib import Path

# Get the base path of the application
BASE_PATH = Path(__file__).parent.parent

# Get the main directories of the application
AUDIO_PATH = BASE_PATH / "audio"
CODE_PATH = BASE_PATH / "code"
GRAPHICS_PATH = BASE_PATH / "graphics"
MAP_PATH = BASE_PATH / "map"
TILEMAP_PATH = GRAPHICS_PATH / "tilemap"

# Get secondary directories of the application
PARTICLES_PATH = GRAPHICS_PATH / "particles"
WEAPONS_PATH = GRAPHICS_PATH / "weapons"
MONSTERS_PATH = GRAPHICS_PATH / "monsters"
ICONS_PATH = GRAPHICS_PATH / "icons"

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
    "bamboo": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "leaf_attack",
        "attack_sound": AUDIO_PATH / "attack" / "slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
    "squid": {
        "health": 100,
        "exp": 100,
        "damage": 20,
        "attack_type": "slash",
        "attack_sound": AUDIO_PATH / "attack" / "slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "spirit": {
        "health": 100,
        "exp": 110,
        "damage": 8,
        "attack_type": "thunder",
        "attack_sound": AUDIO_PATH / "attack/fireball.wav",
        "speed": 4,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 350,
    },
        "scarab": {
        "health": 70,
        "exp": 120,
        "damage": 6,
        "attack_type": "leaf_attack",
        "attack_sound": AUDIO_PATH / "attack" / "slash.wav",
        "speed": 3,
        "resistance": 3,
        "attack_radius": 50,
        "notice_radius": 300,
    },
}
