
import pygame, os, sys
from pygame.locals import *

class Ball:
    def __init__(self, x, y, speed, imgPath):
        self.initX, self.initY, self.initSpeed = x, y, speed
        self.x, self.y, self.speed = x, y, speed
        self.img = pygame.image.load(imgPath)
        self.rect = self.img.get_rect()
        self.served = False

    def hasHitBrick(self, bricks):
        return self.img.get_rect().collidelist(bricks)

    def hasHitBat(self, bat):
        return self.rect.colliderect(bat)

    def draw(self, surface): 
        surface.blit(self.img, (self.x, self. y))
    
    def update(self, gameTime, bat, playerY):
        if not self.served:
            return

        sx = self.speed[0]
        sy = self.speed[1]

        if self.hasHitBat(bat):
            self.y = playerY - 8
            sy *= -1

        if (self.y <= 0): 
            self.y = 0
            sy *= -1
        if (self.x <= 0):
            self.x = 0
            sx *= -1
        if (self.x >=800 - 8):
            self.x = 800 - 8 
            sx *= -1
        # Bottom screen
        if (self.y >= 600 - 8):
            self.served = False
            self.x, self.y = self.initX, self.initY
            (sx, sy)= self.initSpeed

        self.speed = (sx, sy)
        self.x += sx 
        self.y += sy
        self.rect.topleft = (self.x, self.y)
