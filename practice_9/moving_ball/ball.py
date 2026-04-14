import pygame

class Ball:
    def __init__(self, screen_width, screen_height):
        self.x = 100
        self.y = 100
        self.radius = 25
        self.speed = 20
        self.width = screen_width
        self.height = screen_height

    def move(self, key):
        if key == pygame.K_LEFT and self.x - self.radius > 0:
            self.x -= self.speed
        if key == pygame.K_RIGHT and self.x + self.radius < self.width:
            self.x += self.speed
        if key == pygame.K_UP and self.y - self.radius > 0:
            self.y -= self.speed
        if key == pygame.K_DOWN and self.y + self.radius < self.height:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)