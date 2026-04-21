import pygame
from player import MusicPlayer

pygame.init()

WIDTH, HEIGHT = 500, 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 30)

player = MusicPlayer("music")

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                player.play()
            if event.key == pygame.K_s:  # Stop
                player.stop()
            if event.key == pygame.K_n:  # Next
                player.next_track()
            if event.key == pygame.K_b:  # Previous (Back)
                player.previous_track()
            if event.key == pygame.K_q:  # Quit
                running = False

    # Отображение текущего трека
    track_text = font.render("Track: " + player.current_track_name(), True, (0, 0, 0))
    screen.blit(track_text, (20, 80))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()