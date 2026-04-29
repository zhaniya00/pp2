import pygame
import random

# ─── Colors ──────────────────────────────────────────────────────────────────
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
RED     = (220, 50,  50)
ORANGE  = (255, 140, 0)
YELLOW  = (255, 220, 0)
GREEN   = (50,  200, 80)
BLUE    = (50,  120, 220)
GRAY    = (80,  80,  80)
LGRAY   = (160, 160, 160)
DARK    = (15,  15,  25)
ROAD_C  = (45,  45,  45)
STRIPE  = (200, 200, 0)
CYAN    = (0,   220, 220)
PURPLE  = (180, 50,  220)

CAR_COLORS = {
    "red":    (220, 50,  50),
    "blue":   (50,  120, 220),
    "green":  (50,  200, 80),
    "yellow": (220, 200, 0),
    "white":  (230, 230, 230),
}

LANE_X   = [60, 150, 240, 330]   # centre-x of 4 lanes
ROAD_LEFT  = 30
ROAD_RIGHT = 370

DIFF_PARAMS = {
    "easy":   {"enemy_base": 3, "obs_base": 2, "density_step": 800},
    "normal": {"enemy_base": 5, "obs_base": 3, "density_step": 500},
    "hard":   {"enemy_base": 7, "obs_base": 5, "density_step": 300},
}

