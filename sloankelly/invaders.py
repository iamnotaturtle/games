import pygame
import os
import sys
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
        self.message, self.waitTimer, self.nextState = msg, waitTimeMs, nextState
        self.font = BitmapFont(
            './resources/projects/Invaders/bitmap12x12.png', 12, 12)

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
        self.font = BitmapFont(
            './resources/projects/Invaders/bitmap12x12.png', 12, 12)
        self.index = 0
        self.inputTick = 0
        self.menuItems = ['Start Game', 'Quit']

    def setPlayState(self, state):
        self.playGameState = state

    def update(self, gameTime):
        keys = pygame.key.get_pressed()
        if ((keys[K_UP] or keys[K_DOWN]) and self.inputTick == 0):
            self.inputTick = 250
            if (keys[K_UP]):
                self.index -= 1
                if (self.index < 0):
                    self.index = len(self.menuItems) - 1
            elif (keys[K_DOWN]):
                self.index += 1
                if (self.index == len(self.menuItems)):
                    self.index = 0
        elif (self.inputTick > 0):
            self.inputTick -= gameTime

        if (self.inputTick < 0):
            self.inputTick = 0

        if keys[K_SPACE]:
            if (self.index == 1):
                self.game.changeState(None)  # exit the game
            elif (self.index == 0):
                self.game.changeState(self.playGameState)
        
        if keys[K_ESCAPE]:
            self.game.changeState(None) # exit the game

    def draw(self, surface):

        self.font.centre(surface, "Invaders! From Space!", 48)

        count = 0
        y = surface.get_rect().height - len(self.menuItems) * 160
        for item in self.menuItems:
            itemText = "  "

            if (count == self.index):
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
        self.image = pygame.image.load(fontFile)
        self.cellWidth = width
        self.cellHeight = height
        width = self.image.get_rect().width
        height = self.image.get_rect().height
        self.cols = width / self.cellWidth
        self.rows = height / self.cellHeight

    def draw(self, surface, msg, x, y):
        for c in msg:
            ch = self.toIndex(c)
            ox = (ch % self.cols) * self.cellWidth
            oy = (ch / self.cols) * self.cellHeight
            cw = self.cellWidth
            ch = self.cellHeight
            sourceRect = (ox, oy, cw, ch)
            surface.blit(self.image, (x, y, cw, ch), sourceRect)
            x += self.cellWidth

    def centre(self, surface, msg, y):
        width = len(msg) * self.cellWidth
        halfWidth = surface.get_rect().width
        x = (halfWidth - width) / 2
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

    def addBullet(self, x, y):
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
        self.bulletController, self.image = bulletController, pygame.image.load(
            imgPath)

    def render(self, surface):
        for b in self.bulletController.bullets:
            surface.blit(self.image, (b.x, b.y, 8, 8))

# Player


class PlayerModel:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.lives = 3
        self.score = 0
        self.speed = 100  # pixels / sec


class PlayerController:
    def __init__(self, x, y):
        self.model = PlayerModel(x, y)
        self.isPaused = False
        self.bullets = BulletController(-200)  # pixels / sec
        self.shootSound = pygame.mixer.Sound(
            './resources/projects/Invaders/playershoot.wav')

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
            x = self.model.x + 9  # bullet is 8 pixels
            y = self.model.y - 16
            self.bullets.addBullet(x, y)
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
        surface.blit(self.image, (self.player.model.x,
                     self.player.model.y, 32, 32))


class PlayerLivesView:
    def __init__(self, player, imgPath):
        self.player, self.image = player, pygame.image.load(imgPath)
        self.font = BitmapFont(
            './resources/projects/invaders/bitmap12x12.png', 12, 12)

    def render(self, surface):
        x = 8

        for life in range(0, self.player.model.lives):
            surface.blit(self.image, (x, 8, 32, 32))
            x += 40

        self.font.draw(
            surface, f"1UP Score: {self.player.model.score}", 160, 12)

# Alien


class InvaderModel:
    def __init__(self, x, y, alienType):
        self.x, self.y, self.alientype = x, y, alienType
        self.animFrame = 0

    def flipFrame(self):
        self.animFrame = 1 if self.animFrame == 0 else 0

    def hit(self, x, y, width, height):
        return (
            x >= self.x and
            y > self.y and
            x + width <= self.x + 32 and
            y + height <= self.y + 32
        )


