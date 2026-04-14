import pygame
from datetime import datetime
import math

class Clock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (400, 300)

        self.hand = pygame.image.load("images/mickey_hand.png")
        self.hand = pygame.transform.scale(self.hand, (200, 20))

    def draw(self):
        now = datetime.now()
        seconds = now.second
        minutes = now.minute

        # angles
        sec_angle = -seconds * 6
        min_angle = -minutes * 6

        # draw seconds hand (left)
        sec_rot = pygame.transform.rotate(self.hand, sec_angle)
        rect = sec_rot.get_rect(center=self.center)
        self.screen.blit(sec_rot, rect)

        # draw minutes hand (right)
        min_rot = pygame.transform.rotate(self.hand, min_angle)
        rect2 = min_rot.get_rect(center=self.center)
        self.screen.blit(min_rot, rect2)