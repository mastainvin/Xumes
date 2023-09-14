# Connected

# Author : Prajjwal Pathak (pyguru)
# Date : Thursday, 8 August, 2021

import random
import pygame

from games_examples.connected.objects import Message

import pygame

from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
from games_examples.connected.src.generator import Generator
from games_examples.connected.src.tile import Tiles
from games_examples.connected.src.ball import Balls
from games_examples.connected.src.coin import Coins

BACKGROUND_COLOR = (137, 207, 240)


class Game:
    height = HEIGHT
    width = WIDTH
    CENTER = WIDTH // 2, HEIGHT // 2
    terminated = False

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.win = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.dt = 0

        self.last_click_time = pygame.time.get_ticks()
        self.clicked = False
        self.ball = Balls(y=CENTER[1],  game=self)
        self.generator = Generator(game=self)

        # self.score_msg = Message(self.WIDTH // 2, 100, 60, "0", self.score_font, (150, 150, 150), self.win)
    def run(self):
        while self.running:

            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # Background
            self.win.fill(BACKGROUND_COLOR)

            # Make all game state modification
            self.ball.change_direction()
            self.generator.generator(self.dt)
            self.ball.update(self.dt)
            self.generator.move(self.dt)

            self.check_end()

            self.render()

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

    def reset(self):
        self.generator.reset()
        self.ball.reset()
        self.terminated = False

    def render(self):
        # Draw every component
        self.ball.draw(self.win)
        self.generator.draw(self.win)
        self.ball.logs(self.win)

    def check_end(self):
        if self.terminated:
            pass
            # self.reset()

    def end_game(self):
        self.terminated = True

    #

if __name__ == "__main__":
    game = Game()
    game.run()
