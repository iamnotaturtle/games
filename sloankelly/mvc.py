import pygame, sys, random
from pygame.locals import *

class RadarView:
    def __init__(self, blipImagePath, borderImagePath):
        self.blipImage = pygame.image.load(blipImagePath)
        self.borderImage = pygame.image.load(borderImagePath)
    def draw(self, surface, robots):
        surface.blit(self.borderImage, (0, 0))
        for robot in robots:
            x, y = robot.getPosition()
            x /= 10
            y /= 10
            x += 1
            y += 1

            surface.blit(self.blipImage, (x, y))
class RobotController:
    def __init__(self, robots):
        self.robots = robots
    def update(self, deltaTime):
        for robot in self.robots:
            robot.timer += deltaTime
            if robot.getTimer() >= 0.125:
                robot.nextFrame()

            speed = self.multiply(robot.getSpeed(), deltaTime)
            pos = robot.getPosition()
            x, y = self.add(pos, speed)
            sx, sy = robot.getSpeed()

            if x < 0:
                x = 0
                sx *= -1
            elif x > 607:
                x = 607
                sx *= -1

            if y < 0:
                y = 0
                sy *= -1
            elif y > 447:
                y = 447
                sy *= -1
            
            robot.setPosition((x, y))
            robot.setSpeed((sx, sy))
    def multiply(self, speed, deltaTime):
        x = speed[0] * deltaTime
        y = speed[1] * deltaTime
        return (x, y)
    def add(self, position, speed):
        x = position[0] + speed[0]
        y = position[1] + speed[1]
        return (x, y)
class RobotGenerator:
    def __init__(self, generationTime = 1, maxRobots = 10):
        self.generationTime, self.maxRobots = generationTime, maxRobots
        self.robots = []
        self.counter = 0
    def getRobots(self):
        return self.robots
    def update(self, deltaTime):
        self.counter += deltaTime
        if self.counter >= self.generationTime and len(self.robots) < self.maxRobots:
            self.counter = 0
            x = random.randint(36, 600)
            y = random.randint(36, 440)
            frame = random.randint(0, 1)
            sx = -50 + random.random() * 100 
            sy = -50 + random.random() * 100

            newRobot = RobotModel(x, y, frame, (sx, sy))
            self.robots.append(newRobot)
class RobotModel:
    def __init__(self, x, y, frame, speed):
        self.x, self.y, self.frame, self.speed = x, y, frame, speed
        self.timer = 0
    def setPosition(self, newPosition): 
        self.x, self.y = newPosition
    def getPosition(self): 
        return (self.x, self.y)
    def getFrame(self): 
        return self.frame
    def getTimer(self): 
        return self.timer
    def getSpeed(self): 
        return self.speed
    def setSpeed(self, speed): 
        self.speed = speed
    def nextFrame(self):
        self.timer = 0
        self.frame = (self.frame + 1) % 2
class RobotView:
    def __init__(self, imgPath):
        self.img = pygame.image.load(imgPath)
    def draw(self, surface, models):
        for model in models:
            rect = Rect(model.getFrame() * 32, 0, 32, 32)
            surface.blit(self.img, model.getPosition(), rect)

pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((640, 480))

lastMillis = 0

generator = RobotGenerator()
view = RobotView('./resources/mvc/robotframes.png')
radar = RadarView('./resources/mvc/blip.png', './resources/mvc/radar.png')
controller = RobotController(generator.getRobots())

# Game loop
# Check input events -> update logic -> draw
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    deltaTime = lastMillis / 1000

    generator.update(deltaTime)
    controller.update(deltaTime)

    surface.fill((0, 0, 0))

    view.draw(surface, generator.getRobots())
    radar.draw(surface, generator.getRobots())

    # Flip buffer and set frame rate
    pygame.display.update()
    lastMillis = fpsClock.tick(30)
