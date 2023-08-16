from random import randint
import sys

import pygame

from .builder import LevelBuilder, EntityBuilder
from .camera import YSortCameraGroup
from data.level_data import levels
from elements.magic import MagicPlayer
from elements.particles import AnimationPlayer
from elements.weapon import Weapon
from ui.base import UI
from ui.pause_menu import MenuOption, PauseMenu
from user.input_handler import InputHandler
from utils.support import import_csv_layout


class Level:
    def __init__(self, stage):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.finished = False

        # get the stage
        self.stage = stage

        # get the level data for the current stage
        self.level_data = levels[stage]

        # controller setup
        self.input_handler = InputHandler()

        # pause menu setup
        self.pause_menu = PauseMenu(self.toggle_menu, self.input_handler)

        # sprite group setup
        self.visible_sprites = YSortCameraGroup(self.stage)
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # user interface
        self.ui = UI()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

        self.level_builder = LevelBuilder(self.level_data)
        self.level_builder.set_sprite_groups(
            self.visible_sprites, self.obstacle_sprites, self.attackable_sprites
        )
        self.level_builder.build_map()

        self.entity_builder = EntityBuilder(
            self.level_data, self.damage_player, self.trigger_death_particles, self.add_exp
        )

        self.entity_builder.set_layout(import_csv_layout(self.level_data["entities"]))
        self.entity_builder.create_entities(
            self.visible_sprites,
            self.obstacle_sprites,
            self.attackable_sprites,
            self.input_handler,
            create_attack=self.create_attack,
            destroy_attack=self.destroy_attack,
            create_magic=self.create_magic,
        )
        self.player = self.entity_builder.get_player()

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

        if self.input_handler.check_pause():
            self.toggle_menu()

        if self.game_paused:
            result = self.pause_menu.run()
            if result == MenuOption.FINISHED:
                self.game_paused = False
                self.finished = True
        else:
            self.visible_sprites.update()
            self.visible_sprites.update_enemy(self.player)
            self.visible_sprites.update_npc(self.player)
            self.visible_sprites.update_companion(self.player)
            self.player_attack_logic()
