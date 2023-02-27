import sys
import pygame as pg
from vector import Vector
from maze import Maze

#Continuous movement of pacman
movement = {pg.K_a: Vector(-1, 0),   # dictionary to map keys to Vector velocities
            pg.K_d: Vector(1, 0),
            pg.K_w: Vector(0, -1),
            pg.K_s: Vector(0, 1)
            }

def check_keydown_events(event, maze, pacman, game):
    key = event.key
    if key in movement.keys():
        if not checkWall(maze, pacman.posn, movement[key]):
            pacman.bufferedDir = Vector()
            if not pacman.dying:
                pacman.vel = movement[key]
        else: pacman.bufferedDir = movement[key]
        if key == pg.K_w:
            game.selected = True
        elif key == pg.K_s:
            game.selected = False
    elif key == pg.K_RETURN:
        if game.selected:
            game.starting = True
        else:
            game.showing_hi_score = True
    elif key == pg.K_SPACE:
        pacman.spawn_portal()

def check_keyup_events(event, pacman):
    key = event.key
    # if key in movement.keys(): pacman.vel = Vector()

def check_events(maze, pacman, game):
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, maze=maze, pacman=pacman, game=game)
        elif event.type == pg.KEYUP: check_keyup_events(event=event, pacman=pacman)

#Subject cant move outside of the , o 0 s a b
def checkWall(maze, posn, movement):
    if maze.getMaze(posn + movement) == "X" or maze.getMaze(posn + movement) == ".":
        return True
    else:
        return False