class SwarmController:

    def __init__(self, scrwidth, offsety, initialframeticks):

        self.currentframecount = initialframeticks
        self.framecount = initialframeticks
        self.invaders = []
        self.sx = -8
        self.movedown = False
        self.alienslanded = False
        self.bullets = BulletController(200)  # pixels per sec
        self.alienShooter = 3  # each 3rd alien (to start with) fires
        self.bulletDropTime = 2500
        # each bullet is fired in this ms interval
        self.shootTimer = self.bulletDropTime
        self.currentShooter = 0  # current shooting alien

        for y in range(7):
            for x in range(10):
                invader = InvaderModel(
                    160 + (x * 48) + 8, (y * 32) + offsety, y % 2)
                self.invaders.append(invader)

    def reset(self, offsety, ticks):
        self.currentframecount = ticks
        self.framecount = ticks

        for y in range(7):
            for x in range(10):
                invader = InvaderModel(
                    160 + (x * 48) + 8, (y * 32) + offsety, y % 2)
                self.invaders.append(invader)

    def update(self, gameTime):

        self.bullets.update(gameTime)
        self.framecount -= gameTime
        movesideways = True

        if self.framecount < 0:
            if self.movedown:
                self.movedown = False
                movesideways = False
                self.sx *= -1
                self.bulletDropTime -= 250
                if (self.bulletDropTime < 1000):
                    self.bulletDropTime = 1000
                self.currentframecount -= 100
                if self.currentframecount < 200:  # clamp the speed of the aliens to 200ms
                    self.currentframecount = 200

                for i in self.invaders:
                    i.y += 32

            self.framecount = self.currentframecount + self.framecount
            for i in self.invaders:
                i.flipFrame()

            if movesideways:
                for i in self.invaders:
                    i.x += self.sx

            x, y, width, height = self.getarea()

            if (x <= 0 and self.sx < 0) or (x + width >= 800 and self.sx > 0):
                self.movedown = True

        self.shootTimer -= gameTime
        if (self.shootTimer <= 0):
            self.shootTimer += self.bulletDropTime  # reset the timer
            self.currentShooter += self.alienShooter

            self.currentShooter = self.currentShooter % len(self.invaders)

            shooter = self.invaders[self.currentShooter]
            x = shooter.x + 9  # bullet is 8 pixels
            y = shooter.y + 16
            self.bullets.addBullet(x, y)

    def getarea(self):
        leftmost = 2000
        rightmost = -2000
        topmost = -2000
        bottommost = 2000

        for i in self.invaders:
            if i.x < leftmost:
                leftmost = i.x

            if i.x > rightmost:
                rightmost = i.x

            if i.y < bottommost:
                bottommost = i.y

            if i.y > topmost:
                topmost = i.y

        width = (rightmost - leftmost) + 32
        height = (topmost - bottommost) + 32

        return (leftmost, bottommost, width, height)


class InvaderView:
    def __init__(self, swarm, imgPath):
        self.image = pygame.image.load(imgPath)
        self.swarm = swarm

    def render(self, surface):
        for i in self.swarm.invaders:
            surface.blit(self.image, (i.x, i.y, 32, 32),
                         (i.animFrame * 32, 32 * i.alientype, 32, 32))

# Collision Detection


class ExplosionModel:
    def __init__(self, x, y, maxFrames, speed, nextState=None):
        self.x, self.y, self.maxFrames, self.speed, self.nextState = x, y, maxFrames, speed, nextState
        self.initialSpeed = speed
        self.frame = 0


class ExplosionModelList:
    def __init__(self, game):
        self.explosions = []
        self.game = game

    def add(self, explosion, nextState=None):
        x, y, frames, speed = explosion
        exp = ExplosionModel(x, y, frames, speed, nextState)
        self.explosions.append(exp)

    def cleanup(self):
        killList = []
        for e in self.explosions:
            if e.frame == e.maxFrames:
                killList.append(e)
        nextState = None
        for e in killList:
            if not nextState and e.nextState:
                nextState = e.nextState
            self.explosions.remove(e)

        if nextState:
            self.game.changeState(nextState)


class ExplosionView:
    def __init__(self, explosions, explosionImg, width, height):
        self.image = pygame.image.load(explosionImg)
        self.image.set_colorkey((255, 0, 255))
        self.explosions = explosions
        self.width = width
        self.height = height

    def render(self, surface):
        for e in self.explosions:
            surface.blit(self.image, (e.x, e.y, self.width, self.height),
                         (e.frame * self.width, 0, self.width, self.height))


class ExplosionController:
    def __init__(self, game):
        self.list = ExplosionModelList(game)

    def update(self, gameTime):
        for e in self.list.explosions:
            e.speed -= gameTime
            if e.speed < 0:
                e.speed += e.initialSpeed
                e.frame += 1
        self.list.cleanup()


