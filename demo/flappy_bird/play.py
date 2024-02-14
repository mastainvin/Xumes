import pygame

from demo.flappy_bird.params import HEIGHT, WIDTH
from demo.flappy_bird.src.pipe_generator import PipeGenerator
from demo.flappy_bird.src.player import Player

BACKGROUND_COLOR = (137, 207, 240)


class Game:
    height = HEIGHT
    width = WIDTH
    terminated = False

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.dt = 0

        self.player = Player(position=self.height // 2, game=self)
        self.pipe_generator = PipeGenerator(game=self)

    def run(self):
        while self.running:

            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Background
            self.screen.fill(BACKGROUND_COLOR)

            # Make all game state modification
            self.player.wait_jump()
            self.pipe_generator.generator(self.dt)
            self.player.move(self.dt)
            self.pipe_generator.move(self.dt)

            self.check_end()

            self.render()

            # flip() the display to put your work on screen
            pygame.display.flip()

            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            self.dt = self.clock.tick(60) / 1000

    def reset(self):
        self.pipe_generator.reset()
        self.player.reset()
        self.terminated = False

    def render(self):
        # Draw every component
        self.player.draw(self.screen)
        self.pipe_generator.draw(self.screen)
        self.player.logs(self.screen)

    def check_end(self):
        if self.terminated:
            self.reset()
            pass

    def end_game(self):
        self.terminated = True


if __name__ == "__main__":
    game = Game()
    game.run()
