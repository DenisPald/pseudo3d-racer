import random
from typing import Tuple

import pygame

from config import *
from utils import load_image


class Player(pygame.sprite.Sprite):
    image_normal = load_image('car.png')
    image_normal = pygame.transform.scale(
        image_normal, (ROAD_WIDTH // ROAD_LANES * PLAYER_WIDTH_SCALE,
                       SEGMENT_LENGTH * PLAYER_HEIGHT_SCALE))

    image_left = load_image('car_left.png')
    image_left = pygame.transform.scale(
        image_left, (ROAD_WIDTH // ROAD_LANES * PLAYER_WIDTH_SCALE,
                     SEGMENT_LENGTH * PLAYER_HEIGHT_SCALE))

    image_right = load_image('car_right.png')
    image_right = pygame.transform.scale(
        image_right, (ROAD_WIDTH // ROAD_LANES * PLAYER_WIDTH_SCALE,
                      SEGMENT_LENGTH * PLAYER_HEIGHT_SCALE))

    def __init__(self, group) -> None:
        super().__init__(*group)
        self.x = 0
        self.y = 0
        self.z = DISTANCE
        self.speed = 15
        self.turn_speed = TURN_SPEED_CONST * self.speed
        self.direction = None

        self.image = Player.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = (WIDTH // 2) - (self.rect.w // 2)
        self.rect.y = HEIGHT - self.rect.h - 10

    def update(self):
        cur_segment = self.road.get_segment(self.z)
        self.y = cur_segment.y
        half_x = cur_segment.x - (self.x * ROAD_WIDTH)
        if abs(half_x) > ROAD_WIDTH // 2:
            if self.speed >= MAX_SPEED / 3:
                self.speed -= 2 * ACCEL

        if self.speed < MAX_SPEED:
            self.speed += ACCEL
        self.z += self.speed

        self.turn_speed = TURN_SPEED_CONST * self.speed

        if self.z > ROAD_LENGTH:
            self.z -= ROAD_LENGTH

        if self.direction == LEFT:
            self.x -= self.turn_speed
            self.image = Player.image_left
        elif self.direction == RIGHT:
            self.x += self.turn_speed
            self.image = Player.image_right
        else:
            self.image = Player.image_normal

    def set_direction(self, direction):
        self.direction = direction

    def set_road(self, road):
        self.road = road


class Camera():
    def __init__(self, player: Player) -> None:
        self.player = player
        self.x = WIDTH // 2
        self.y = CAMERA_HEIGHT
        self.z = self.player.z - DISTANCE
        self.dist_to_plane = 1 / (CAMERA_HEIGHT / DISTANCE)

    def update(self):
        self.x = (self.player.x * ROAD_WIDTH) + ROAD_WIDTH // 2
        self.y = self.player.y + CAMERA_HEIGHT
        self.z = self.player.z - DISTANCE


class Segment():
    def __init__(self, index: int, z: int, camera: Camera,
                 surface: pygame.surface.Surface, x) -> None:
        self.surface = surface

        self.camera = camera
        self.index = index
        self.x = x
        self.y = 0
        self.z = z
        self.scale = 0
        self.color = Colors.DARK.value if (
            index // RUMBLE_SEGMENTS) % 2 == 0 else Colors.LIGHT.value

    def render(self) -> Tuple[int, int, int]:
        x_trans = self.x - self.camera.x
        y_trans = self.y - self.camera.y
        z_trans = self.z - self.camera.z
        scale = self.camera.dist_to_plane / z_trans
        projected_x = scale * x_trans
        projected_y = scale * y_trans
        projected_w = scale * ROAD_WIDTH

        screen_x = round((1 + projected_x) * HALF_WIDTH)
        screen_y = round((1 - projected_y) * HALF_HEIGHT)
        screen_w = round(projected_w * HALF_WIDTH)
        return (screen_x, screen_y, screen_w)


class Tile(pygame.sprite.Sprite):
    colors = ('red', 'green', 'yellow', 'brown')

    def __init__(self, x: int, y: int, z: int, camera: Camera, group,
                 road) -> None:
        super().__init__(group)
        self.image = pygame.Surface(
            ((ROAD_WIDTH // ROAD_LANES) * TILE_WIDTH_SCALE, TILE_HEIGHT))
        self.color = random.choice(Tile.colors)
        self.image.fill(self.color)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.z = z
        self.camera = camera
        self.road = road
        self.rect.x = x
        self.rect.y = y - self.rect.h

        self.height = self.rect.h
        self.width = self.rect.w

        self.player = camera.player

    def render(self) -> Tuple[int, int, int, int]:
        x_trans = self.x - self.camera.x
        y_trans = self.y
        z_trans = self.z - self.camera.z
        scale = self.camera.dist_to_plane / z_trans
        projected_x = scale * x_trans
        projected_y = scale * y_trans
        projected_w = scale * self.width
        projected_h = scale * self.height

        screen_x = round((1 + projected_x) * HALF_WIDTH)
        screen_y = round((1 - projected_y) * HALF_HEIGHT)
        screen_w = round(projected_w * HALF_WIDTH)
        screen_h = round(projected_h * HALF_HEIGHT)
        return (screen_x, screen_y, screen_w, screen_h)

    def update(self):
        render_this = True

        if self.z < self.camera.z and self.camera.z > 0:
            self.camera.z -= ROAD_LENGTH
        # Если сзади камеры или слишком далеко то не рисуем
        if self.z <= self.camera.z + DISTANCE or self.z >= self.camera.z + TILE_RENDER_RANGE * SEGMENT_LENGTH:
            render_this = False

        if render_this:
            if self.z < self.camera.z and self.camera.z > 0:
                self.camera.z -= ROAD_LENGTH
            x, y, w, h = self.render()
            self.rect.x = x
            self.rect.y = y
            self.rect.w = w
            self.rect.h = h
            self.image.fill(self.color)
        else:
            self.rect.x = 0
            self.rect.y = 0
            self.rect.w = 0
            self.rect.h = 0

        if self.z > self.camera.z:
            self.camera.z += ROAD_LENGTH

        self.image: pygame.surface.Surface = pygame.transform.scale(
            self.image, self.rect.size)


class Road():
    def __init__(self, camera: Camera, surface: pygame.surface.Surface,
                 tile_group) -> None:
        self.surface = surface
        self.segments = []
        self.tiles = []
        self.camera = camera
        self.maxy = 0
        self.tile_group = tile_group
        self.reset_road()

    def reset_road(self):
        for i in range(TOTAL_SEGMENTS):
            self.segments.append(
                Segment(i, i * SEGMENT_LENGTH, self.camera, self.surface, 0))

        for i in range(1, len(MAP)):
            self.segments[i].x = self.segments[i - 1].x + MAP[i][0]
            self.segments[i].y = self.segments[i - 1].y + MAP[i][1]

        for i in range(RUMBLE_SEGMENTS):
            self.segments[i].color = Colors.FINISH1.value
            self.segments[RUMBLE_SEGMENTS - i].color = Colors.FINISH2.value

        diff = (TOTAL_SEGMENTS // TOTAL_TILES) * SEGMENT_LENGTH
        z = 0
        for i in range(TOTAL_TILES):
            z += diff
            x = random.randint(0, ROAD_WIDTH)
            tile = Tile(x, 0, z, self.camera, self.tile_group, self)
            self.tiles.append(tile)
            self.tile_group.add(tile)

    def get_segment(self, z) -> Segment:
        index = int((z // SEGMENT_LENGTH) % TOTAL_SEGMENTS)
        return self.segments[index]

    def render(self):
        base_index = self.get_segment(self.camera.z).index
        for i in range(RENDERING_RANGE):

            past_index = (i + base_index) % TOTAL_SEGMENTS
            current_index = (i + 1 + base_index) % TOTAL_SEGMENTS

            past = self.segments[past_index]
            current = self.segments[current_index]

            if past_index == TOTAL_SEGMENTS - 1:
                current = self.segments[0]
                #Костыль для отрисовки нулевого элемента
                past = Segment(0, -SEGMENT_LENGTH, self.camera, self.surface,
                               0)
                current_index = 1
                past_index = 0

            if current_index < base_index and self.camera.z > 0:
                self.camera.z -= ROAD_LENGTH

            if current.z <= self.camera.z + DISTANCE:
                continue

            x1, y1, w1 = past.render()
            x2, y2, w2 = current.render()

            if current_index < base_index:
                self.camera.z += ROAD_LENGTH

            asphalt_color = current.color[0]
            #Координаты для отрисовки асфальта
            ac1 = (x1, y1)
            ac2 = (x2, y2)
            ac3 = (x2 + w2, y2)
            ac4 = (x1 + w1, y1)
            grass_color = current.color[1]
            #Координаты для отрисовки травы
            gc1 = (0, y1)
            gc2 = (0, y2)
            gc3 = (WIDTH, y2)
            gc4 = (WIDTH, y1)
            pygame.draw.polygon(self.surface, grass_color,
                                [gc1, gc2, gc3, gc4])
            pygame.draw.polygon(self.surface, asphalt_color,
                                [ac1, ac2, ac3, ac4])
            lane_color = current.color[2]
            if lane_color:
                lane_w1 = w1 / 100
                lane_w2 = w2 / 100
                indent1 = w1 / ROAD_LANES
                indent2 = w2 / ROAD_LANES
                lane_x1 = x1
                lane_x2 = x2
                for i in range(1, ROAD_LANES):
                    lane_x1 += indent1
                    lane_x2 += indent2
                    lc1 = (lane_x1 - lane_w1, y1)
                    lc2 = (lane_x1 + lane_w1, y1)
                    lc3 = (lane_x2 + lane_w2, y2)
                    lc4 = (lane_x2 - lane_w2, y2)
                    pygame.draw.polygon(self.surface, lane_color,
                                        [lc1, lc2, lc3, lc4])

            curb_color = current.color[3]
            curb_width_1 = (w1 / 30)
            curb_width_2 = (w2 / 30)
            cc1 = (x1, y1)
            cc2 = (x2, y2)
            cc3 = (x2 + curb_width_2, y2)
            cc4 = (x1 + curb_width_1, y1)
            pygame.draw.polygon(self.surface, curb_color, [cc1, cc2, cc3, cc4])
            cc1 = (x1 + w1, y1)
            cc2 = (x2 + w2, y2)
            cc3 = (x2 + w2 - curb_width_2, y2)
            cc4 = (x1 + w1 - curb_width_1, y1)
            pygame.draw.polygon(self.surface, curb_color, [cc1, cc2, cc3, cc4])
