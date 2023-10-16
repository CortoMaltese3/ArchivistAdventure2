import pygame

# from src.data.magic_data import magic_data
# from src.data.weapon_data import weapon_data
from .entity import Entity
from src.settings import game_settings, paths
from src.utils.support import import_folder


class Player(Entity):
    def __init__(
        self,
        pos,
        groups,
        obstacle_sprites,
        create_attack,
        destroy_attack,
        create_magic,
        input_handler,
    ):
        super().__init__(groups)
        self.image = pygame.image.load(
            paths.PLAYER_DIR / "down_idle" / "idle_down.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, game_settings.HITBOX_OFFSET["player"])

        # input setup
        self.input_handler = input_handler

        # graphics setup
        self.import_player_assets()
        self.status = "down"

        # movement
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.current_weapon = None
        self.current_weapon_name = None
        self.weapons = []
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # magic
        self.create_magic = create_magic
        self.current_magic = None
        self.current_magic_name = None
        self.magics = []
        self.can_switch_magic = True
        self.magic_switch_time = None

        # stats
        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 5}
        self.max_stats = {
            "health": 300,
            "energy": 140,
            "attack": 20,
            "magic": 10,
            "speed": 10,
        }
        self.health = self.stats["health"] * 0.5
        self.energy = self.stats["energy"] * 0.8
        self.exp = 0
        self.speed = self.stats["speed"]

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        # import a sound
        self.weapon_attack_sound = pygame.mixer.Sound(paths.WEAPONS_AUDIO_DIR / "sword.wav")
        self.weapon_attack_sound.set_volume(game_settings.SFX_VOLUME)

    def import_player_assets(self):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_attack": [],
            "left_attack": [],
            "up_attack": [],
            "down_attack": [],
        }

        for animation in self.animations.keys():
            full_path = paths.PLAYER_DIR / animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        actions = self.input_handler.get_input()

        if not self.attacking:
            # movement input
            if actions["move_up"]:
                self.direction.y = -1
                self.status = "up"
            elif actions["move_down"]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0
            if actions["move_right"]:
                self.direction.x = 1
                self.status = "right"
            elif actions["move_left"]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            # attack input
            if actions["attack"] and self.current_weapon:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.set_volume(game_settings.SFX_VOLUME)
                self.weapon_attack_sound.play()

            # magic input
            if actions["magic"] and self.current_magic:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                strength = (
                    self.current_magic.get(self.current_magic_name).get("strength")
                    + self.stats["magic"]
                )
                cost = self.current_magic.get(self.current_magic_name).get("cost")
                self.create_magic(self.current_magic_name, strength, cost)

            # weapon switching
            if actions["switch_weapon"] and self.can_switch_weapon and self.current_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                # Find the current weapon's position in the list
                current_position = self.weapons.index(self.current_weapon)

                # Switch to the next weapon
                next_position = (current_position + 1) % len(self.weapons)
                self.current_weapon = self.weapons[next_position]
                self.current_weapon_name = list(self.current_weapon.keys())[0]

            # magic switching
            if actions["switch_magic"] and self.can_switch_magic and self.current_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                # Find the current weapon's position in the list
                current_position = self.magics.index(self.current_magic)

                # Switch to the next weapon
                next_position = (current_position + 1) % len(self.magics)
                self.current_magic = self.magics[next_position]
                self.current_magic_name = list(self.current_magic.keys())[0]

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if self.current_weapon:
                if (
                    current_time - self.attack_time
                    >= self.attack_cooldown
                    + self.current_weapon.get(self.current_weapon_name).get("cooldown")
                ):
                    self.attacking = False
                    self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats["attack"]
        weapon_damage = self.current_weapon.get(self.current_weapon_name).get("damage")
        return base_damage + weapon_damage

    def get_full_magic_damage(self):
        base_damage = self.stats["magic"]
        spell_damage = self.current_magic.get(self.current_magic_name).get("strength")
        return base_damage + spell_damage

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def add_weapon(self, weapon):
        if weapon not in self.weapons:
            self.weapons.append(weapon)
            if self.current_weapon is None:
                self.current_weapon = weapon
                weapon_name = list(weapon.keys())[0]
                self.current_weapon_name = weapon_name

    def add_magic(self, magic):
        if magic not in self.magics:
            self.magics.append(magic)
            if self.current_magic is None:
                self.current_magic = magic
                magic_name = list(magic.keys())[0]
                self.current_magic_name = magic_name

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recovery()
