import pygame

class Ball:
    def __init__(self):
        self.x = 300
        self.y = 200
        self.radius = 25
        self.speed = 20

    def move(self, key, width, height):
        if key == pygame.K_RIGHT and self.x + self.speed <= width - self.radius:
            self.x += self.speed

        if key == pygame.K_LEFT and self.x - self.speed >= self.radius:
            self.x -= self.speed

        if key == pygame.K_UP and self.y - self.speed >= self.radius:
            self.y -= self.speed

        if key == pygame.K_DOWN and self.y + self.speed <= height - self.radius:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)