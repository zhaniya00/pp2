import pygame
import math

class ClockHand:
    def __init__(self, image_path, center, length_scale=1.0):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=center)
        self.center = center
        self.length_scale = length_scale

    def update(self, angle_degrees):
        """Поворачиваем руку по углу (0° = вверх, по часовой стрелке)"""
        # pygame.transform.rotate поворачивает против часовой стрелки, поэтому -angle
        self.image = pygame.transform.rotozoom(self.original_image, -angle_degrees, self.length_scale)
        self.rect = self.image.get_rect(center=self.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)