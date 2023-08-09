from settings import GRAPHICS_PATH, LEVEL_PATH

level_0 = {
            'ground': LEVEL_PATH / "0" / "ground.png",
            'constraints': LEVEL_PATH / "0" / "map_FloorBlocks.csv",
            'entities': LEVEL_PATH / "0" / "map_Entities.csv",
            'grass': LEVEL_PATH / "0" / "map_Grass.csv",
            'objects': LEVEL_PATH / "0" / "map_Objects.csv",
            'node_graphics': GRAPHICS_PATH  / "overworld" / "0",
            'unlock': 1,
        }

level_1 = {
            'ground': LEVEL_PATH / "1" / "ground.png",
            'constraints': LEVEL_PATH / "1" / "map_FloorBlocks.csv",
            'entities': LEVEL_PATH / "1" / "map_Entities.csv",
            'grass': LEVEL_PATH / "1" / "map_Grass.csv",
            'objects': LEVEL_PATH / "1" / "map_Objects.csv",
            'node_graphics': GRAPHICS_PATH  / "overworld" / "1",
            'unlock': 2,
        }


levels = {
	0: level_0,
	1: level_1,
}