class CollisionController:
    def __init__(self, game, swarm, player, explosionController, playState):
        self.swarm, self.player, self.game, self.playGameState = swarm, player, game, playState
        self.BulletController = player.bullets
        self.EnemyBullets = swarm.bullets
        self.expCtrl = explosionController
        self.playGameState = playState
        self.alienDeadSound = pygame.mixer.Sound(
            './resources/projects/Invaders/aliendie.wav')
        self.playerDieSound = pygame.mixer.Sound(
            './resources/projects/Invaders/playerdie.wav')

    def update(self, gameTime):

        aliens = []
        bullets = []

        for b in self.BulletController.bullets:

            if (bullets.count(b) > 0):
                continue

            for inv in self.swarm.invaders:
                if (inv.hit(b.x+3, b.y+3, 8, 12)):
                    aliens.append(inv)
                    bullets.append(b)
                    break

        for b in bullets:
            self.BulletController.removeBullet(b)

        for inv in aliens:
            self.swarm.invaders.remove(inv)
            self.player.model.score += (10 * (inv.alientype + 1))
            self.expCtrl.list.add((inv.x, inv.y, 6, 50))
            self.alienDeadSound.play()

        playerHit = False

        for b in self.EnemyBullets.bullets:
            if (self.player.hit(b.x+3, b.y+3, 8, 12)):
                self.player.model.lives -= 1
                playerHit = True
                break

        if (playerHit):
            self.EnemyBullets.clear()
            self.player.bullets.clear()

            if (self.player.model.lives > 0):
                self.player.pause(True)
                getReadyState = InterstitialState(
                    self.game, 'Get Ready!', 2000, self.playGameState)
                self.expCtrl.list.add(
                    (self.player.model.x, self.player.model.y, 6, 50), getReadyState)

            self.playerDieSound.play()

# Main game state


class PlayGameState(GameState):
    def __init__(self, game, gameOverState):
        super().__init__(game)
        self.controllers = None
        self.renderers = None
        self.playerController = None
        self.swarmController = None
        self.swarmSpeed = 500
        self.gameOverState = gameOverState
        self.initialize()

    def onEnter(self, previousState):
        self.playerController.pause(False)

    def initialize(self):
        self.swarmController = SwarmController(800, 48, self.swarmSpeed)
        swarmRenderer = InvaderView(
            self.swarmController, './resources/projects/Invaders/invaders.png')
        self.playerController = PlayerController(0, 540)
        playerRenderer = PlayerView(
            self.playerController, './resources/projects/Invaders/ship.png')
        livesRenderer = PlayerLivesView(
            self.playerController, './resources/projects/Invaders/ship.png')
        bulletRenderer = BulletView(
            self.playerController.bullets, './resources/projects/Invaders/bullet.png')
        alienbulletRenderer = BulletView(
            self.swarmController.bullets, './resources/projects/Invaders/alienbullet.png')
        explosionController = ExplosionController(self.game)
        collisionController = CollisionController(
            self.game, self.swarmController, self.playerController, explosionController, self)
        explosionView = ExplosionView(
            explosionController.list.explosions, './resources/projects/Invaders/explosion.png', 32, 32)

        self.renderers = [
            alienbulletRenderer,
            swarmRenderer,
            bulletRenderer,
            playerRenderer,
            livesRenderer,
            explosionView,
        ]

        self.controllers = [
            self.swarmController,
            self.playerController,
            collisionController,
            explosionController,
        ]

    def update(self, gameTime):
        for ctrl in self.controllers:
            ctrl.update(gameTime)

            if self.playerController.model.lives == 0:
                self.game.changeState(self.gameOverState)

            if len(self.swarmController.invaders) == 0:
                self.swarmSpeed -= 50
                if self.swarmSpeed < 100:
                    self.swarmSpeed = 100

                self.swarmController.reset(48, self.swarmSpeed)
                levelUpMessage = InterstitialState(
                    invadersGame, 'Congratulations! Level Up!', 2000, self)
                self.game.changeState(levelUpMessage)

    def draw(self, surface):
        for view in self.renderers:
            view.render(surface)


# Main program
invadersGame = Game('Invaders', 800, 600)
mainMenuState = MainMenuState(invadersGame)
gameOverState = InterstitialState(
    invadersGame, 'G A M E  O V E R !', 5000, mainMenuState)
playGameState = PlayGameState(invadersGame, gameOverState)
getReadyState = InterstitialState(
    invadersGame, 'Get Ready!', 2000, playGameState)
mainMenuState.setPlayState(getReadyState)

invadersGame.run(mainMenuState)
