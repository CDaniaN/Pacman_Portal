# from game import Game
from scoreboard import Scoreboard

class Maze:
    def __init__(self, game):
        self.rows, self.cols = (65, 61)
        self.maze = [[1 for x in range(self.cols)] for y in range(self.rows)]
        self.game = game
        self.now = -10001
        # print(self.maze)
        self.reset()

    def reset(self):
        yIndex = 0
        file = open("map.txt")
        for line in file:
            xIndex = 0
            if yIndex >= self.rows:
                # print("yIndex too high! greater than self.rows")
                break
            for currCh in line:
                if xIndex >= self.cols:
                    # print("xIndex too high! greater than self.cols")
                    break
                else:
                    self.maze[yIndex][xIndex] = currCh
                xIndex += 1
            yIndex += 1
        # print(self.maze)

    def getMaze(self, posn):
        return self.maze[posn.y][posn.x]

    def setMaze(self, posn, newCh):
        self.maze[posn.y][posn.x] = newCh

    def check_empty(self):
        yIndex = 0
        for line in self.maze:
            xIndex = 0
            if yIndex >= self.rows:
                # print("yIndex too high! greater than self.rows")
                break
            for currCh in line:
                if xIndex >= self.cols:
                    # print("xIndex too high! greater than self.cols")
                    break
                else:
                    if self.maze[yIndex][xIndex] == 'o' or self.maze[yIndex][xIndex] == '0': return False
                xIndex += 1
            yIndex += 1
        return True

    def update(self, pacman):
        pacBlock = self.getMaze(pacman.posn)
        if pacBlock == 'o':
            self.game.sound.pacman_nom()
            self.setMaze(pacman.posn, ',')
            self.game.scoreboard.increment_score(0)
            if self.check_empty():
                self.game.sound.you_win()
                self.game.level += 1
                self.game.reset()
        elif pacBlock == '0':
            self.game.sound.pacman_nom_power()
            self.game.inky.sound.ghost_stop_chase()
            self.game.inky.sound.ghost_scare()
            self.now = self.game.elapsed
            self.game.blinky.isScared = True
            self.game.blinky.timer = self.game.blinky.timer_scared
            # self.game.blinky.vel *= -1
            # self.game.blinky.prevVel *= -1
            # self.game.blinky.pxPosn += self.game.blinky.prevVel
            self.game.pinky.isScared = True
            self.game.pinky.timer = self.game.pinky.timer_scared
            # self.game.pinky.vel *= -1
            # self.game.pinky.prevVel *= -1
            self.game.inky.isScared = True
            self.game.inky.timer = self.game.inky.timer_scared
            # self.game.inky.vel *= -1
            # self.game.inky.prevVel *= -1
            self.game.clyde.isScared = True
            self.game.clyde.timer = self.game.clyde.timer_scared
            # self.game.clyde.vel *= -1
            # self.game.clyde.prevVel *= -1
            self.setMaze(pacman.posn, ',')
            self.game.scoreboard.increment_score(1)
        if self.game.elapsed > self.now + 1700:
            self.game.inky.sound.ghost_stop_scare()
            self.game.inky.sound.ghost_chase()
            self.game.blinky.isScared = False
            self.game.blinky.timer = self.game.blinky.timer_normal
            self.game.pinky.isScared = False
            self.game.pinky.timer = self.game.pinky.timer_normal
            self.game.inky.isScared = False
            self.game.inky.timer = self.game.inky.timer_normal
            self.game.clyde.isScared = False
            self.game.clyde.timer = self.game.clyde.timer_normal
        elif self.game.elapsed > self.now + 1400:
            if self.game.blinky.isScared: self.game.blinky.timer = self.game.blinky.timer_unscaring
            if self.game.pinky.isScared: self.game.pinky.timer = self.game.pinky.timer_unscaring
            if self.game.inky.isScared: self.game.inky.timer = self.game.inky.timer_unscaring
            if self.game.clyde.isScared: self.game.clyde.timer = self.game.clyde.timer_unscaring
        self.check_empty()