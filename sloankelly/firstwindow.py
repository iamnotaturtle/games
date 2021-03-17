import pygame, os, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((800, 600))
background = pygame.Color(100, 149, 237)

image = pygame.image.load('./resources/intro/invaders.png')

while True:
    surface.fill(background)
    surface.blit(image, (0, 0), (32, 0, 32, 32)) # x, y, width, height

    pygame.display.update() # drawn on back buffer (double buffer technique)
    fpsClock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()