import pygame
import datetime
from clock import ClockHand

pygame.init()

WIDTH, HEIGHT = 400, 400
CENTER = (WIDTH // 2, HEIGHT // 2)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

# Загружаем руку Микки (один файл для обеих стрелок)
hand_image_path = "images/mickey_hand.png"
minute_hand = ClockHand(hand_image_path, CENTER)
second_hand = ClockHand(hand_image_path, CENTER)

clock = pygame.time.Clock()
running = True

while running:
    screen.fill((255, 255, 255))  # Белый фон

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    minute = now.minute
    second = now.second

    # Рассчёт углов стрелок
    minute_angle = (minute / 60) * 360
    second_angle = (second / 60) * 360

    # Обновляем стрелки
    minute_hand.update(minute_angle)
    second_hand.update(second_angle)

    # Рисуем стрелки
    minute_hand.draw(screen)
    second_hand.draw(screen)

    pygame.display.flip()
    clock.tick(1)  # Обновляем 1 раз в секунду

pygame.quit()