from enum import Enum
from map_file import MAP, TOTAL_SEGMENTS

FPS = 60
WIDTH = 900
HEIGHT = 900
SIZE = (WIDTH, HEIGHT)
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
ACCEL = 1
DISTANCE = 500
CAMERA_HEIGHT = 450
ROAD_WIDTH = 4000  # ось x: Расстояниие от середины дороги(0 координата) до края дороги (единичная координата)
SEGMENT_LENGTH = 100
RUMBLE_SEGMENTS = 5
ROAD_LENGTH = TOTAL_SEGMENTS * SEGMENT_LENGTH
RENDERING_RANGE = 150
TILE_RENDER_RANGE = 20
ROAD_LANES = 6 #Менять в связке с шириной дороги
MAX_SPEED = SEGMENT_LENGTH
TURN_SPEED_CONST = (1 / FPS) * (1 / MAX_SPEED)

PLAYER_WIDTH_SCALE = 0.6
PLAYER_HEIGHT_SCALE = 2

TILE_WIDTH_SCALE = 10
TILE_HEIGHT_SCALE = 10


class Colors(Enum):
    # Цвет асфальта, цвет травы, цвет разметки, цвет бордюра
    DARK = ((90, 90, 90), (57, 126, 73), (221, 221, 221), (221, 221, 221))
    LIGHT = ((102, 102, 102), (65, 146, 85), None, (183, 49, 47))
    FINISH1 = ((255, 255, 255), (57, 126, 73), None, (0, 0, 0))
    FINISH2 = ((0, 0, 0), (65, 146, 85), None, (255, 255, 255))

LEFT = 0
RIGHT = 1

TOTAL_TILES = 10
