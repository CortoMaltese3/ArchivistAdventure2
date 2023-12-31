import pygame
import textwrap

from src.settings import game_settings, paths


class SpeechBubble:
    def __init__(self, text, pos, max_width=game_settings.UI_FONT_WIDTH, show_indicator=None):
        self.full_text = text
        self.current_text = ""
        self.pos = pos
        self.max_width = max_width
        self.font = pygame.font.Font(paths.UI_FONT_PATH, game_settings.UI_FONT_SIZE)
        self.image = self.create_bubble_image()
        self.timer = 0
        self.typing_speed = 50  # Time in milliseconds between each letter
        self.show_indicator = show_indicator

    def create_bubble_image(self):
        wrapped_text = textwrap.fill(self.current_text, width=self.max_width)
        lines = wrapped_text.split("\n")
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in lines]
        max_text_width = max(text_surface.get_width() for text_surface in text_surfaces)

        total_height = sum(
            text_surface.get_height() + game_settings.LINE_SPACING for text_surface in text_surfaces
        )
        bubble_surface = pygame.Surface((max_text_width + 20, total_height + 30), pygame.SRCALPHA)
        pygame.draw.rect(bubble_surface, (255, 255, 255, 200), bubble_surface.get_rect(), 0)
        pygame.draw.rect(bubble_surface, (0, 0, 0, 200), bubble_surface.get_rect(), 1)

        y_offset = 5
        for text_surface in text_surfaces:
            bubble_surface.blit(text_surface, (10, y_offset))
            y_offset += text_surface.get_height() + 5

        # Indicator handling
        if self.is_finished() and self.show_indicator:
            if self.show_indicator == "triangle":
                triangle_size = 10
                triangle_center = (
                    bubble_surface.get_width() // 2,
                    bubble_surface.get_height() - triangle_size - 5,
                )
                pygame.draw.polygon(
                    bubble_surface,
                    (0, 0, 0),
                    [
                        (triangle_center[0], triangle_center[1] + triangle_size),
                        (triangle_center[0] - triangle_size // 2, triangle_center[1]),
                        (triangle_center[0] + triangle_size // 2, triangle_center[1]),
                    ],
                )
            elif self.show_indicator == "exit":
                exit_text = self.font.render("[EXIT]", True, (128, 128, 128))
                exit_pos = (
                    (bubble_surface.get_width() - exit_text.get_width()) // 2,
                    bubble_surface.get_height() - exit_text.get_height() - 5,
                )
                bubble_surface.blit(exit_text, exit_pos)

        return bubble_surface

    def is_finished_typing(self):
        return len(self.current_text) == len(self.full_text)

    def reset_typing(self):
        self.current_text = ""
        self.timer = 0
        self.image = self.create_bubble_image()

    def is_finished(self):
        return self.current_text == self.full_text

    def update(self, dt):
        if len(self.current_text) < len(self.full_text):
            self.timer += dt
            if self.timer >= self.typing_speed:
                self.current_text += self.full_text[len(self.current_text)]
                self.timer = 0
                self.image = self.create_bubble_image()

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
