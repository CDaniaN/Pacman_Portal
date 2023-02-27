import math
import pygame as pg
from ghost import Ghost
from vector import Vector
from timer import Timer

class Blinky(Ghost):
    blinky_images = [pg.transform.rotozoom(pg.image.load(f'images/Blinky{n+3}.png'), 0, 2) for n in range(2)]
    scared_images = [pg.transform.rotozoom(pg.image.load(f'images/Scared{n}.png'), 0, 2) for n in range(2)]
    almost_unscared_images = [pg.transform.rotozoom(pg.image.load(f'images/Scared{n}.png'), 0, 2) for n in range(4)]

    def __init__(self, game):
        super().__init__(game)
        self.timer_normal = Timer(frames=self.blinky_images, wait=200)
        self.timer_scared = Timer(frames=self.scared_images, wait=200)
        self.timer_unscaring = Timer(frames=self.almost_unscared_images, wait=200)
        self.image = self.blinky_images[0]

        self.timer = self.timer_normal

    def draw(self):
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