# ─── Road ─────────────────────────────────────────────────────────────────────
class Road:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.stripe_y = [i * 60 for i in range(H // 60 + 2)]
        self.speed = 6
        self.nitro_boost_zones = []   # (rect, timer)
        self.speed_bumps = []          # (rect, timer)
        self._spawn_timer = 0

    def update(self, speed):
        self.speed = speed
        for sy in range(len(self.stripe_y)):
            self.stripe_y[sy] += speed
            if self.stripe_y[sy] > self.H + 60:
                self.stripe_y[sy] -= (self.H + 120)

        # dynamic events
        self._spawn_timer += 1
        if self._spawn_timer > 180:
            self._spawn_timer = 0
            self._spawn_event()

        for zone in self.nitro_boost_zones[:]:
            zone[1] -= 1
            zone[0].y += speed
            if zone[0].y > self.H or zone[1] <= 0:
                self.nitro_boost_zones.remove(zone)

        for bump in self.speed_bumps[:]:
            bump[1] -= 1
            bump[0].y += speed
            if bump[0].y > self.H or bump[1] <= 0:
                self.speed_bumps.remove(bump)

    def _spawn_event(self):
        lane = random.choice(LANE_X)
        kind = random.choice(["nitro", "bump"])
        r = pygame.Rect(lane - 25, -30, 50, 15)
        if kind == "nitro":
            self.nitro_boost_zones.append([r, 300])
        else:
            self.speed_bumps.append([r, 300])

    def draw(self, surface):
        # Road surface
        pygame.draw.rect(surface, ROAD_C,
                         (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, self.H))
        # Edge lines
        pygame.draw.line(surface, WHITE, (ROAD_LEFT,  0), (ROAD_LEFT,  self.H), 3)
        pygame.draw.line(surface, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, self.H), 3)
        # Lane dashes
        for lx in [110, 200, 290]:
            for sy in self.stripe_y:
                pygame.draw.rect(surface, STRIPE, (lx - 2, sy, 4, 30))

        # Nitro strips (cyan)
        for zone, _ in self.nitro_boost_zones:
            pygame.draw.rect(surface, CYAN, zone, border_radius=3)
            lbl = pygame.font.SysFont(None, 18).render("NITRO", True, BLACK)
            surface.blit(lbl, (zone.x + 2, zone.y))

        # Speed bumps (orange)
        for bump, _ in self.speed_bumps:
            pygame.draw.rect(surface, ORANGE, bump, border_radius=3)


# ─── Weighted Coin (from Practice 11) ────────────────────────────────────────
class Coin:
    VALUES = [1, 2, 3]
    COLORS = {1: YELLOW, 2: ORANGE, 3: CYAN}

    def __init__(self, W, speed):
        lane = random.choice(LANE_X)
        self.rect  = pygame.Rect(lane - 15, -30, 30, 30)
        self.value = random.choice(self.VALUES)
        self.speed = speed

    def update(self, speed):
        self.speed = speed
        self.rect.y += speed

    def draw(self, surface):
        color = self.COLORS[self.value]
        pygame.draw.circle(surface, color,
                           self.rect.center, 15)
        pygame.draw.circle(surface, WHITE,
                           self.rect.center, 15, 2)
        lbl = pygame.font.SysFont(None, 20).render(str(self.value), True, BLACK)
        surface.blit(lbl, (self.rect.centerx - 4, self.rect.centery - 7))


# ─── Power-ups ────────────────────────────────────────────────────────────────
class PowerUp:
    TYPES   = ["nitro", "shield", "repair"]
    COLORS  = {"nitro": CYAN, "shield": BLUE, "repair": GREEN}
    SYMBOLS = {"nitro": "N", "shield": "S", "repair": "R"}
    TIMEOUT = 300   # frames before despawn

    def __init__(self, W, speed):
        lane = random.choice(LANE_X)
        self.rect   = pygame.Rect(lane - 18, -36, 36, 36)
        self.kind   = random.choice(self.TYPES)
        self.speed  = speed
        self.timer  = self.TIMEOUT

    def update(self, speed):
        self.speed = speed
        self.rect.y += speed
        self.timer  -= 1

    def draw(self, surface):
        col = self.COLORS[self.kind]
        pygame.draw.rect(surface, col, self.rect, border_radius=6)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=6)
        sym = pygame.font.SysFont(None, 26).render(self.SYMBOLS[self.kind], True, WHITE)
        surface.blit(sym, (self.rect.centerx - sym.get_width()//2,
                           self.rect.centery - sym.get_height()//2))

    def expired(self):
        return self.timer <= 0 or self.rect.y > 620


# ─── Obstacles ────────────────────────────────────────────────────────────────
class Obstacle:
    KINDS = ["oil", "barrier", "pothole"]
    COLORS = {"oil": (30, 30, 90), "barrier": (180, 30, 30), "pothole": (20, 20, 20)}

    def __init__(self, W, speed, player_rect):
        attempts = 0
        while True:
            lane = random.choice(LANE_X)
            r = pygame.Rect(lane - 22, -50, 44, 24)
            # safe-spawn: not directly above player
            safe_zone = pygame.Rect(player_rect.x - 50, player_rect.y - 150, 150, 200)
            if not r.colliderect(safe_zone) or attempts > 10:
                break
            attempts += 1
        self.rect  = r
        self.kind  = random.choice(self.KINDS)
        self.speed = speed

    def update(self, speed):
        self.speed = speed
        self.rect.y += speed

    def draw(self, surface):
        col = self.COLORS[self.kind]
        if self.kind == "barrier":
            pygame.draw.rect(surface, col, self.rect, border_radius=4)
            pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=4)
            lbl = pygame.font.SysFont(None, 16).render("BARRIER", True, WHITE)
            surface.blit(lbl, (self.rect.x + 2, self.rect.y + 4))
        elif self.kind == "oil":
            pygame.draw.ellipse(surface, col, self.rect)
            pygame.draw.ellipse(surface, (60, 60, 180), self.rect, 2)
        else:  # pothole
            pygame.draw.ellipse(surface, col, self.rect)
            pygame.draw.ellipse(surface, GRAY, self.rect, 3)


# ─── Traffic Enemy (from Practice 11 extended) ───────────────────────────────
class TrafficCar:
    BODY_COLORS = [RED, (200, 100, 0), (160, 0, 160), (0, 160, 160)]

    def __init__(self, W, speed, player_rect):
        attempts = 0
        while True:
            lane = random.choice(LANE_X)
            r = pygame.Rect(lane - 25, -80, 50, 70)
            safe_zone = pygame.Rect(player_rect.x - 60, player_rect.y - 200, 170, 250)
            if not r.colliderect(safe_zone) or attempts > 10:
                break
            attempts += 1
        self.rect  = r
        self.speed = speed + random.uniform(-1, 1)
        self.color = random.choice(self.BODY_COLORS)

    def update(self, speed):
        self.rect.y += self.speed

    def draw(self, surface):
        r = self.rect
        # Body
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        # Windshield
        pygame.draw.rect(surface, (150, 220, 255),
                         (r.x+8, r.y+8, r.w-16, 18), border_radius=3)
        # Wheels
        for wx, wy in [(r.x, r.y+10), (r.x+r.w-10, r.y+10),
                       (r.x, r.y+r.h-20), (r.x+r.w-10, r.y+r.h-20)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 10, 14), border_radius=2)


