import pygame, os, sys
from pygame.locals import *
from classes import Ball, Bat

def init():
    pygame.init()
    fpsClock = pygame.time.Clock()
    mainSurface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("It's brick outside")

    pygame.mixer.init()
    pygame.mixer.music.load('./resources/music.mp3')

    black = pygame.Color(0, 0, 0)
    playerY = 540

    bat = Bat(0, playerY, './resources/udf/bat.png')
    ball = Ball(24, 200, [6, 6], './resources/udf/ball.png')

    brick = pygame.image.load('./resources/udf/brick.png')
    bricks = []
    for y in range(5):
        brickY = (y * 24) + 100
        for x in range(10):
            brickX = (x * 31) + 245
            width = brick.get_width()
            height = brick.get_height()
            rect = Rect(brickX, brickY, width, height)
            bricks.append(rect)

    return (
        fpsClock,
        mainSurface,
        black,
        playerY,
        bat,
        ball,
        brick,
        bricks,
    )

(
    fpsClock,
    mainSurface,
    black,
    playerY,
    bat,
    ball,
    brick,
    bricks,
) = init()

pygame.mixer.music.play(-1)

while True:    
    brickHitIndex = ball.hasHitBrick(bricks)
    if brickHitIndex >= 0:
        hb = bricks[brickHitIndex]
        mX = ball.x + 4
        mY = ball.y + 4
        if mX > hb.x + hb.width or mX < hb.x:
            ball.speed[0] *= -1
        else:
            ball.speed[1] *= -1
        del bricks[brickHitIndex]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.mixer.quit()
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP and not ball.served:
            ball.served = True
        elif event.type == MOUSEMOTION:
            mouseX, mouseY = event.pos
            if mouseX < 800 - 55:
                bat.update(mouseX, playerY)
            else:
                bat.update(800 - 55, playerY)

    ball.update(bat.rect, playerY)

    mainSurface.fill(black)
    for b in bricks:
        mainSurface.blit(brick, b)
    ball.draw(mainSurface)
    bat.draw(mainSurface)


    pygame.display.update()
    fpsClock.tick(30)
