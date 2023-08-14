import pygame

class SpeechBubble:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.font = pygame.font.Font(None, 24)  # Choose a font size
        self.image = self.create_bubble_image()

    def create_bubble_image(self):
        text_surface = self.font.render(self.text, True, (0, 0, 0))  # Black text
        bubble_surface = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10), pygame.SRCALPHA)
        pygame.draw.rect(bubble_surface, (255, 255, 255, 200), bubble_surface.get_rect(), 0)  # White bubble
        pygame.draw.rect(bubble_surface, (0, 0, 0, 200), bubble_surface.get_rect(), 1)  # Black border
        bubble_surface.blit(text_surface, (10, 5))  # Render text inside the bubble
        return bubble_surface

    def draw(self, surface, pos):
        surface.blit(self.image, pos)
