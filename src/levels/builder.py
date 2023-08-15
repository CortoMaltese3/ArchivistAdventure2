from random import choice

from settings import TILESIZE, WORLD_GRAPH_PATH
from ui.tile import Tile
from utils.support import import_csv_layout, import_folder

from entities.player import Player
from entities.npc import NPC
from entities.companion import Companion
from entities.enemy import Enemy

from data.companion_data import companions
from data.npc_data import npcs


class LevelBuilder:
    def __init__(self, level_data):
        self.level_data = level_data

        self.visible_sprites = None
        self.obstacle_sprites = None
        self.attackable_sprites = None

    def set_sprite_groups(self, visible_sprites, obstacle_sprites, attackable_sprites):
        self.visible_sprites = visible_sprites
        self.obstacle_sprites = obstacle_sprites
        self.attackable_sprites = attackable_sprites

    def build_map(self):
        layouts = {
            "boundary": import_csv_layout(self.level_data["constraints"]),
            "grass": import_csv_layout(self.level_data["grass"]),
            "object": import_csv_layout(self.level_data["objects"]),
            "entities": import_csv_layout(self.level_data["entities"]),
        }
        graphics = {
            "grass": import_folder(WORLD_GRAPH_PATH / "grass"),
            "objects": import_folder(WORLD_GRAPH_PATH / "objects"),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")
                        if style == "grass":
                            random_grass_image = choice(graphics["grass"])
                            Tile(
                                (x, y),
                                [
                                    self.visible_sprites,
                                    self.obstacle_sprites,
                                    self.attackable_sprites,
                                ],
                                "grass",
                                random_grass_image,
                            )
                        if style == "object":
                            surf = graphics["objects"][int(col)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                surf,
                            )


class EntityBuilder:
    def __init__(self, level_data, damage_player, trigger_death_particles, add_exp):
        self.level_data = level_data
        self.entities_layout = None
        self.player = None

        # Store the callbacks
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles
        self.add_exp = add_exp

    def set_layout(self, entities_layout):
        self.entities_layout = entities_layout

    def create_entities(
        self, visible_sprites, obstacle_sprites, attackable_sprites, *args, **callbacks
    ):
        for row_index, row in enumerate(self.entities_layout):
            for col_index, col in enumerate(row):
                if col != "-1":
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    if col == "394":
                        self.player = Player(
                            (x, y),
                            [visible_sprites],
                            obstacle_sprites,
                            callbacks["create_attack"],
                            callbacks["destroy_attack"],
                            callbacks["create_magic"],
                            *args,
                        )
                    elif col in ["400", "401"]:
                        npc_data = npcs[int(col)]
                        NPC(
                            name=npc_data["name"],
                            pos=(x, y),
                            groups=[visible_sprites, obstacle_sprites],
                            obstacle_sprites=obstacle_sprites,
                        )
                    elif col in ["500"]:
                        companion_data = companions[int(col)]
                        Companion(
                            name=companion_data["name"],
                            pos=(x, y),
                            groups=[visible_sprites],
                            obstacle_sprites=obstacle_sprites,
                        )
                    else:
                        if col == "397":
                            monster_name = "scarab"
                        elif col == "398":
                            monster_name = "book"
                        else:
                            monster_name = "book"  # TODO: Change it
                        Enemy(
                            monster_name,
                            (x, y),
                            [visible_sprites, attackable_sprites],
                            obstacle_sprites,
                            self.damage_player,
                            self.trigger_death_particles,
                            self.add_exp,
                        )

    def get_player(self):
        return self.player
