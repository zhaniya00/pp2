import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

ball = Ball(300, 200, 25, 20, WIDTH, HEIGHT)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # обработка нажатых клавиш (ВАЖНО: через get_pressed)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ball.move_up()
    if keys[pygame.K_DOWN]:
        ball.move_down()
    if keys[pygame.K_LEFT]:
        ball.move_left()
    if keys[pygame.K_RIGHT]:
        ball.move_right()

    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()