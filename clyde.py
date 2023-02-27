import math
import pygame as pg
from timer import Timer
from ghost import Ghost
from vector import Vector

class Clyde(Ghost):
    clyde_images = [pg.transform.rotozoom(pg.image.load(f'images/Clyde{n + 3}.png'), 0, 2) for n in range(2)]
    scared_images = [pg.transform.rotozoom(pg.image.load(f'images/Scared{n}.png'), 0, 2) for n in range(2)]
    almost_unscared_images = [pg.transform.rotozoom(pg.image.load(f'images/Scared{n}.png'), 0, 2) for n in range(4)]

    def __init__(self, game):
        super().__init__(game)
        self.timer_normal = Timer(frames=self.clyde_images, wait=200)
        self.timer_scared = Timer(frames=self.scared_images, wait=200)
        self.timer_unscaring = Timer(frames=self.almost_unscared_images, wait=200)
        self.image = self.clyde_images[0]

        self.timer = self.timer_normal

    def scatter(self): self.set_target(self.settings.scatter_clyde)

    def aggro(self):
        currDist = self.calc_dist(self.posn, self.game.pacman.posn)
        if currDist < 16.0: self.scatter()
        else: self.set_target(self.game.pacman.posn)

    # def reset(self):
    #     self.vel = Vector(-1, 0)
    #     self.prevPosn = Vector()
    #     self.posn = self.center_blinky()
    #     self.pxPosn = Vector(self.posn.x * self.settings.block_size, self.posn.y * self.settings.block_size)

    def update(self, ticks):
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
                self.timer = self.timer_normal
        elif self.isScared: self.scared()
        elif self.isScatter: self.scatter()
        else: self.aggro()
        if self.pxPosn.x == (self.posn.x + 0.5) * self.settings.block_size and self.pxPosn.y == (self.posn.y + 0.5) * self.settings.block_size:
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
                self.pxPosn += (self.vel * self.settings.speed_clyde)
        self.posn = Vector(math.floor(self.pxPosn.x / self.settings.block_size),
                           math.floor(self.pxPosn.y / self.settings.block_size))
        if self.posn != self.currPosn:

            self.prevPosn = self.currPosn

        self.currPosn = self.posn
        self.draw()

    def draw(self):  # temporarily using circles until we have images
        if self.isEaten:
            # pg.draw.circle(self.screen, [100, 100, 255],
            #                [self.pxPosn.x, self.pxPosn.y], 14)
            self.rect = pg.Rect(self.pxPosn.x - self.settings.block_size / 2,
                                self.pxPosn.y - self.settings.block_size / 2, 28, 28)
            # print("I GOTTA GO!!!")
        elif self.isScared:
            # pg.draw.circle(self.screen, [100, 100, 255],
            #                [self.pxPosn.x, self.pxPosn.y], 14)
            image = self.timer.imagerect()
            rect = image.get_rect()
            rect.left, rect.top = self.rect.left - 27, self.rect.top - 32
            self.screen.blit(image, rect)
            self.rect = pg.Rect(self.pxPosn.x - self.settings.block_size / 2,
                                self.pxPosn.y - self.settings.block_size / 2, 28, 28)
        else:
            # pg.draw.circle(self.screen, self.settings.color_blinky,
            #                [self.pxPosn.x, self.pxPosn.y], 14)
            self.rect = pg.Rect(self.pxPosn.x - self.settings.block_size / 2,
                                self.pxPosn.y - self.settings.block_size / 2, 28, 28)
            image = self.timer.imagerect()
            rect = image.get_rect()
            rect.left, rect.top = self.rect.left - 27, self.rect.top - 32
            self.screen.blit(image, rect)
        self.drawEyes()