# ─── Player Car ───────────────────────────────────────────────────────────────
class PlayerCar:
    W = 50
    H = 70

    def __init__(self, x, y, color=(220, 50, 50)):
        self.rect  = pygame.Rect(x, y, self.W, self.H)
        self.color = color
        self.shield_active  = False
        self.nitro_active   = False
        self.nitro_timer    = 0
        self.shield_charges = 0
        self.active_powerup = None
        self.powerup_timer  = 0
        self.slow_timer     = 0   # from oil spill

    def apply_powerup(self, kind):
        self.active_powerup = kind
        if kind == "nitro":
            self.nitro_active  = True
            self.nitro_timer   = 60 * 4   # 4 seconds
            self.powerup_timer = self.nitro_timer
        elif kind == "shield":
            self.shield_active  = True
            self.shield_charges = 1
            self.powerup_timer  = 0   # until hit
        elif kind == "repair":
            self.active_powerup = None  # instant

    def update(self):
        if self.nitro_active:
            self.nitro_timer   -= 1
            self.powerup_timer -= 1
            if self.nitro_timer <= 0:
                self.nitro_active   = False
                self.active_powerup = None
        if self.slow_timer > 0:
            self.slow_timer -= 1

    def get_speed_mult(self):
        if self.nitro_active:
            return 1.6
        if self.slow_timer > 0:
            return 0.5
        return 1.0

    def try_hit(self):
        """Returns True if car is destroyed (no shield)."""
        if self.shield_active and self.shield_charges > 0:
            self.shield_charges -= 1
            self.shield_active   = False
            self.active_powerup  = None
            return False
        return True

    def hit_oil(self):
        self.slow_timer = 120

    def move(self, keys, W):
        speed = 5
        if self.nitro_active:
            speed = 8
        elif self.slow_timer > 0:
            speed = 2
        if keys[pygame.K_LEFT]  and self.rect.left  > ROAD_LEFT:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT] and self.rect.right < ROAD_RIGHT:
            self.rect.x += speed

    def draw(self, surface):
        r = self.rect
        pygame.draw.rect(surface, self.color, r, border_radius=6)
        # Windshield
        pygame.draw.rect(surface, (150, 220, 255),
                         (r.x+8, r.y+8, r.w-16, 18), border_radius=3)
        # Rear window
        pygame.draw.rect(surface, (150, 220, 255),
                         (r.x+8, r.y+r.h-26, r.w-16, 14), border_radius=3)
        # Wheels
        for wx, wy in [(r.x-6, r.y+10), (r.x+r.w-4, r.y+10),
                       (r.x-6, r.y+r.h-24), (r.x+r.w-4, r.y+r.h-24)]:
            pygame.draw.rect(surface, BLACK, (wx, wy, 10, 18), border_radius=3)
        # Shield glow
        if self.shield_active:
            s = pygame.Surface((r.w+20, r.h+20), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (50, 120, 220, 90), (0, 0, r.w+20, r.h+20))
            surface.blit(s, (r.x-10, r.y-10))
        # Nitro flames
        if self.nitro_active:
            for ox in [10, 25, 40]:
                pygame.draw.polygon(surface, ORANGE, [
                    (r.x+ox-4, r.y+r.h),
                    (r.x+ox+4, r.y+r.h),
                    (r.x+ox,   r.y+r.h+14)
                ])


# ─── HUD ──────────────────────────────────────────────────────────────────────
def draw_hud(surface, W, score, distance, coins, total_distance,
             player, font, small_font):
    # Semi-transparent top bar
    bar = pygame.Surface((W, 50), pygame.SRCALPHA)
    bar.fill((0, 0, 0, 160))
    surface.blit(bar, (0, 0))

    surface.blit(font.render(f"Score: {score}", True, YELLOW),     (8, 8))
    surface.blit(font.render(f"Coins: {coins}", True, WHITE),      (8, 28))
    dist_lbl = font.render(f"{distance} m", True, WHITE)
    surface.blit(dist_lbl, (W - dist_lbl.get_width() - 8, 8))

    # Progress bar
    if total_distance > 0:
        prog = min(distance / total_distance, 1.0)
        pygame.draw.rect(surface, GRAY,  (W//2 - 60, 10, 120, 10), border_radius=5)
        pygame.draw.rect(surface, GREEN, (W//2 - 60, 10, int(120*prog), 10), border_radius=5)
        lbl = small_font.render(f"{total_distance - distance}m left", True, LGRAY)
        surface.blit(lbl, (W//2 - lbl.get_width()//2, 22))

    # Active power-up
    if player.active_powerup:
        col = {"nitro": CYAN, "shield": BLUE, "repair": GREEN}.get(player.active_powerup, WHITE)
        txt = player.active_powerup.upper()
        if player.active_powerup == "nitro" and player.nitro_timer > 0:
            secs = player.nitro_timer // 60
            txt += f" {secs+1}s"
        pu_lbl = font.render(f"[ {txt} ]", True, col)
        surface.blit(pu_lbl, (W//2 - pu_lbl.get_width()//2, 35))