import pygame
import datetime

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.center = (400, 300)

        # load image
        self.hand = pygame.image.load("images/mickey_hand.png")
        self.hand = pygame.transform.scale(self.hand, (200, 50))

        self.rect = self.hand.get_rect(center=self.center)

    def draw_hand(self, angle):
        rotated = pygame.transform.rotate(self.hand, angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect.topleft)

    def update(self):
        now = datetime.datetime.now()

        seconds = now.second
        minutes = now.minute

        sec_angle = -seconds * 6 + 90
        min_angle = -minutes * 6 + 90

        # draw hands
        self.draw_hand(min_angle)
        self.draw_hand(sec_angle)