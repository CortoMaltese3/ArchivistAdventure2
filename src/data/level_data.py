from settings import paths


def create_level(level_num, node_pos):
    return {
        "ground": paths.LEVEL_DIR / str(level_num) / "ground.png",
        "constraints": paths.LEVEL_DIR / str(level_num) / "map_FloorBlocks.csv",
        "entities": paths.LEVEL_DIR / str(level_num) / "map_Entities.csv",
        "grass": paths.LEVEL_DIR / str(level_num) / "map_Grass.csv",
        "objects": paths.LEVEL_DIR / str(level_num) / "map_Objects.csv",
        "node_graphics": paths.OVERWORLD_DIR / str(level_num),
        "node_pos": node_pos,
        "unlock": level_num + 1,
        "bg_music": paths.WORLD_AUDIO_DIR / f"{str(level_num)}.ogg",
    }


levels = {
    0: create_level(0, (110, 400)),
    1: create_level(1, (300, 220)),
}
