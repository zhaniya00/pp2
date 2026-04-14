import pygame
from clock import Clock

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Mickey Clock")

clock = Clock(screen)
fps = pygame.time.Clock()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.draw()

    pygame.display.update()
    fps.tick(1)  # update every second

pygame.quit()