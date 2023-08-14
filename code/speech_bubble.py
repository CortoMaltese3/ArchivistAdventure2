import pygame
import textwrap

from settings import LINE_SPACING, UI_FONT, UI_FONT_SIZE

class SpeechBubble:
    def __init__(self, text, pos, max_width=100):  # Set your desired max width
        self.text = text
        self.pos = pos
        self.max_width = max_width
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        self.image = self.create_bubble_image()

    def create_bubble_image(self):
        wrapped_text = textwrap.fill(self.text, width=self.max_width)
        lines = wrapped_text.split('\n')
        text_surfaces = [self.font.render(line, True, (0, 0, 0)) for line in lines]
        max_text_width = max(text_surface.get_width() for text_surface in text_surfaces)

        total_height = sum(text_surface.get_height() + LINE_SPACING for text_surface in text_surfaces)
        bubble_surface = pygame.Surface((max_text_width + 20, total_height + 10), pygame.SRCALPHA)
        pygame.draw.rect(bubble_surface, (255, 255, 255, 200), bubble_surface.get_rect(), 0)
        pygame.draw.rect(bubble_surface, (0, 0, 0, 200), bubble_surface.get_rect(), 1)

        y_offset = 5
        for text_surface in text_surfaces:
            bubble_surface.blit(text_surface, (10, y_offset))
            y_offset += text_surface.get_height() + 5

        return bubble_surface

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
