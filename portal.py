# import pygame as pg
# from pygame.sprite import Sprite
from vector import Vector

class Portal():
    def __init__(self, maze, pacman):
        # super().__init__()
        self.maze = maze
        self.pacman = pacman
        self.posnA = Vector()
        self.posnB = Vector()
        self.dirA = pacman.vel
        # 0 is UP, 1 is RIGHT, 2 is DOWN, 3 is LEFT
        # self.addToMap()

    def setPosn(self, posnA):
        self.posnA = posnA
        self.setPosB()

    def setPosB(self):
        blocksBehind = 0
        nextBlockCh = ','
        while nextBlockCh != '.':
            blocksBehind += 1
            nextBlockCh = self.maze.getMaze(self.pacman.posn - (blocksBehind * self.pacman.vel))
        self.posnB = self.pacman.posn - (blocksBehind * self.pacman.vel)

    def addToMap(self):
        blocksAhead = 0
        nextBlockCh = ','
        while nextBlockCh != '.':
            blocksAhead += 1
            nextBlockCh = self.maze.getMaze(self.pacman.posn + (blocksAhead * self.pacman.vel))
        self.setPosn(self.pacman.posn + (blocksAhead * self.pacman.vel))
        self.dirA = self.pacman.vel
        self.maze.setMaze(self.posnA, 'A')
        self.maze.setMaze(self.posnB, 'a')

    def reset(self):
        self.maze.setMaze(self.posnA, '.')
        self.maze.setMaze(self.posnB, '.')