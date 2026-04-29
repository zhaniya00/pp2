import pygame
from datetime import datetime
import sys
from tools import flood_fill   # импорт функции

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint SIMPLE")

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

palette = [
    (240,144,245),
    (245,240,144),
    (118,188,254),
    (167,247,153),
    (180,139,224),
    (255, 255, 255)
]

color = palette[0]

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)

tool = "brush"
brush_size = 2

drawing = False
start_pos = (0, 0)
last_pos = None

text_input = ""
text_pos = None
typing = False

font = pygame.font.SysFont(None, 24)


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # клавиатура
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "line"
            elif event.key == pygame.K_3:
                tool = "rect"
            elif event.key == pygame.K_4:
                tool = "circle"
            elif event.key == pygame.K_5:
                tool = "pencil"
            elif event.key == pygame.K_9:
                tool = "fill"
            elif event.key == pygame.K_0:
                tool = "text"

            # размер кисти
            if event.key == pygame.K_z:
                brush_size = 2
            elif event.key == pygame.K_x:
                brush_size = 5
            elif event.key == pygame.K_c:
                brush_size = 10

            # сохранение
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(canvas, filename)

            # текст
            if typing and tool == "text":

                if event.key == pygame.K_RETURN:
                    text_surface = font.render(text_input, True, color)
                    canvas.blit(text_surface, text_pos)
                    typing = False

                elif event.key == pygame.K_ESCAPE:
                    typing = False

                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]

                else:
                    text_input += event.unicode

        # мышь
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # выбор цвета
            for i, c in enumerate(palette):
                if 10 + i*50 <= x <= 50 + i*50 and 10 <= y <= 50:
                    color = c

            drawing = True
            start_pos = event.pos
            last_pos = event.pos

            # заливка
            if tool == "fill":
                flood_fill(canvas, x, y, color, WIDTH, HEIGHT)

            # текст
            if tool == "text":
                text_pos = event.pos
                typing = True
                text_input = ""

        # отпускание мыши
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "line":
                pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

            elif tool == "rect":
                pygame.draw.rect(canvas, color,
                                 (min(start_pos[0], end_pos[0]),
                                  min(start_pos[1], end_pos[1]),
                                  abs(start_pos[0]-end_pos[0]),
                                  abs(start_pos[1]-end_pos[1])),
                                 brush_size)

            elif tool == "circle":
                r = int(((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)**0.5)
                pygame.draw.circle(canvas, color, start_pos, r, brush_size)

        # рисование
        if event.type == pygame.MOUSEMOTION:
            if drawing:

                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, brush_size)

                elif tool == "eraser":
                    pygame.draw.circle(canvas, BLACK, event.pos, brush_size)

                elif tool == "pencil":
                    pygame.draw.line(canvas, color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

    # отрисовка
    screen.fill(BLACK)
    screen.blit(canvas, (0, 0))

    for i, c in enumerate(palette):
        pygame.draw.rect(screen, c, (10 + i*50, 10, 40, 40))

    text = font.render(f"Tool: {tool}", True, WHITE)
    screen.blit(text, (10, 60))

    pygame.display.flip()
    clock.tick(60)