import logging

import pygame

from games_examples.flappy_bird.params import PIPE_WIDTH, PIPE_SPACE, HEIGHT, PIPE_SPEED, SIZE, LEFT_POSITION


class Pipe:
    player_passed = False

    def __init__(self, player=None, generator=None, space_length=PIPE_SPACE, height=100, position=0):
        self.space_length = space_length
        self.width = PIPE_WIDTH
        self.position = position
        self.height = height
        self.player = player
        self.generator = generator
        self.rect1 = pygame.Rect(self.position, -3000, self.width, height+3000)
        self.rect2 = pygame.Rect(self.position, self.space_length + self.height, self.width, HEIGHT - self.height)

    def draw(self, canvas):
        pygame.draw.rect(canvas, "green", self.rect1)
        pygame.draw.rect(canvas, "green", self.rect2)

    def move(self, dt):
        # Go to left
        self.position -= dt * PIPE_SPEED
        # Move rectangles
        self.rect1 = pygame.Rect(self.position, -3000, self.width, self.height+3000)
        self.rect2 = pygame.Rect(self.position, self.space_length + self.height, self.width,
                                 HEIGHT - self.height - self.space_length)

        # Check if collides with player
        if not self.collision():
            # Check if player passed the pipe (win one point)
            self.is_player_passed()

    def collision(self):
        # if the pipe collides we stop the game
        if (
                self.position <= SIZE + LEFT_POSITION <= self.position + PIPE_WIDTH or self.position <= LEFT_POSITION <= self.position + PIPE_WIDTH) and (
                self.player.position <= self.height or self.player.position + SIZE >= self.space_length + self.height):
            self.generator.end()
            return True
        return False

    def is_player_passed(self):
        if self.position + PIPE_WIDTH / 2 <= SIZE + LEFT_POSITION and not self.player_passed:
            self.player_passed = True
            self.player.gain_point()
