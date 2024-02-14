import random

import pygame

from demo.flappy_bird.params import LEFT_POSITION, PIPE_SPACE, HEIGHT, JUMP_SPEEDUP, FALL_SPEEDUP, \
    PIPE_SPEED, BIRD_WIDTH, BIRD_HEIGHT

PLAYER_COLOR = "yellow"

class Player:
    speedup = 0
    points = 0
    dt_jump = 0
    distance = 0

    def __init__(self, position=None, game=None):
        self.initial_position = position
        self.position = position
        self.game = game
        self.reward = False
        self.image = pygame.image.load("/home/vincent/Documents/Xumes/demo/flappy_bird/assets/bird.png")
        self.image = pygame.transform.scale(self.image, (BIRD_WIDTH, BIRD_HEIGHT))

    def reset(self):
        self.position = self.initial_position
        self.speedup = 0
        self.points = 0
        self.distance = 0
        self.reward = False
        self.dt_jump = 0

    def reset_random(self, pipes):
        self.speedup = 0
        self.points = 0
        self.distance = 0
        self.reward = False
        self.dt_jump = 0
        in_pipe = False
        for pipe in pipes:
            if LEFT_POSITION <= pipe.position <= LEFT_POSITION + BIRD_WIDTH:
                self.position = random.uniform(pipe.height + BIRD_HEIGHT + 10, pipe.height + PIPE_SPACE - BIRD_HEIGHT - 10)
                in_pipe = True
                break
        if not in_pipe:
            self.position = random.uniform(100, HEIGHT - 100)

    def wait_jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        if self.dt_jump >= 0.2:
            self.speedup = JUMP_SPEEDUP
            self.dt_jump = 0

    def move(self, dt):
        self.position -= self.speedup * dt
        self.speedup -= FALL_SPEEDUP * dt
        self.dt_jump += dt
        self.distance += dt * PIPE_SPEED
        self.collision()

    def collision(self):
        if self.position > HEIGHT - BIRD_HEIGHT:
            self.game.end_game()

    def draw(self, canvas):
        canvas.blit(self.image, (LEFT_POSITION, self.position, BIRD_WIDTH, BIRD_HEIGHT))

    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'points: {self.points} speedup: {self.speedup}',
                                      False, (0, 0, 0))
        canvas.blit(text_surface, (0, 0))

    def gain_point(self):
        self.points += 1
        self.reward = True

    @property
    def center(self):
        return LEFT_POSITION + BIRD_WIDTH / 2, self.position + BIRD_HEIGHT / 2
