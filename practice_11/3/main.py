import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint SIMPLE")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BLACK)

palette = [
    (240,144,245),
    (245,240,144),
    (118,188,254),
    (167,247,153),
    (180,139,224),
    (255, 255, 255)
]

color = (240,144,245)

tool = 'brush'

radius = 10

drawing = False

start_pos = (0, 0)

font = pygame.font.SysFont(None, 24)


while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = 'brush'
            elif event.key == pygame.K_2:
                tool = 'rect'
            elif event.key == pygame.K_3:
                tool = 'circle'
            elif event.key == pygame.K_4:
                tool = 'eraser'
            elif event.key == pygame.K_5:
                tool = 'square'
            elif event.key == pygame.K_6:
                tool = 'right triangle'
            elif event.key == pygame.K_7:
                tool = 'equilateral triangle'
            elif event.key == pygame.K_8:
                tool = 'rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            for i, c in enumerate(palette):
                if 10 + i * 50 <= x <= 50 + i * 50 and 10 <= y <= 50:
                    color = c

            if event.button == 1:
                drawing = True
                start_pos = event.pos

            elif event.button == 3:
                radius = max(1, radius - 2)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                end_pos = event.pos

                if tool == 'rect':
                    pygame.draw.rect(
                        canvas,
                        color,
                        (
                            min(start_pos[0], end_pos[0]),
                            min(start_pos[1], end_pos[1]),
                            abs(start_pos[0] - end_pos[0]),
                            abs(start_pos[1] - end_pos[1])
                        ),
                        2
                    )

                elif tool == 'circle':
                    r = int(
                        (
                            (start_pos[0] - end_pos[0]) ** 2 +
                            (start_pos[1] - end_pos[1]) ** 2
                        ) ** 0.5
                    )
                    pygame.draw.circle(canvas, color, start_pos, r, 2)

                elif tool == "square":
                    pygame.draw.rect(canvas, color, (x, y, 100, 100), 2)

                elif tool == "equilateral triangle":
                    points = [
                        (start_pos[0], start_pos[1]),
                        (end_pos[0], end_pos[1]),
                        (start_pos[0], end_pos[1])
                    ]

                    pygame.draw.polygon(canvas, color, points, 2)

                elif tool == "right triangle":
                    side = abs(end_pos[0] - start_pos[0])

                    points = [
                        (start_pos[0], start_pos[1]),
                        (start_pos[0] - side//2, start_pos[1] + side),
                        (start_pos[0] + side//2, start_pos[1] + side)
                    ]

                    pygame.draw.polygon(canvas, color, points, 2)

                elif tool == "rhombus":

                    center_x = (start_pos[0] + end_pos[0]) // 2
                    center_y = (start_pos[1] + end_pos[1]) // 2

                    points = [
                        (center_x, start_pos[1]),
                        (end_pos[0], center_y),
                        (center_x, end_pos[1]),
                        (start_pos[0], center_y)
                    ]

                    pygame.draw.polygon(canvas, color, points, 2)

        if event.type == pygame.MOUSEMOTION:
            if drawing:

                if tool == 'brush':
                    pygame.draw.circle(canvas, color, event.pos, radius)

                elif tool == 'eraser':
                    pygame.draw.circle(canvas, BLACK, event.pos, radius)

    screen.fill(BLACK)

    screen.blit(canvas, (0, 0))

    for i, c in enumerate(palette):
        pygame.draw.rect(screen, c, (10 + i * 50, 10, 40, 40))

    text = font.render(f"Tool: {tool}", True, WHITE)
    screen.blit(text, (10, 60))

    pygame.display.flip()

    clock.tick(60)