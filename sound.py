import pygame as pg
import time


class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(1)
        self.nom = pg.mixer.Sound('sounds/nom.wav')
        self.nom_power = pg.mixer.Sound('sounds/nom_power.wav')
        self.eat_fruit = pg.mixer.Sound('sounds/eat_fruit.wav')
        self.ghost_walking = pg.mixer.Sound('sounds/ghost_walking.wav')  # indefinitely
        self.ghost_scared = pg.mixer.Sound('sounds/ghost_scared.wav')  # indefinitely
        self.ghost_dies = pg.mixer.Sound('sounds/ghost_dies.wav')
        self.pacman_dies = pg.mixer.Sound('sounds/pacman_dying.wav')
        self.win = pg.mixer.Sound("sounds/you_win.wav")

        # Channels for the sounds
        self.channel0 = pg.mixer.Channel(0)
        self.channel1 = pg.mixer.Channel(1)
        self.channel2 = pg.mixer.Channel(2)
        self.channel3 = pg.mixer.Channel(3)
        self.channel4 = pg.mixer.Channel(4)
        self.channel5 = pg.mixer.Channel(5)
        self.channel6 = pg.mixer.Channel(6)
        self.channel7 = pg.mixer.Channel(7)
        self.channel0.set_volume(0.5)
        self.channel2.set_volume(0)
        self.channel3.set_volume(0)
        self.channel6.set_volume(0.5)
        self.channel2.play(self.ghost_walking, -1)
        self.channel3.play(self.ghost_scared, -1)

    def play_title_music(self):
        pg.mixer.music.play(loops=-1)

    def stop_title_music(self):
        pg.mixer.music.stop()

    def pacman_nom(self):
        self.channel0.play(self.nom, 0)

    def pacman_nom_power(self):
        self.channel1.play(self.nom_power, 0)

    def ghost_chase(self):
        self.channel2.set_volume(1)

    def ghost_stop_chase(self):
        self.channel2.set_volume(0)

    def ghost_scare(self):
        self.channel3.set_volume(0.4)

    def ghost_stop_scare(self):
        self.channel3.set_volume(0)

    def ghost_die(self):
        self.channel4.play(self.ghost_dies, 0)

    def pacman_die(self):
        self.channel5.play(self.pacman_dies, 0)

    def fruit_eaten(self):
        self.channel6.play(self.eat_fruit, 0)

    def you_win(self):
        self.channel7.play(self.win, 0)

    def stop_bg(self):
        self.channel0.stop()
        self.channel1.stop()
        self.channel2.stop()
        self.channel3.stop()
        self.channel4.stop()
        self.channel5.stop()
        self.channel6.stop()

    def shoot_laser(self):
        self.sounds['laser'].set_volume(0.1)
        pg.mixer.Sound.play(self.sounds['laser'])

    def gameover(self):
        self.stop_bg()
        pg.mixer.music.load('sounds/gameover.wav')
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(1)
        time.sleep(2.8)