import pygame

# ─── Palette ────────────────────────────────────────────────────────────────
BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
GRAY    = (60,  60,  60)
LGRAY   = (120, 120, 120)
YELLOW  = (255, 220, 0)
GREEN   = (50,  200, 80)
RED     = (220, 50,  50)
BLUE    = (50,  120, 220)
ORANGE  = (255, 140, 0)
CYAN    = (0,   210, 210)
DARK    = (15,  15,  25)
ROAD    = (40,  40,  40)
STRIPE  = (200, 200, 0)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  120, 220),
    "green":  (50,  200, 80),
    "yellow": (220, 200, 0),
    "white":  (230, 230, 230),
}

def draw_button(surface, rect, text, font, hover=False,
                color=GRAY, hover_color=LGRAY, text_color=WHITE, border=2):
    c = hover_color if hover else color
    pygame.draw.rect(surface, c, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, border, border_radius=8)
    label = font.render(text, True, text_color)
    lx = rect.x + (rect.width  - label.get_width())  // 2
    ly = rect.y + (rect.height - label.get_height()) // 2
    surface.blit(label, (lx, ly))

def draw_text_center(surface, text, font, color, y, width):
    label = font.render(text, True, color)
    surface.blit(label, ((width - label.get_width()) // 2, y))

# ─── Main Menu ───────────────────────────────────────────────────────────────
def draw_main_menu(surface, mx, my, W, H, fonts):
    surface.fill(DARK)
    # decorative road stripes
    for i in range(0, H, 60):
        pygame.draw.rect(surface, ROAD, (W//2 - 80, i, 160, 40), border_radius=4)

    title_font, btn_font = fonts
    draw_text_center(surface, "🏎  RACER", title_font, YELLOW, 80, W)
    draw_text_center(surface, "TSIS 3", btn_font, LGRAY, 130, W)

    buttons = {}
    labels = ["Play", "Leaderboard", "Settings", "Quit"]
    for i, lbl in enumerate(labels):
        r = pygame.Rect(W//2 - 100, 200 + i*70, 200, 50)
        hover = r.collidepoint(mx, my)
        draw_button(surface, r, lbl, btn_font, hover=hover)
        buttons[lbl.lower()] = r
    return buttons

# ─── Settings Screen ─────────────────────────────────────────────────────────
def draw_settings(surface, mx, my, W, H, fonts, settings):
    surface.fill(DARK)
    title_font, btn_font, small_font = fonts
    draw_text_center(surface, "Settings", title_font, YELLOW, 40, W)

    buttons = {}
    y = 120

    # Sound toggle
    sound_lbl = f"Sound:  {'ON' if settings['sound'] else 'OFF'}"
    r = pygame.Rect(W//2 - 120, y, 240, 45)
    hover = r.collidepoint(mx, my)
    col = GREEN if settings['sound'] else GRAY
    draw_button(surface, r, sound_lbl, btn_font, hover=hover, color=col)
    buttons["sound"] = r
    y += 70

    # Car color
    draw_text_center(surface, "Car Color:", btn_font, WHITE, y, W)
    y += 36
    color_names = list(CAR_COLORS.keys())
    sw = 200 // len(color_names)
    for i, cn in enumerate(color_names):
        cr = pygame.Rect(W//2 - 100 + i*sw, y, sw-4, 34)
        col = CAR_COLORS[cn]
        selected = (settings["car_color"] == cn)
        pygame.draw.rect(surface, col, cr, border_radius=6)
        if selected:
            pygame.draw.rect(surface, WHITE, cr, 3, border_radius=6)
        buttons[f"color_{cn}"] = cr
    y += 55

    # Difficulty
    draw_text_center(surface, "Difficulty:", btn_font, WHITE, y, W)
    y += 36
    diffs = ["easy", "normal", "hard"]
    dw = 200 // len(diffs)
    for i, d in enumerate(diffs):
        dr = pygame.Rect(W//2 - 100 + i*dw, y, dw-4, 34)
        selected = (settings["difficulty"] == d)
        col = BLUE if selected else GRAY
        draw_button(surface, dr, d.capitalize(), small_font, hover=dr.collidepoint(mx, my), color=col)
        buttons[f"diff_{d}"] = dr
    y += 65

    # Back
    br = pygame.Rect(W//2 - 80, y, 160, 45)
    draw_button(surface, br, "Back", btn_font, hover=br.collidepoint(mx, my))
    buttons["back"] = br

    return buttons

# ─── Leaderboard Screen ───────────────────────────────────────────────────────
def draw_leaderboard(surface, mx, my, W, H, fonts, board):
    surface.fill(DARK)
    title_font, btn_font, small_font = fonts
    draw_text_center(surface, "Top 10 Leaderboard", title_font, YELLOW, 30, W)

    header = small_font.render("#   Name           Score  Dist  Coins", True, LGRAY)
    surface.blit(header, (20, 80))
    pygame.draw.line(surface, LGRAY, (20, 100), (W-20, 100), 1)

    for i, entry in enumerate(board[:10]):
        y = 110 + i * 38
        col = YELLOW if i == 0 else (LGRAY if i < 3 else WHITE)
        row = f"{i+1:<3} {entry['name'][:12]:<13} {entry['score']:<7} {entry['distance']:<5} {entry['coins']}"
        lbl = small_font.render(row, True, col)
        surface.blit(lbl, (20, y))

    if not board:
        draw_text_center(surface, "No scores yet!", btn_font, LGRAY, 200, W)

    br = pygame.Rect(W//2 - 80, H - 70, 160, 45)
    draw_button(surface, br, "Back", btn_font, hover=br.collidepoint(mx, my))
    return {"back": br}

# ─── Game Over Screen ─────────────────────────────────────────────────────────
def draw_game_over(surface, mx, my, W, H, fonts, score, distance, coins):
    surface.fill(DARK)
    title_font, btn_font, small_font = fonts
    draw_text_center(surface, "GAME OVER", title_font, RED, 80, W)

    stats = [
        f"Score:     {score}",
        f"Distance:  {distance} m",
        f"Coins:     {coins}",
    ]
    for i, s in enumerate(stats):
        lbl = btn_font.render(s, True, WHITE)
        surface.blit(lbl, (W//2 - lbl.get_width()//2, 180 + i*40))

    retry_r = pygame.Rect(W//2 - 110, 360, 100, 45)
    menu_r  = pygame.Rect(W//2 +  10, 360, 100, 45)
    draw_button(surface, retry_r, "Retry",     btn_font, hover=retry_r.collidepoint(mx, my), color=GREEN)
    draw_button(surface, menu_r,  "Main Menu", btn_font, hover=menu_r.collidepoint(mx, my))
    return {"retry": retry_r, "menu": menu_r}

# ─── Username Entry ───────────────────────────────────────────────────────────
def draw_name_entry(surface, mx, my, W, H, fonts, name_text):
    surface.fill(DARK)
    title_font, btn_font, small_font = fonts
    draw_text_center(surface, "Enter Your Name", title_font, YELLOW, 120, W)
    draw_text_center(surface, "Press ENTER to start", small_font, LGRAY, 200, W)

    box = pygame.Rect(W//2 - 120, 240, 240, 50)
    pygame.draw.rect(surface, GRAY, box, border_radius=8)
    pygame.draw.rect(surface, WHITE, box, 2, border_radius=8)
    cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
    name_lbl = btn_font.render(name_text + cursor, True, WHITE)
    surface.blit(name_lbl, (box.x + 10, box.y + 12))

    start_r = pygame.Rect(W//2 - 80, 320, 160, 45)
    draw_button(surface, start_r, "Start", btn_font,
                hover=start_r.collidepoint(mx, my), color=GREEN)
    return {"start": start_r}