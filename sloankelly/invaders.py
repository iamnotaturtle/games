import pygame, os, sys
from pygame.locals import *

# Game States
class GameState:
    def __init__(self, game):
        self.game = game
    
    def onEnter(self, previousState):
        pass

    def onExit(self):
        pass

    def update(self, gameTime):
        pass

    def draw(self, surface):
        pass

class InterstitialState(GameState):
    def __init__(self, game, msg, waitTimeMs, nextState):
        super().__init__(game)
        self.nextState = nextState
        self.font = BitmapFont('./resources/projects/Invaders/bitmap12x12.png', 12, 12)
        self.waitTimer = waitTimeMs
    
    def update(self, gameTime):
        self.waitTimer -= gameTime
        if self.waitTimer < 0:
            self.game.changeState(self.nextState)
    
    def draw(self, surface):
        self.font.centre(surface, self.message, surface.get_rect().height / 2)

class MainMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.playGameState = None
        self.font = BitmapFont('./resources/projects/Invaders/bitmap12x12.png', 12, 12)
        self.index = 0
        self.inputTick = 0
        self.menuItems = ['Start Game', 'Quit']
    
    def setPlayState(self, state):
        self.playGameState = state
    
    def update(self, gameTime):
        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_DOWN] and self.inputTick == 0:
            self.inputTick = 250
            n = len(self.menuItems)
            if keys[K_UP]:
                self.index = self.index - 1 if self.index > 0 else n - 1
            elif keys[K_DOWN]:
                self.index = self.index + 1 if self.index < n else 0
        elif self.inputTick > 0:
            self.inputTick -= gameTime
        if self.inputTick < 0:
            self.inputTick == 0
        
        if keys[K_SPACE]:
            if self.index == 1:
                self.game.changeState(None) # exit game
            elif self.index == 0:
                self.game.changeState(self.playGameState)

    def draw(self, surface):
        self.font.centre(surface, 'Invaders! From Space!', 48)
        count = 0
        y = surface.get_rect().height - len(self.menuItems) * 160
        for item in self.menuItems:
            itemText = " "
            if count == self.index:
                itemText = "> "
            itemText += item
            self.font.draw(surface, itemText, 25, y)
            y += 24
            count += 1

class Game:
    def __init__(self, gameName, width, height):
        pygame.init()
        pygame.display.set_caption(gameName)

        self.fpsClock = pygame.time.Clock()
        self.mainwindow = pygame.display.set_mode((width, height))
        self.background = pygame.Color(0, 0, 0)
        self.currentState = None
    
    def changeState(self, newState):
        if self.currentState != None:
            self.currentState.onExit()
        
        if not newState:
            pygame.quit()
            sys.exit()
        
        oldState = self.currentState
        self.currentState = newState
        newState.onEnter(oldState)
    
    def run(self, initialState):
        self.changeState(initialState)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT: 
                    pygame.quit()
                    sys.exit()
            gameTime = self.fpsClock.get_time()

            if self.currentState:
                self.currentState.update(gameTime)
            
            self.mainwindow.fill(self.background)

            if self.currentState:
                self.currentState.draw(self.mainwindow)
            
            pygame.display.update()
            self.fpsClock.tick(30)

class BitmapFont:
    def __init__(self, fontFile, width, height):
        self.image, self.cellWidth, self.cellHeight = pygame.image.load(fontFile), width, height

        width = self.image.get_rect().width
        height = self.image.get_rect().height
        self.cols = width / self.cellWidth
        self.rows = height / self.cellHeight

    def draw(self, surface, msg, x, y):
        for c in msg:
            ch = self.toIndex(c)
            ox = (ch % self.cols) * self.cellWidth
            oy = (ch / self.cols) * self.cellHeight

            # Calculate x/y offsets for bitmap
            cw = self.cellWidth
            ch = self.cellHeight
            sourceRect = (ox, oy, cw, ch)
            surface.blit(self.image, (x, y, cw, ch), sourceRect)
            x += self.cellWidth
    
    def centre(self, surface, msg, y):
        width = len(msg) * self.cellWidth
        halfWidth = surface.get_rect().width
        x = (halfWidth / width) / 2
        self.draw(surface, msg, x, y)

    def toIndex(self, char):
        return ord(char) - ord(' ')

# Bullet
class BulletModel:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def update(self, delta):
        self.y += delta

class BulletController:
    def __init__(self, speed):
        self.speed = speed
        self.countdown = 0
        self.bullets = []
    
    def clear(self):
        self.bullets[:] = []
    
    def canFire(self):
        return self.countdown == 0 and len(self.bullets) < 3
    
    def addbullet(self, x, y):
        self.bullets.append(BulletModel(x, y))
        self.countdown = 1000
    
    def removeBullet(self, bullet):
        self.bullets.remove(bullet)

    def update(self, gameTime):
        killList = []

        self.countdown = self.countdown - gameTime if self.countdown > 0 else 0

        for b in self.bullets:
            b.update(self.speed * (gameTime / 1000.0))
            if b.y < 0:
                killList.append(b)
        
        for b in killList:
            self.removeBullet(b)

class BulletView:
    def __init__(self, bulletController, imgPath):
        self.bulletController, self.image = bulletController, pygame.image.load(imgPath)
    
    def render(self, surface):
        for b in self.bulletController.bullets:
            surface.blit(self.image, (b.x, b.y, 8, 8))

# Player
class PlayerModel:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.lives = 3
        self.score = 0
        self.speed = 100 # pixels / sec

class PlayerController:
    def __init__(self, x, y):
        self.model = PlayerModel(x, y)
        self.isPaused = False
        self.bullets = BulletController(-200) # pixels / sec
        self.shootSound = pygame.mixer.Sound('./resources/projects/Invaders/playershoot.wav')
    
    def pause(self, isPaused):
        self.isPaused = isPaused
    
    def update(self, gameTime):
        self.bullets.update(gameTime)

        if self.isPaused:
            return
        
        keys = pygame.key.get_pressed()

        # Position is percentage of movement speed based on gametime
        if keys[K_RIGHT] and self.model.x < 800 - 32:
            self.model.x += (gameTime / 1000.0) * self.model.speed
        elif keys[K_LEFT] and self.model.x > 0:
            self.model.x -= (gameTime / 1000.0) * self.model.speed
        
        if keys[K_SPACE] and self.bullets.canFire():
            x = self.model.x + 9 # bullet is 8 pixels
            y = self.model.y - 16
            self.bullets.addbullet(x, y)
            self.shootSound.play()
    
    def hit(self, x, y, width, height):
        return (
            x >= self.model.x and 
            y >= self.model.y and 
            x + width <= self.model.x + 32 and 
            y + height <= self.model.y + 32
        )

class PlayerView:
    def __init__(self, player, imgPath):
        self.player, self.image = player, pygame.image.load(imgPath)
    
    def render(self, surface):
        surface.blit(self.image, (self.player.model.x, self.player.model.y, 32, 32))

class PlayerLivesView:
    def __init__(self, player, imgPath):
        self.player, self.image = player, pygame.image.load(imgPath)
        self.font = BitmapFont('./resources/projects/invaders/bitmap12x12.png', 12, 12)
    
    def render(self, surface):
        x = 8

        for life in range(0, self.player.model.lives):
            surface.blit(self.image, (x, 8, 32, 32))
            x += 40
        
        self.font.draw(surface, f"1UP Score: {self.player.model.score}", 160, 12)