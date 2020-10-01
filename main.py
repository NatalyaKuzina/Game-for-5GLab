import pygame
from copy import deepcopy
import numpy as np
from numba import njit

# determine the size of the playing field (WIDTH&HEIGHT) and tiles.
RES = WIDTH, HEIGHT = 900, 900
TILE = 2
W, H = WIDTH // TILE, HEIGHT // TILE

pygame.init()
surface = pygame.display.set_mode(RES)

next_field = np.array([[0 for i in range(W)] for j in range(H)])
current_field = np.array([[1 if i == W // 2 or j == H // 2 else 0 for i in range(W)] for j in range(H)])

# function to check the status of tiles
@njit(fastmath=True)
def check_cells(current_field, next_field):
    res = []
    for x in range(W):
        for y in range(H):
            count = 0
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if current_field[j % H][i % W] == 1:
                        count += 1

            if current_field[y][x] == 1:
                count -= 1
                if count == 2 or count == 3:
                    next_field[y][x] = 1
                    res.append((x,y))
                else:
                    next_field[y][x] = 0
            else:
                if count == 3:
                    next_field[y][x] = 1
                    res.append((x, y))
                else:
                    next_field[y][x] = 0
    return next_field, res

while True:
    surface.fill(pygame.Color('white'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    # building a grid
    [pygame.draw.line(surface, pygame.Color('lightgrey'), (x, 0), (x, HEIGHT)) for x in range(0, WIDTH, TILE)]
    [pygame.draw.line(surface, pygame.Color('lightgrey'), (0, y), (WIDTH, y)) for y in range(0, HEIGHT, TILE)]
    # draw life
    next_field, res = check_cells(current_field, next_field)
    [pygame.draw.rect(surface, pygame.Color('lightblue'),
                      (x * TILE + 1, y * TILE + 1, TILE - 1, TILE - 1)) for x,y in res]

    current_field = deepcopy(next_field)
    pygame.display.flip()
