from pathlib import Path

# Grid settings
ROWS = 50
COLS = 50
CELL_SIZE = 15

# Default color map (Color name: numerical value)
COLOR_MAP = {"white": -1, "black": 395, "red": 2, "green": 3, "blue": 4}

# Get the base path of the application
BASE_PATH = Path(__file__).parent.parent

MAP_PATH = BASE_PATH / "map"
MAP_FLOOR_BLOCKS = MAP_PATH / "map_FloorBlocks.csv"
