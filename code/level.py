from random import choice, randint

import pygame

from enemy import Enemy
from input_handler import InputHandler
from level_data import levels
from magic import MagicPlayer
from npc import NPC
from npc_data import npcs
from particles import AnimationPlayer
from player import Player
from settings import GRAPHICS_PATH, TILESIZE
from support import import_csv_layout, import_folder
from tile import Tile
from ui import UI
from weapon import Weapon


class Level:
    def __init__(self, stage):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False

        # get the stage
        self.stage = stage

        # get the level data for the current stage
        self.level_data = levels[stage]

        # controller setup
        self.input_handler = InputHandler()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(self.stage)
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        # use the level data
        layouts = {
            "boundary": import_csv_layout(self.level_data["constraints"]),
            "grass": import_csv_layout(self.level_data["grass"]),
            "object": import_csv_layout(self.level_data["objects"]),
            "entities": import_csv_layout(self.level_data["entities"]),
        }
        graphics = {
            "grass": import_folder(GRAPHICS_PATH / "grass"),
            "objects": import_folder(GRAPHICS_PATH / "objects"),
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

                        if style == "entities":
                            if col == "394":
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic,
                                    self.input_handler,
                                )
                            elif col in ["400", "401"]:
                                npc_data = npcs[int(col)]
                                NPC(
                                    npc_data["name"],
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites],
                                    self.obstacle_sprites,
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
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp,
                                )

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        if style == "heal":
            self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

        if style == "flame":
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.attackable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "grass":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(
                                    pos - offset, [self.visible_sprites]
                                )
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animation_player.create_particles(
                attack_type, self.player.rect.center, [self.visible_sprites]
            )

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.update_enemy(self.player)
            self.visible_sprites.update_npc(self.player)
            self.player_attack_logic()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, stage):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Set stage
        self.stage = stage

        # use the ground image from level data
        self.floor_surf = pygame.image.load(levels[stage]["ground"]).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def update_enemy(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.update_enemy(player)

    def update_npc(self, player):
        npc_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "npc"
        ]
        for npc in npc_sprites:
            npc.update_npc(player)
