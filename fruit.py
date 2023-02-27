import pygame as pg
import math
from pygame.sprite import Sprite
from vector import Vector
from timer import Timer

class Fruit(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.maze = game.maze
        self.fruit_cherry = pg.image.load(f'images/Fruit1.png')
        self.rect = self.fruit_cherry.get_rect()
        self.posn = self.center_fruit()
        self.isActive = False
        self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size, (self.posn.y + 0.5) * self.settings.block_size)

    def center_fruit(self):
        return Vector(30, 36)

    def reset(self):
        self.isActive = False

    def check_touch(self):
        if self.game.pacman.posn.x == self.posn.x and self.game.pacman.posn.y == self.posn.y:
            self.sound.fruit_eaten()
            self.game.scoreboard.increment_score(3)
            self.isActive = False

    def update(self):
        if self.isActive:
            self.check_touch()
            self.draw()
 
    def draw(self):
        image_rect = self.fruit_cherry.get_rect()
        image_rect.left += self.center_fruit().x * self.settings.block_size - 9
        image_rect.top += self.center_fruit().y * self.settings.block_size - 9
        self.screen.blit(self.fruit_cherry, image_rect)
        # pg.draw.rect(self.screen, [250, 20, 220],
        #                                  [self.center_fruit().x * self.settings.block_size, self.center_fruit().y * self.settings.block_size,
        #                                   self.settings.block_size, self.settings.block_size])