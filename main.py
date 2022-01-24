import pygame

from config import *
from objects import *

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.LayeredUpdates()
    player = Player(player_group)
    player_group.add(player)
    camera = Camera(player)
    road = Road(camera, screen, tiles_group)
    player.set_road(road)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((134, 209, 236))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.set_direction(LEFT)
                if event.key == pygame.K_d:
                    player.set_direction(RIGHT)
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    player.set_direction(None)

        camera.update()
        road.render()
        player_group.update()
        player_group.draw(screen)
        tiles_group.update()
        tiles_group.draw(screen)

        f1 = pygame.font.Font(None, 40)
        text = f1.render(f'{str(int(player.z))}/{str(int(ROAD_LENGTH))}', True,
                         (0, 0, 0))
        screen.blit(text, (0, 0))

        pygame.display.flip()

        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(FPS)
    pygame.quit()
