import pygame as pg
import math
from pygame.sprite import Sprite
from vector import Vector
from portal import Portal
from timer import Timer
import game_functions as gf
from sys import exit


class Pacman(Sprite):
    pacman_images_up = [pg.transform.rotozoom(pg.image.load(f'images/pacman_move{n}.png'), 90, 2) for n in range(4)]
    pacman_images_right = [pg.transform.rotozoom(pg.image.load(f'images/pacman_move{n}.png'), 0, 2) for n in range(4)]
    pacman_images_down = [pg.transform.rotozoom(pg.image.load(f'images/pacman_move{n}.png'), -90, 2) for n in range(4)]
    pacman_images_left = [pg.transform.rotozoom(pg.image.load(f'images/pacman_move{n}.png'), 180, 2) for n in range(4)]
    pacman_images_death = [pg.transform.rotozoom(pg.image.load(f'images/pacman_dead_{n}.png'), 0, 2) for n in range(10)]

    def __init__(self, game, settings, screen, sound):
        super().__init__()
        self.game = game
        self.screen = screen
        self.settings = settings
        self.sound = sound
        self.lives_left = 3 #probably add some call to settings
        self.image = pg.image.load("images/burst0.png")
        #**replace with timer animation later**
        self.rect = pg.Rect(self.center_pacman().x * self.settings.block_size,
                            self.center_pacman().y * self.settings.block_size, 28, 28)  # self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.posn = self.center_pacman() #posn is the centerx, bottom of the rect, not left, top
        self.pxPosn = Vector(self.posn.x * self.settings.block_size, self.posn.y * self.settings.block_size)
        self.vel = Vector(-1, 0)
        self.bufferedDir = Vector()
        self.dying = self.dead = False
        self.portal = Portal(self.game.maze, self)
        self.timer_up = Timer(frames=self.pacman_images_up, wait=70)
        self.timer_right = Timer(frames=self.pacman_images_right, wait=70)
        self.timer_down = Timer(frames=self.pacman_images_down, wait=70)
        self.timer_left = Timer(frames=self.pacman_images_left, wait=70)
        self.timer_death = Timer(frames=self.pacman_images_death, looponce=True)
        self.timer = self.timer_left

    def center_pacman(self):
        return Vector(30, 48)

    def reset(self):
        self.vel = self.bufferedDir = Vector()
        self.posn = self.center_pacman()
        self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size, (self.posn.y + 0.5) * self.settings.block_size)
        self.rect.left, self.rect.top = self.pxPosn.x, self.pxPosn.y
        self.vel = Vector(-1, 0)
        self.dying = self.dead = False
        self.game.blinky.isPacmanDead = False
        self.game.pinky.isPacmanDead = False
        self.game.inky.isPacmanDead = False
        self.game.clyde.isPacmanDead = False

    def spawn_portal(self):
        if self.vel.x != 0 or self.vel.y != 0:
            self.portal.reset()
            self.portal.addToMap()

    def check_hit(self):
        if pg.sprite.collide_rect(self, self.game.blinky):
            if self.game.blinky.isEaten: pass
            elif not self.game.blinky.isScared: self.hit() # print("COLLISION WITH BLINKY")
            else:
                self.game.blinky.die()
                self.game.scoreboard.increment_score(2)
        if pg.sprite.collide_rect(self, self.game.pinky):
            if self.game.pinky.isEaten: pass
            elif not self.game.pinky.isScared: self.hit() # print("COLLISION WITH PINKY")
            else:
                self.game.pinky.die()
                self.game.scoreboard.increment_score(2)
        if pg.sprite.collide_rect(self, self.game.inky):
            if self.game.inky.isEaten: pass
            elif not self.game.inky.isScared: self.hit() # print("COLLISION WITH INKY")
            else:
                self.game.inky.die()
                self.game.scoreboard.increment_score(2)
        if pg.sprite.collide_rect(self, self.game.clyde):
            if self.game.clyde.isEaten: pass
            elif not self.game.clyde.isScared: self.hit() # print("COLLISION WITH CLYDE")
            else:
                self.game.clyde.die()
                self.game.scoreboard.increment_score(2)

    def hit(self):
        # CHANGE TIMERS
        self.vel = Vector()
        self.sound.pacman_die()
        self.dying = True
        self.game.blinky.isPacmanDead = True
        self.game.pinky.isPacmanDead = True
        self.game.inky.isPacmanDead = True
        self.game.clyde.isPacmanDead = True
        self.timer = self.timer_death

    def die(self):
        self.lives_left -= 1
        print(f'Pac-Man died! Only {self.lives_left} lives left')
        self.game.reset_death() if self.lives_left > 0 else self.game.game_over
        #**might have to alter above line**

    def update(self, ticks):
        self.check_hit()
        if self.dying and self.timer == self.timer_death and self.timer.finished:
            self.game.reset_death()
            self.timer_death.reset()
        # print(self.bufferedDir)
        if self.game.maze.getMaze(self.posn) == 's':
            self.posn = Vector(1, 30)
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                 (self.posn.y + 0.5) * self.settings.block_size)
        elif self.game.maze.getMaze(self.posn) == 'S':
            self.posn = Vector(59, 30)
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                 (self.posn.y + 0.5) * self.settings.block_size)
        elif self.game.maze.getMaze(self.posn) == 'A':
            self.posn = self.portal.posnB + self.portal.dirA
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                 (self.posn.y + 0.5) * self.settings.block_size)
        elif self.game.maze.getMaze(self.posn) == 'a':
            self.posn = self.portal.posnA - self.portal.dirA
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size,
                                 (self.posn.y + 0.5) * self.settings.block_size)
        if self.bufferedDir.x != 0 or self.bufferedDir.y != 0:
            if not gf.checkWall(self.game.maze, self.posn, self.bufferedDir):
                self.vel = self.bufferedDir
                self.bufferedDir = Vector()
        if gf.checkWall(self.game.maze, self.posn, self.vel):
            self.vel = Vector()
            self.pxPosn = Vector((self.posn.x + 0.5) * self.settings.block_size, (self.posn.y + 0.5) * self.settings.block_size)
        elif self.vel.x == 0:
            self.pxPosn.x = (self.posn.x + 0.5) * self.settings.block_size
            if self.vel.y == 1: self.timer = self.timer_down
            elif self.vel.y == -1: self.timer = self.timer_up
        elif self.vel.y == 0:
            self.pxPosn.y = (self.posn.y + 0.5) * self.settings.block_size
            if self.vel.x == 1: self.timer = self.timer_right
            elif self.vel.x == -1: self.timer = self.timer_left
        if ticks % 24 == 0:
            self.pxPosn += (self.vel * self.settings.speed_pacman)
        self.posn = Vector(math.floor(self.pxPosn.x / self.settings.block_size),
                           math.floor(self.pxPosn.y / self.settings.block_size))

        self.draw()

    def draw(self):
        # self.screen.blit(self.image, self.rect)
        # pg.draw.rect(self.screen, [255, 90, 200], [])
        # pg.draw.circle(self.screen, self.settings.color_pacman,
                       #[self.pxPosn.x, self.pxPosn.y], 14)
        self.image = self.timer.imagerect()
        # rect = self.image.get_rect
        # rect.left, rect.top = self.pxPosn.x - 2 - self.settings.block_size / 2, self.pxPosn.y - 2 - self.settings.block_size / 2
        rect = pg.Rect(self.pxPosn.x - 33, self.pxPosn.y - 33, 32, 32)
        self.screen.blit(self.image, rect)
        self.rect = pg.Rect(self.pxPosn.x - self.settings.block_size / 2, self.pxPosn.y - self.settings.block_size / 2,
                            28, 28)