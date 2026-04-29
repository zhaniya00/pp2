import pygame
import random
import sys

from persistence import load_settings, save_settings, load_leaderboard, save_score
from racer import (Road, Coin, PowerUp, Obstacle, TrafficCar, PlayerCar,
                   draw_hud, DIFF_PARAMS, CAR_COLORS,
                   ROAD_LEFT, ROAD_RIGHT, LANE_X, DARK)
from ui import (draw_main_menu, draw_settings, draw_leaderboard,
                draw_game_over, draw_name_entry, CAR_COLORS as UI_CAR_COLORS)

pygame.init()
W, H = 400, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer – TSIS 3")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont(None, 52)
font_med   = pygame.font.SysFont(None, 34)
font_small = pygame.font.SysFont(None, 22)

TOTAL_DISTANCE = 2000   # metres to finish

# ─── State machine ────────────────────────────────────────────────────────────
STATE_MENU       = "menu"
STATE_NAME       = "name"
STATE_PLAY       = "play"
STATE_GAMEOVER   = "gameover"
STATE_LEADERBOARD= "leaderboard"
STATE_SETTINGS   = "settings"

state    = STATE_MENU
settings = load_settings()
board    = load_leaderboard()
username = ""
name_input = ""

# Game session variables (reset each run)
def new_session():
    diff   = settings.get("difficulty", "normal")
    params = DIFF_PARAMS[diff]
    car_col = CAR_COLORS.get(settings.get("car_color", "red"), (220, 50, 50))

    player = PlayerCar(W // 2 - 25, H - 100, car_col)
    road   = Road(W, H)

    return {
        "player":       player,
        "road":         road,
        "coins":        [],
        "powerups":     [],
        "obstacles":    [],
        "traffic":      [],
        "score":        0,
        "coin_count":   0,
        "distance":     0,
        "base_speed":   params["enemy_base"],
        "current_speed":float(params["enemy_base"]),
        "params":       params,
        "frame":        0,
        "active_pu":    None,   # only one power-up at a time
        "finished":     False,
    }

session = new_session()
last_score  = 0
last_dist   = 0
last_coins  = 0

# ─── Main loop ────────────────────────────────────────────────────────────────
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    dt     = clock.tick(60)
    clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True

        elif event.type == pygame.KEYDOWN and state == STATE_NAME:
            if event.key == pygame.K_RETURN and name_input.strip():
                username = name_input.strip()[:16]
                session  = new_session()
                state    = STATE_PLAY
            elif event.key == pygame.K_BACKSPACE:
                name_input = name_input[:-1]
            else:
                if len(name_input) < 16:
                    name_input += event.unicode

    # ─── MENU ───────────────────────────────────────────────────────────────
    if state == STATE_MENU:
        btns = draw_main_menu(screen, mx, my, W, H,
                              (font_big, font_med))
        if clicked:
            if btns["play"].collidepoint(mx, my):
                name_input = ""
                state = STATE_NAME
            elif btns["leaderboard"].collidepoint(mx, my):
                board = load_leaderboard()
                state = STATE_LEADERBOARD
            elif btns["settings"].collidepoint(mx, my):
                state = STATE_SETTINGS
            elif btns["quit"].collidepoint(mx, my):
                running = False

    # ─── NAME ENTRY ──────────────────────────────────────────────────────────
    elif state == STATE_NAME:
        btns = draw_name_entry(screen, mx, my, W, H,
                               (font_big, font_med, font_small), name_input)
        if clicked and btns["start"].collidepoint(mx, my):
            if name_input.strip():
                username = name_input.strip()[:16]
                session  = new_session()
                state    = STATE_PLAY

    # ─── SETTINGS ────────────────────────────────────────────────────────────
    elif state == STATE_SETTINGS:
        btns = draw_settings(screen, mx, my, W, H,
                             (font_big, font_med, font_small), settings)
        if clicked:
            if btns["sound"].collidepoint(mx, my):
                settings["sound"] = not settings["sound"]
                save_settings(settings)
            elif btns["back"].collidepoint(mx, my):
                state = STATE_MENU
            else:
                for cn in UI_CAR_COLORS:
                    k = f"color_{cn}"
                    if k in btns and btns[k].collidepoint(mx, my):
                        settings["car_color"] = cn
                        save_settings(settings)
                for d in ["easy", "normal", "hard"]:
                    k = f"diff_{d}"
                    if k in btns and btns[k].collidepoint(mx, my):
                        settings["difficulty"] = d
                        save_settings(settings)

    # ─── LEADERBOARD ─────────────────────────────────────────────────────────
    elif state == STATE_LEADERBOARD:
        btns = draw_leaderboard(screen, mx, my, W, H,
                                (font_big, font_med, font_small), board)
        if clicked and btns["back"].collidepoint(mx, my):
            state = STATE_MENU

    # ─── GAME OVER ───────────────────────────────────────────────────────────
    elif state == STATE_GAMEOVER:
        btns = draw_game_over(screen, mx, my, W, H,
                              (font_big, font_med, font_small),
                              last_score, last_dist, last_coins)
        if clicked:
            if btns["retry"].collidepoint(mx, my):
                session = new_session()
                state   = STATE_PLAY
            elif btns["menu"].collidepoint(mx, my):
                state = STATE_MENU

    # ─── GAMEPLAY ────────────────────────────────────────────────────────────
    elif state == STATE_PLAY:
        g = session
        p = g["player"]

        # ── Input ──
        keys = pygame.key.get_pressed()
        p.move(keys, W)
        p.update()

        # ── Speed / difficulty scaling ──
        g["frame"] += 1
        step = g["params"]["density_step"]
        speed_level = g["distance"] // step
        g["current_speed"] = g["base_speed"] + speed_level * 0.8
        road_speed = g["current_speed"] * p.get_speed_mult()

        # ── Road ──
        g["road"].update(road_speed)

        # ── Distance ──
        g["distance"] += road_speed / 60   # metres
        g["distance"]  = round(g["distance"], 1)

        # ── Road events: check player on nitro strip or bump ──
        for zone, _ in g["road"].nitro_boost_zones:
            if p.rect.colliderect(zone) and not p.nitro_active:
                p.apply_powerup("nitro")
        for bump, _ in g["road"].speed_bumps:
            if p.rect.colliderect(bump):
                p.slow_timer = max(p.slow_timer, 60)

        # ── Spawn coins ──
        if random.randint(1, 30) == 1:
            g["coins"].append(Coin(W, road_speed))

        # ── Spawn power-ups (only if none active) ──
        if g["active_pu"] is None and random.randint(1, 200) == 1:
            g["powerups"].append(PowerUp(W, road_speed))

        # ── Spawn obstacles ──
        obs_chance = int(max(4, 60 - speed_level * 3))
        if random.randint(1, obs_chance) == 1:
            g["obstacles"].append(Obstacle(W, road_speed, p.rect))

        # ── Spawn traffic ──
        traffic_chance = int(max(3, 50 - speed_level * 3))
        if random.randint(1, traffic_chance) == 1:
            g["traffic"].append(TrafficCar(W, g["current_speed"], p.rect))

        # ── Update coins ──
        for coin in g["coins"][:]:
            coin.update(road_speed)
            if p.rect.colliderect(coin.rect):
                g["coins"].remove(coin)
                g["coin_count"] += coin.value
                g["score"]      += coin.value * 10
            elif coin.rect.y > H:
                g["coins"].remove(coin)

        # ── Update power-ups ──
        for pu in g["powerups"][:]:
            pu.update(road_speed)
            if p.rect.colliderect(pu.rect) and g["active_pu"] is None:
                g["powerups"].remove(pu)
                g["active_pu"] = pu.kind
                if pu.kind == "repair":
                    # instant: clear one obstacle nearest to player
                    if g["obstacles"]:
                        nearest = min(g["obstacles"],
                                      key=lambda o: abs(o.rect.centery - p.rect.centery))
                        g["obstacles"].remove(nearest)
                    g["active_pu"] = None
                else:
                    p.apply_powerup(pu.kind)
            elif pu.expired():
                g["powerups"].remove(pu)

        # Clear active_pu ref when nitro ends
        if g["active_pu"] == "nitro" and not p.nitro_active:
            g["active_pu"] = None
        if g["active_pu"] == "shield" and not p.shield_active:
            g["active_pu"] = None

        # ── Update obstacles ──
        game_over = False
        for obs in g["obstacles"][:]:
            obs.update(road_speed)
            if obs.rect.y > H:
                g["obstacles"].remove(obs)
                continue
            if p.rect.colliderect(obs.rect):
                if obs.kind == "oil":
                    p.hit_oil()
                    g["obstacles"].remove(obs)
                elif obs.kind in ("barrier", "pothole"):
                    if p.try_hit():
                        game_over = True
                    else:
                        g["obstacles"].remove(obs)

        # ── Update traffic ──
        for car in g["traffic"][:]:
            car.update(road_speed)
            if car.rect.y > H:
                g["traffic"].remove(car)
                continue
            if p.rect.colliderect(car.rect):
                if p.try_hit():
                    game_over = True
                else:
                    g["traffic"].remove(car)

        # ── Finish check ──
        if g["distance"] >= TOTAL_DISTANCE:
            game_over = True
            g["score"] += 500   # bonus for finishing

        if game_over:
            last_score = g["score"]
            last_dist  = int(g["distance"])
            last_coins = g["coin_count"]
            board = save_score(username, last_score, last_dist, last_coins)
            state = STATE_GAMEOVER

        # ── Draw ──
        screen.fill(DARK)
        g["road"].draw(screen)
        for coin in g["coins"]:    coin.draw(screen)
        for pu   in g["powerups"]: pu.draw(screen)
        for obs  in g["obstacles"]:obs.draw(screen)
        for car  in g["traffic"]:  car.draw(screen)
        p.draw(screen)

        draw_hud(screen, W,
                 g["score"], int(g["distance"]), g["coin_count"],
                 TOTAL_DISTANCE, p, font_med, font_small)

    pygame.display.flip()

pygame.quit()
sys.exit()