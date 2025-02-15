import pygame

class Ground:
    def __init__(self, x, y, width, height, color="brown"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
