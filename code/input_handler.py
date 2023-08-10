import pygame


class InputHandler:
    def __init__(self):
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None
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
