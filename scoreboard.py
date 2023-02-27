import pygame as pg
import random
# import pygame.font

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 0
        self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        # self.bg = game.bg
        self.screen_rect = self.screen.get_rect()

        self.text_color = (254, 250, 240)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.prep_score()

    def increment_score(self, type):
        if type == 0:
            self.score += 10
        elif type == 1:
            self.score += 50
        else:
            self.score += 100
        self.prep_score()

    def prep_score(self): 
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def get_hi_score(self):
        with open("hi_score.txt") as file:
            for line in file:
                pass
            self.high_score = int(line)
            return self.high_score

    def set_hi_score(self, score):
        file = open("hi_score.txt", 'a')
        file.write("\n"+str(score))
        file.close()

    def reset(self): 
        self.score = 0
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)