import pygame, os, sys
from pygame.locals import *
from invaders import *

def testPlayer():
    pygame.init()
    fpsClock = pygame.time.Clock()
    surface = pygame.display.set_mode((800, 600)) 
    pygame.display.set_caption('Player Test') 
    black = pygame.Color(0, 0, 0)
    player = PlayerController(0, 200)
    playerView = PlayerView(player, './resources/projects/Invaders/ship.png') 
    playerLivesView = PlayerLivesView(player, './resources/projects/Invaders/ship.png')

    while True:
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit() 
                sys.exit()
        player.update(fpsClock.get_time())
        
        surface.fill(black) 
        playerView.render(surface) 
        playerLivesView.render(surface)

        pygame.display.update() 
        fpsClock.tick(30)


# Pass in class to test
testClass = sys.argv[1] if len(sys.argv) > 1 else None
if not testClass:
    raise Error('Must pass in class to test')
elif testClass == 'player':
    testPlayer()