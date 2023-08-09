from settings import GRAPHICS_PATH, LEVEL_PATH

def create_level(level_num, node_pos):
    return {
        'ground': LEVEL_PATH / str(level_num) / "ground.png",
        'constraints': LEVEL_PATH / str(level_num) / "map_FloorBlocks.csv",
        'entities': LEVEL_PATH / str(level_num) / "map_Entities.csv",
        'grass': LEVEL_PATH / str(level_num) / "map_Grass.csv",
        'objects': LEVEL_PATH / str(level_num) / "map_Objects.csv",
        'node_graphics': GRAPHICS_PATH  / "overworld" / str(level_num),
        'node_pos': node_pos,
        'unlock': level_num + 1,
    }

levels = {
    0: create_level(0, (110,400)),
    1: create_level(1, (300,220)),
}
