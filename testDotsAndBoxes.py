# From PyGuru 

import pygame

screen = width, height = 300, 300
cellsize = 20
padding = 20
rows = cols = (width -4*padding) // cellsize
print(rows, cols)

pygame.init()
win = pygame.display.set_mode(screen)