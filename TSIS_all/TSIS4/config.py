import pygame
import json
import os

# ─── Grid / Layout constants ─────────────────────────────────────────────────
SIZE_BLOCK    = 40      # pixel size of one cell
COUNT_BLOCK   = 20      # number of cells per row/column
MARGIN        = 1       # gap between cells (pixels)
HEADER_MARGIN = 60      # height of the score bar at the top

# Derived window size
_grid_px = SIZE_BLOCK * COUNT_BLOCK + MARGIN * (COUNT_BLOCK + 1) + SIZE_BLOCK
size = (_grid_px, HEADER_MARGIN + _grid_px)

# ─── Color palette ───────────────────────────────────────────────────────────
COLORS = {
    "FRAME":  (20,  20,  40),
    "HEADER": (10,  10,  25),
    "BLUE":   (50,  80,  140),
    "DBLUE":  (30,  50,  100),
    "PINK":   (255, 180, 220),
    "FOOD":   (220, 80,  80),
    "POISON": (80,  200, 80),
    "BONUS":  (255, 210, 0),
    "WALL":   (120, 120, 120),
    "SHIELD": (80,  180, 255),
}

# ─── Settings ────────────────────────────────────────────────────────────────
SETTINGS_FILE = "settings.json"

_DEFAULT = {
    "snake_color":    [255, 255, 255],
    "show_grid":      True,
    "sound_enabled":  True,
}

class Settings:
    def __init__(self):
        data = dict(_DEFAULT)
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r") as f:
                    loaded = json.load(f)
                    for k, v in loaded.items():
                        if k in data:
                            data[k] = v
            except Exception:
                pass

        self.snake_color   = tuple(data["snake_color"])
        self.show_grid     = bool(data["show_grid"])
        self.sound_enabled = bool(data["sound_enabled"])

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self._save()

    def _save(self):
        data = {
            "snake_color":   list(self.snake_color),
            "show_grid":     self.show_grid,
            "sound_enabled": self.sound_enabled,
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)