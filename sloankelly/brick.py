import pygame, os, sys
from pygame.locals import *

def init():
    pygame.init()
    fpsClock = pygame.time.Clock()
    mainSurface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("It's brick outside")

    pygame.mixer.init()
    pygame.mixer.music.load('./resources/music.mp3')

    black = pygame.Color(0, 0, 0)

    playerY = 540

    bat = pygame.image.load('./resources/udf/bat.png')
    batRect = bat.get_rect()
    batRect.y = playerY

    ball = pygame.image.load('./resources/udf/ball.png')
    ballRect = ball.get_rect()
    ballStartY, ballSpeed, ballServed = 200, 6, False
    bX, bY = 24, ballStartY
    sX, sY = ballSpeed, ballSpeed
    ballRect.topleft = (bX, bY)

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
        batRect,
        ball,
        ballRect,
        bX,
        bY,
        sX,
        sY,
        ballSpeed,
        ballStartY,
        ballServed,
        brick,
        bricks,
    )

(
    fpsClock,
    mainSurface,
    black,
    playerY,
    bat,
    batRect,
    ball,
    ballRect,
    bX,
    bY,
    sX,
    sY,
    ballSpeed,
    ballStartY,
    ballServed,
    brick,
    bricks,
) = init()

pygame.mixer.music.play(-1)

while True:
    if bY <= 0:
        bY = 0
        sY *= -1
    if bY >= 600 - 8:
        ballServed = False
        bX, bY = (24, ballStartY)
        sX, sY = (ballSpeed, ballSpeed)
        ballRect.topleft = (bX, bY)
    if bX <= 0:
        bX = 0
        sX *= -1
    if bX >= 800 - 8:
        bX = 800 - 8
        sX *= -1
    if ballRect.colliderect(batRect):
        bY = playerY - 8
        sY *= -1
    
    brickHitIndex = ballRect.collidelist(bricks)
    if brickHitIndex >= 0:
        hb = bricks[brickHitIndex]

        mX = bX + 4
        mY = bY + 4
        if mX > hb.x + hb.width or mX < hb.x:
            sX *= -1
        else:
            sY *= -1

        del bricks[brickHitIndex]

    if ballServed:
        bX += sX
        bY += sY
        ballRect.topleft = (bX, bY)

    mainSurface.fill(black)
    mainSurface.blit(bat, batRect)
    mainSurface.blit(ball, ballRect)

    for b in bricks:
        mainSurface.blit(brick, b)

    for event in pygame.event.get():
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP and not ballServed:
            ballServed = True
        elif event.type == MOUSEMOTION:
            mouseX, mouseY = event.pos
            if mouseX < 800 - 55:
                batRect.topleft = (mouseX, playerY)
            else:
                batRect.topleft = (800 - 55, playerY)
    
    pygame.display.update()
    fpsClock.tick(30)
