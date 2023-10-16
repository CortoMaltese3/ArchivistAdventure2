import pygame


class InputHandler:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
        # menu options
        self.menu_option = 0
        self.menu_timer = 0
        self.pause_timer = 0

        if self.joystick:
            self.joystick.init()

    def get_input(self):
        actions = {
            "move_up": False,
            "move_down": False,
            "move_left": False,
            "move_right": False,
            "attack": False,
            "magic": False,
            "switch_weapon": False,
            "switch_magic": False,
            "select": False,
        }

        keys = pygame.key.get_pressed()
        actions["move_up"] = keys[pygame.K_UP]
        actions["move_down"] = keys[pygame.K_DOWN]
        actions["move_left"] = keys[pygame.K_LEFT]
        actions["move_right"] = keys[pygame.K_RIGHT]
        actions["attack"] = keys[pygame.K_z]
        actions["select"] = keys[pygame.K_z]
        actions["magic"] = keys[pygame.K_x]
        actions["switch_weapon"] = keys[pygame.K_a]
        actions["switch_magic"] = keys[pygame.K_s]

        if self.joystick:
            actions["move_up"] = actions["move_up"] or self.joystick.get_axis(1) < 0
            actions["move_down"] = actions["move_down"] or self.joystick.get_axis(1) > 0
            actions["move_left"] = actions["move_left"] or self.joystick.get_axis(0) < 0
            actions["move_right"] = actions["move_right"] or self.joystick.get_axis(0) > 0
            actions["attack"] = actions["attack"] or self.joystick.get_button(0)
            actions["select"] = actions["select"] or self.joystick.get_button(0)
            actions["magic"] = actions["magic"] or self.joystick.get_button(1)
            actions["switch_weapon"] = actions["switch_weapon"] or self.joystick.get_button(2)
            actions["switch_magic"] = actions["switch_magic"] or self.joystick.get_button(3)
        return actions

    def check_pause(self):
        is_paused = False
        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        joystick_pause = self.joystick.get_button(4) if self.joystick else False  # TODO: Test it

        if (keys[pygame.K_ESCAPE] or joystick_pause) and current_time - self.pause_timer > 200:
            is_paused = True
            self.pause_timer = current_time

        return is_paused

    def handle_pause_input(self):
        actions = {
            "select_option": False,
            "next_option": False,
            "previous_option": False,
        }

        keys = pygame.key.get_pressed()
        actions["select_option"] = keys[pygame.K_RETURN]

        # Adding delay for up and down keys
        current_time = pygame.time.get_ticks()
        if current_time - self.menu_timer > 200:  # 200ms delay
            if keys[pygame.K_DOWN] or (self.joystick and self.joystick.get_axis(1) > 0):
                actions["next_option"] = True
                self.menu_timer = current_time
            if keys[pygame.K_UP] or (self.joystick and self.joystick.get_axis(1) < 0):
                actions["previous_option"] = True
                self.menu_timer = current_time

        return actions
