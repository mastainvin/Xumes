import random
import numpy as np
import pygame

from games_examples.flappy_bird.params import SPACE_BETWEEN_PIPES, PIPE_WIDTH, PIPE_SPEED, WIDTH, LEFT_POSITION, HEIGHT, \
    PIPE_SPACE
from games_examples.flappy_bird.src.pipe import Pipe


class PipeGenerator:

    def __init__(self, game=None):
        self.pipes = []
        self.game = game
        self.time_between = (SPACE_BETWEEN_PIPES + PIPE_WIDTH) / PIPE_SPEED
        self.time_spent = 0

    def reset(self):
        self.pipes = []
        self.time_spent = 0

    def reset_random(self):
        number_of_pipes = WIDTH // (SPACE_BETWEEN_PIPES + PIPE_WIDTH)
        self.pipes = []
        start_position = np.random.uniform(LEFT_POSITION, WIDTH / 3)
        for i in range(number_of_pipes):
            self.pipes.append(
                Pipe(self.game.player, self, position=start_position + i * (PIPE_WIDTH + SPACE_BETWEEN_PIPES),
                     height=random.randint(50, HEIGHT - 50 - PIPE_SPACE)))

    def gen_pipe(self):
        # Create a pipe with random height
        # TODO make an easy way to change how we compute the height (random or not)
        return Pipe(self.game.player, self, position=100 + WIDTH,
                    height=random.randint(50, HEIGHT - 50 - PIPE_SPACE))

    def generator(self, dt):
        self.time_spent += dt
        # We wait enough time and create a new pipe
        if self.pipes:
            if WIDTH - self.pipes[-1].position + 100 > SPACE_BETWEEN_PIPES:
                self.time_spent = 0
                self.pipes.append(self.gen_pipe())
        else:
            self.pipes.append(self.gen_pipe())

    def move(self, dt):
        pipes_to_delete = []
        for pipe in self.pipes:
            pipe.move(dt)
            # if the pipe is out screen we delete him
            if pipe.position < -100:
                pipes_to_delete.append(pipe)
        for pipe in pipes_to_delete:
            self.pipes.remove(pipe)

    def draw(self, canvas):
        for pipe in self.pipes:
            pipe.draw(canvas)

    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'pipes: {len(self.pipes)}', False, (0, 0, 0))
        canvas.blit(text_surface, (0, 20))

    def end(self):
        self.game.end_game()
