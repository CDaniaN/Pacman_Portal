import pygame as pg
from settings import Settings
import game_functions as gf
from maze import Maze
from pacman import Pacman
from settings import Settings
from sound import Sound
from blinky import Blinky
from inky import Inky
from pinky import Pinky
from clyde import Clyde
from vector import Vector
from scoreboard import Scoreboard
from fruit import Fruit
import math
import random
import sys

class Game:
    def __init__(self):
        pg.init()
        self.maze = Maze(self)
        self.level = 0
        self.settings = Settings(game=self)
        size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Pacman Portal")
        self.title_bg = pg.transform.rotozoom(pg.image.load('images/bg.png'), 0, 1)

        self.sound = Sound(bg_music="sounds/bgm.wav") #replace

        self.scoreboard = Scoreboard(game=self)
        self.pacman = Pacman(game=self, screen=self.screen, settings=self.settings, sound=self.sound)
        self.blinky = Blinky(game=self)
        self.inky = Inky(game=self)
        self.pinky = Pinky(game=self)
        self.clyde = Clyde(game=self)
        self.fruit = Fruit(game=self)
        self.fruit_time = -10001

        self.lives = 3
        self.lives_pacman_image = pg.transform.rotozoom(pg.image.load('images/pacman_move2.png'), 0, 1.5)

        self.selected = True
        self.starting = False
        self.showing_hi_score = False

    def reset(self):
        print('Resetting game...')

        self.pacman.reset()
        # self.lives -= 1
        if self.lives < 1: self.game_over()
        self.blinky.reset()
        self.pinky.reset()
        self.inky.reset()
        self.clyde.reset()
        self.maze.reset()
        self.blinky_time = self.elapsed

    def reset_death(self):
        print('Resetting game...')

        self.pacman.reset()
        self.lives -= 1
        if self.lives < 1: self.game_over()
        self.blinky.reset()
        self.pinky.reset()
        self.inky.reset()
        self.clyde.reset()
        # self.maze.reset()
        self.blinky_time = self.elapsed

    def game_over(self):
        print('Pacman Died :(')
        # self.sound.gameover()
        if self.scoreboard.score > self.scoreboard.get_hi_score():
            self.scoreboard.set_hi_score(self.scoreboard.score)
        pg.quit()
        sys.exit()

    def play(self):
        # self.sound.play_bg()
        # play cutscene
        self.startTime = pg.time.get_ticks()
        self.elapsed = self.blinky_time = 0
        while True:
            if pg.time.get_ticks() > self.startTime + self.elapsed:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
                # print(self.elapsed)
                self.elapsed += 1
                gf.check_events(maze=self.maze, pacman=self.pacman, game=self)
                self.screen.fill(self.settings.bg_color)
                self.maze.update(self.pacman)

                for y in range(self.maze.rows):
                    for x in range(self.maze.cols):
                        if self.maze.maze[y][x] == 'S' or self.maze.maze[y][x] == 's' or self.maze.maze[y][x] == 'A' or \
                                self.maze.maze[y][x] == 'a':
                            pg.draw.rect(self.screen, [220, 200, 255],
                                         [x * self.settings.block_size, y * self.settings.block_size,
                                          self.settings.block_size, self.settings.block_size])
                        elif self.maze.maze[y][x] == 'X':
                            pg.draw.rect(self.screen, [60, 20, 220],
                                         [x * self.settings.block_size, y * self.settings.block_size,
                                          self.settings.block_size, self.settings.block_size])
                        elif self.maze.maze[y][x] == 'o':
                            pg.draw.circle(self.screen, [255, 255, 0],
                                         [(x + 0.5) * self.settings.block_size, (y + 0.5) * self.settings.block_size],
                                           self.settings.block_size / 4)
                        elif self.maze.maze[y][x] == '0':
                            if math.floor(self.elapsed / 32) % 2 == 0:
                                pg.draw.circle(self.screen, [255, 255, 0],
                                             [(x + 0.5) * self.settings.block_size, (y + 0.5) * self.settings.block_size],
                                               self.settings.block_size / 2)
                            else:
                                pg.draw.circle(self.screen, [255, 194, 0],
                                               [(x + 0.5) * self.settings.block_size,
                                                (y + 0.5) * self.settings.block_size],
                                               self.settings.block_size / 2)
                if self.elapsed % 2000 < 2:
                    if random.randint(0, 4) == 0:
                        # print('rngtime bro')
                        self.fruit.isActive = True
                        self.fruit_time = self.elapsed
                if self.elapsed >= self.fruit_time + 2000: self.fruit.isActive = False
                self.fruit.update()
                self.pacman.update(self.elapsed)
                self.blinky.update(self.elapsed)
                if self.elapsed >= self.blinky_time + 500:
                    self.pinky.update(self.elapsed)
                if self.elapsed >= self.blinky_time + 1000:
                    self.inky.update(self.elapsed)
                if self.elapsed >= self.blinky_time + 1500:
                    self.clyde.update(self.elapsed)
                self.scoreboard.update()
                image_rect = image_rect2 = image_rect3 = self.lives_pacman_image.get_rect()
                image_rect.left += 8
                image_rect.top += 8
                self.screen.blit(self.lives_pacman_image, image_rect)
                if(self.lives > 1):
                    image_rect2.left += 24
                    # image_rect2.top += 8
                    self.screen.blit(self.lives_pacman_image, image_rect2)
                if(self.lives > 2):
                    image_rect3.left += 24
                    # image_rect3.top += 8
                    self.screen.blit(self.lives_pacman_image, image_rect3)
                pg.display.flip()

    def title(self):
        self.sound.play_title_music()
        self.hi_score_font = pg.font.SysFont(None, 48)
        self.pointer = pg.transform.rotozoom(pg.image.load('images/pacman_move1.png'), 0, 1.5)
        self.pointer_rect = self.pointer.get_rect()
        self.selected = 0
        self.showing_hi_score = False
        self.title_text = self.hi_score_font.render(str(self.scoreboard.get_hi_score()), False, (255, 255, 255))
        self.title_text_area = self.title_text.get_rect()
        self.title_text_area.center = (525, 625)
        while True:
            gf.check_events(maze=self.maze, pacman=self.pacman, game=self)
            if self.starting:
                self.sound.stop_title_music()
                self.pacman.bufferedDir = Vector()
                self.play()
            self.screen.blit(self.title_bg, (0, 0))
            if self.showing_hi_score == True:
                self.screen.blit(self.title_text, self.title_text_area)
            if self.selected:
                self.pointer_rect.left, self.pointer_rect.top = 150, 539
            else:
                self.pointer_rect.left, self.pointer_rect.top = 160, 599
            self.screen.blit(self.pointer, self.pointer_rect)
            # self.screen.blit(self.name_text, self.name_text_area)
            pg.display.flip()

def main():
    g = Game()
    g.title()


if __name__ == '__main__':
    main()
