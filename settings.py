from maze import Maze
from vector import Vector

class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self, game):
        """Initialize the game's settings."""
        # Screen settings
        maze = game.maze
        self.block_size = 11
        self.screen_width = maze.cols * self.block_size
        self.screen_height = maze.rows * self.block_size
        self.bg_color = (1, 1, 20)

        self.speed_pacman = self.block_size * 0.9
        self.speed_blinky = 0.8 * self.speed_pacman + game.level * 0.06
        self.speed_pinky = 0.6 * self.speed_pacman + game.level * 0.06
        self.speed_inky = 0.55 * self.speed_pacman + game.level * 0.06
        self.speed_clyde = 0.4 * self.speed_pacman + game.level * 0.06
        self.speed_scared = 0.2 * self.speed_pacman
        self.speed_eaten = 1.12 * self.speed_pacman

        self.scatter_blinky = Vector(60, 0)
        self.scatter_pinky = Vector(0, 0)
        self.scatter_clyde = Vector(0, 64)
        self.scatter_inky = Vector(60, 64)

        self.color_pacman = [255, 255, 0]
        self.color_blinky = [237, 39, 36]
        self.color_pinky = [253, 194, 212]
        self.color_clyde = [255, 183, 72]
        self.color_inky = [0, 255, 223]

        self.fruit_spawn = Vector(30, 36)
