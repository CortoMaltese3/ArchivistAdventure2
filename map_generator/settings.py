from pathlib import Path

# Grid settings
ROWS = 50
COLS = 50
CELL_SIZE = 15

COLOR_MAP = {
    "air": ("white", -1),
    "wall": ("black", 395),
    "player": ("gold", 394),
    "grass": ("green", 8),
    "water": ("blue", 4),
    "enemy": ("red", 390),
    "object": ("brown", 3),
}

# Get the base path of the application
BASE_PATH = Path(__file__).parent.parent

# Maps
MAP_PATH = BASE_PATH / "map"
MAP_FLOOR_BLOCKS = MAP_PATH / "map_FloorBlocks.csv"
MAP_ENTITIES = MAP_PATH / "map_Entities.csv"
MAP_GRASS = MAP_PATH / "map_Grass.csv"
MAP_OBJECTS = MAP_PATH / "map_Objects.csv"
