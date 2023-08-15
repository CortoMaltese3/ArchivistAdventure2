from random import randint
import sys

import pygame

from .builder import LevelBuilder, EntityBuilder
from data.level_data import levels
from elements.magic import MagicPlayer
from elements.particles import AnimationPlayer
from elements.weapon import Weapon
from settings import HEIGHT, WIDTH
from ui.base import UI
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

    def draw_pause_menu(self):
        font = pygame.font.Font(None, 36)
        options = ["Continue", "Main Menu", "Quit"]
        for index, option in enumerate(options):
            color = (255, 255, 255) if index != self.input_handler.menu_option else (255, 0, 0)
            text = font.render(option, True, color)
            self.display_surface.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2 + index * 40,
                ),
            )

    def handle_pause_menu(self):
        actions = self.input_handler.handle_pause_input()
        if actions["next_option"]:
            self.input_handler.menu_option = (self.input_handler.menu_option + 1) % 3
        elif actions["previous_option"]:
            self.input_handler.menu_option = (self.input_handler.menu_option - 1) % 3
        elif actions["select_option"]:
            # Continue game
            if self.input_handler.menu_option == 0:
                self.toggle_menu()
            # Switch back to overworld view
            elif self.input_handler.menu_option == 1:
                self.game_paused = False
                self.finished = True
            # Quit game
            elif self.input_handler.menu_option == 2:
                pygame.quit()
                sys.exit()

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.input_handler.check_pause():
            self.toggle_menu()

        if self.game_paused:
            self.draw_pause_menu()
            self.handle_pause_menu()
        else:
            self.visible_sprites.update()
            self.visible_sprites.update_enemy(self.player)
            self.visible_sprites.update_npc(self.player)
            self.visible_sprites.update_companion(self.player)
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

        # draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # draw sprites and speech bubbles:
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "npc":
                if hasattr(sprite, "speech_bubble"):  # Check if 'speech_bubble' attribute exists
                    bubble_pos = offset_pos - pygame.Vector2(
                        (sprite.speech_bubble.image.get_width() - sprite.rect.width) / 2,
                        sprite.speech_bubble.image.get_height(),
                    )
                    sprite.speech_bubble.draw(self.display_surface, bubble_pos)

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

    def update_companion(self, player):
        companion_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "companion"
        ]
        for companion in companion_sprites:
            companion.update_companion(player)
