import sys

import pygame

from games_examples.super_mario.classes.Level import Level
from games_examples.super_mario.classes.Menu import Menu
from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.classes.Dashboard import Dashboard

windowSize = 640, 480


class Game:
    terminated = False

    def __init__(self, levelname, feature):

        pygame.mixer.pre_init(44100, -16, 2, 4096)
        pygame.init()
        self.levelname, self.feature = levelname, feature
        self.screen = pygame.display.set_mode(windowSize)
        self.max_frame_rate = 240
        self.dashboard = Dashboard("font.png", 8, self.screen)
        self.level = Level(self.screen,self.dashboard, self.levelname, self.feature)
        self.mario = Mario(0, 0, self.level, self.screen, self.dashboard)
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

    def run(self):

        while True:

            pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(self.clock.get_fps())))
            self.level.drawLevel(self.mario.camera, self.dt)
            self.dashboard.update()

            print(self.mario.rect.x)
            self.mario.update(self.dt)

            if self.mario.restart or self.mario.ending_level:
                self.end_game()

            self.check_end()
            self.dt = self.clock.tick(self.max_frame_rate) / 1000

            self.render()

    def render(self):
        pygame.display.update()
        self.dt = self.clock.tick(self.max_frame_rate) / 1000

    def check_end(self):
        if self.terminated:
            self.reset(["ennemies","1-0"])

    def end_game(self):
        self.terminated = True

    def reset(self, feature):
        self.terminated = False
        self.dashboard = Dashboard("font.png", 8, self.screen)
        self.level = Level(self.screen, self.dashboard, self.levelname, feature)
        self.mario = Mario(0, 0, self.level, self.screen, self.dashboard)
        self.clock = pygame.time.Clock()


if __name__ == "__main__":
    game = Game("ennemies_feature", ["ennemies","1-0"])
    game.run()

