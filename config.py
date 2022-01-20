from enum import Enum
from map_file import remake_map

# pygame settings
FPS = 60
WIDTH = 900
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2

# Camera settings
DISTANCE = 500
CAMERA_HEIGHT = 450


# Texture size settings
PLAYER_WIDTH_SCALE = 0.6
PLAYER_HEIGHT_SCALE = 2

TILE_WIDTH_SCALE = 0.8
TILE_HEIGHT = 500


# Road settings
TOTAL_SEGMENTS = 500
SEGMENT_LENGTH = 100
ROAD_WIDTH = 4000  # ось x: Расстояниие от середины дороги(0 координата) до края дороги (единичная координата)
ROAD_LENGTH = TOTAL_SEGMENTS * SEGMENT_LENGTH
RUMBLE_SEGMENTS = 5
ROAD_LANES = 6
MAP = remake_map(TOTAL_SEGMENTS, 100)

RENDERING_RANGE = 150
TILE_RENDER_RANGE = 150

TOTAL_TILES = 5


# Speed settings
ACCEL = 0.5
MAX_SPEED = SEGMENT_LENGTH
TURN_SPEED_CONST = (1 / FPS) * (1 / MAX_SPEED)


class Colors(Enum):
    # Цвет асфальта, цвет травы, цвет разметки, цвет бордюра
    DARK = ((90, 90, 90), (57, 126, 73), (221, 221, 221), (221, 221, 221))
    LIGHT = ((102, 102, 102), (65, 146, 85), None, (183, 49, 47))
    FINISH1 = ((255, 255, 255), (57, 126, 73), None, (0, 0, 0))
    FINISH2 = ((0, 0, 0), (65, 146, 85), None, (255, 255, 255))

LEFT = 0
RIGHT = 1

