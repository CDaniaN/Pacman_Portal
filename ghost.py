import pygame as pg
import math
import random
from pygame.sprite import Sprite
from settings import Settings
import game_functions as gf
from maze import Maze
from pacman import Pacman
from vector import Vector

eye_left = pg.transform.rotozoom(pg.image.load(f'images/EyesLeft.png'), 0, 1.9)
eye_right = pg.transform.rotozoom(pg.image.load(f'images/EyesRight.png'), 0, 1.9)
eye_up = pg.transform.rotozoom(pg.image.load(f'images/EyesUp.png'), 0, 1.9)
eye_down = pg.transform.rotozoom(pg.image.load(f'images/EyesDown.png'), 0, 1.9)

class Ghost(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.maze = game.maze
        self.image = pg.image.load("images/burst0.png")
        # **replace with timer animation later**
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.prevPosn = Vector()
        self.prevVel = Vector(-1, 0)
        self.currPosn = self.center_blinky()
        self.posn = self.center_blinky()  # posn is the centerx, bottom of the rect, not left, top
        self.pxPosn = Vector(self.posn.x * self.settings.block_size, self.posn.y * self.settings.block_size)
        self.vel = Vector(-1, 0)
        self.target = game.pacman.posn
        self.isScatter = False
        self.isScared = False
        self.isEaten = False
        self.isPacmanDead = False
        self.velocityLocked = 0

    def center_blinky(self):
        return Vector(30, 24)

    # def center_cage(self): return Vector(30, 24)

    def die(self):
        self.isScared = False
        self.isEaten = True
        self.set_target(self.center_blinky())
        # self.reset()

    def chase(self):
        # 0 is UP, 1 is RIGHT, 2 is DOWN, 3 is LEFT
        adj = [self.posn + gf.movement[pg.K_w], self.posn + gf.movement[pg.K_d], self.posn + gf.movement[pg.K_s], self.posn + gf.movement[pg.K_a]]
        countPaths = 0
        isPath = [False, False, False, False]
        pathDist = [None, None, None, None]
        for i in range(4):
            if self.maze.getMaze(adj[i]) != '.' and self.maze.getMaze(adj[i]) != 'X':
                if adj[i] != self.prevPosn:
                    if i == 0:
                        if self.prevVel.x != 0 or self.prevVel.y != 1:
                            countPaths += 1
                            isPath[i] = True
                    elif i == 1:
                        if self.prevVel.x != -1 or self.prevVel.y != 0:
                            countPaths += 1
                            isPath[i] = True
                    elif i == 2:
                        if self.prevVel.x != 0 or self.prevVel.y != -1:
                            countPaths += 1
                            isPath[i] = True
                    else:
                        if self.prevVel.x != 1 or self.prevVel.y != 0:
                            countPaths += 1
                            isPath[i] = True
        if countPaths > 1: #turning point
            for j in range(4):
                if isPath[j]:
                    pathDist[j] = self.calc_dist(b=self.target, a=adj[j])
            if self.prevVel.x == 0 and self.prevVel.y == -1:
                pathDist[2] = None
            elif self.prevVel.x == 1 and self.prevVel.y == 0:
                pathDist[3] = None
            elif self.prevVel.x == 0 and self.prevVel.y == 1:
                pathDist[0] = None
            else:
                pathDist[1] = None
            leastIndex = pathDist.index(min(k for k in pathDist if k is not None))
            if leastIndex == 0:
                self.pxPosn += Vector(0, -11)
                # self.posn += Vector(0, -1)
                return Vector(0, -1)
            elif leastIndex == 1:
                self.pxPosn += Vector(11, 0)
                # self.posn += Vector(1, 0)
                return Vector(1, 0)
            elif leastIndex == 2:
                self.pxPosn += Vector(0, 11)
                # self.posn += Vector(0, 1)
                return Vector(0, 1)
            else:
                self.pxPosn += Vector(-11, 0)
                # self.posn += Vector(-1, 0)
                return Vector(-1, 0)
        elif countPaths == 0:
            self.reset()
            return Vector(-1, 0)
        else:
            if gf.checkWall(self.maze, self.posn, self.vel):
                self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                     (self.posn.y + 0.5) * self.settings.block_size)
                if self.prevVel.x == 0 and self.prevVel.y == -1:
                    isPath[2] = False
                elif self.prevVel.x == 1 and self.prevVel.y == 0:
                    isPath[3] = False
                elif self.prevVel.x == 0 and self.prevVel.y == 1:
                    isPath[0] = False
                else:
                    isPath[1] = False
                pathIndex = isPath.index(True)
                if pathIndex == 0:
                    self.pxPosn += Vector(0, -11)
                    # self.posn += Vector(0, -1)
                    return Vector(0, -1)
                elif pathIndex == 1:
                    self.pxPosn += Vector(11, 0)
                    # self.posn += Vector(1, 0)
                    return Vector(1, 0)
                elif pathIndex == 2:
                    self.pxPosn += Vector(0, 11)
                    # self.posn += Vector(0, 1)
                    return Vector(0, 1)
                else:
                    self.pxPosn += Vector(-11, 0)
                    # self.posn += Vector(-1, 0)
                    return Vector(-1, 0)
            else:
                return self.vel

    def calc_dist(self, a, b):
        return math.dist([a.x, a.y], [b.x, b.y])

    def scatter(self): self.set_target(self.settings.scatter_blinky)

    def aggro(self): self.set_target(self.game.pacman.posn) # TARGET DEPENDS ON GHOST, THIS IS BLINKY'S TARGET

    def scared(self):
    #     # 0 is UP, 1 is RIGHT, 2 is DOWN, 3 is LEFT
    #     adj = [self.posn + gf.movement[pg.K_w], self.posn + gf.movement[pg.K_d], self.posn + gf.movement[pg.K_s],
    #            self.posn + gf.movement[pg.K_a]]
    #     countPaths = 0
    #     isPath = [False, False, False, False]
    #     for i in range(4):
    #         if self.maze.getMaze(adj[i]) != '.' and self.maze.getMaze(adj[i]) != 'X':
    #             if adj[i] != self.prevPosn:
    #                 countPaths += 1
    #                 isPath[i] = True
    #     if countPaths > 1:  # turning point
    #         isValidPath = False
    #         randPath = 0
    #         while isValidPath == False:
    #             randPath = random.randint(0, 3)
    #             isValidPath = isPath[randPath]
    #         self.velocityLocked = self.game.elapsed
    #         if randPath == 0:
    #             # self.pxPosn += Vector(0, -11)
    #             return Vector(0, -1)
    #         elif randPath == 1:
    #             # self.pxPosn += Vector(11, 0)
    #             return Vector(1, 0)
    #         elif randPath == 2:
    #             # self.pxPosn += Vector(0, 11)
    #             return Vector(0, 1)
    #         else:
    #             # self.pxPosn += Vector(-11, 0)
    #             return Vector(-1, 0)
    #     elif countPaths == 0:
    #         self.reset()
    #         return Vector(-1, 0)
    #     else:
    #         if gf.checkWall(self.maze, self.posn, self.vel):
    #             self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
    #                                  (self.posn.y + 0.5) * self.settings.block_size)
    #             pathIndex = isPath.index(True)
    #             if pathIndex == 0:
    #                 self.pxPosn += Vector(0, -10)
    #                 return Vector(0, -1)
    #             elif pathIndex == 1:
    #                 self.pxPosn += Vector(10, 0)
    #                 return Vector(1, 0)
    #             elif pathIndex == 2:
    #                 self.pxPosn += Vector(0, 10)
    #                 return Vector(0, 1)
    #             else:
    #                 self.pxPosn += Vector(-10, 0)
    #                 return Vector(-1, 0)
    #         else:
    #             return self.vel
        diffX = self.game.pacman.posn.x - self.posn.x
        diffY = self.game.pacman.posn.y - self.posn.y
        self.set_target((self.posn) - Vector(diffX, diffY))

    def set_target(self, target): self.target = target

    def reset(self):
        self.vel = Vector(-1, 0)
        self.prevPosn = Vector()
        self.posn = self.center_blinky() # CHANGE THIS DEPENDING ON GHOST (blinky can keep default)
        self.pxPosn = Vector(self.posn.x * self.settings.block_size, self.posn.y * self.settings.block_size)
        self.isScared = False
        self.isEaten = False
        self.game.inky.sound.ghost_stop_scare()
        self.game.inky.sound.ghost_chase()

    def checkPortal(self):
        if self.game.maze.getMaze(self.posn) == 's':
            self.posn = Vector(1, 30)
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                 (self.posn.y + 0.5) * self.settings.block_size)
        elif self.game.maze.getMaze(self.posn) == 'S':
            self.posn = Vector(59, 30)
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                 (self.posn.y + 0.5) * self.settings.block_size)

    def update(self, ticks):
        # print(self.isScared)
        self.checkPortal()
        if ticks % 15000 <= 10000:
            self.isScatter = False
            # print('in scatter mode')
        elif ticks % 15000 > 10000:
            self.isScatter = True
            # print('out of scatter mode')
        if self.isPacmanDead: self.vel = Vector()
        elif self.isEaten:
            # pass
            if self.posn.x == self.center_blinky().x and self.posn.y == self.center_blinky().y:
                self.isEaten = False
                self.isScared = False
                self.game.inky.sound.ghost_stop_scare()
                self.game.inky.sound.ghost_chase()
                self.game.blinky.timer = self.game.blinky.timer_normal
        elif self.isScared: self.scared()
        elif self.isScatter: self.scatter()
        else: self.aggro()
        if self.pxPosn.x == (self.posn.x + 0.5) * self.settings.block_size and self.pxPosn.y == (
                self.posn.y + 0.5) * self.settings.block_size:
            self.prevVel = self.vel
        if not self.isPacmanDead: self.vel = self.chase()
        # if gf.checkWall(self.game.maze, self.posn, self.vel):
        #     self.vel = Vector()
        #     self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size, (self.posn.y + 0.5) * self.settings.block_size)
        if self.vel.x == 0:
            self.pxPosn.x = (self.posn.x + 0.5) * self.settings.block_size
        elif self.vel.y == 0:
            self.pxPosn.y = (self.posn.y + 0.5) * self.settings.block_size
        if ticks % 24 == 0:
            if self.isEaten:
                self.pxPosn += (self.vel * self.settings.speed_eaten)
            elif self.isScared:
                self.pxPosn += (self.vel * self.settings.speed_scared)
            else:
                self.pxPosn += (self.vel * self.settings.speed_blinky)  # CHANGE THIS TO GHOST'S SPEED
        self.posn = Vector(math.floor(self.pxPosn.x / self.settings.block_size),
                           math.floor(self.pxPosn.y / self.settings.block_size))
        if self.posn != self.currPosn:
            self.prevPosn = self.currPosn

        self.currPosn = self.posn
        self.draw()

    def draw(self): #temporarily using circles until we have images
        if self.isEaten:
            pass
            # print("I GOTTA GO!!!")
        elif self.isScared:
            pg.draw.circle(self.screen, [100, 100, 255],
                           [self.pxPosn.x, self.pxPosn.y], 14)
            self.rect = pg.Rect(self.pxPosn.x - self.settings.block_size / 2,
                                self.pxPosn.y - self.settings.block_size / 2, 28, 28)
        else:
            pg.draw.circle(self.screen, self.settings.color_blinky,
                           [self.pxPosn.x, self.pxPosn.y], 14)
            self.rect = pg.Rect(self.pxPosn.x - self.settings.block_size / 2, self.pxPosn.y - self.settings.block_size / 2, 28, 28)

    def drawEyes(self):
        if self.isScared and not self.isEaten:
            pass #scared ghosts already have eyes, so keep this as a pass
        else:
            if self.vel.x == -1 and self.vel.y == 0:
                image = eye_left
                rect = image.get_rect()
                rect.left, rect.top = self.rect.left - 27, self.rect.top - 28
                self.screen.blit(image, rect)
            elif self.vel.x == 1 and self.vel.y == 0:
                image = eye_right
                rect = image.get_rect()
                rect.left, rect.top = self.rect.left - 24, self.rect.top - 28
                self.screen.blit(image, rect)
            elif self.vel.x == 0 and self.vel.y == -1:
                image = eye_up
                rect = image.get_rect()
                rect.left, rect.top = self.rect.left - 25.2, self.rect.top - 31
                self.screen.blit(image, rect)
            else:
                image = eye_down
                rect = image.get_rect()
                rect.left, rect.top = self.rect.left - 25.2, self.rect.top - 30
                self.screen.blit(image, rect)