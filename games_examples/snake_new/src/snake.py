import random
import sys

import pygame
from pygame import Vector2

cell_size = 30


class Snake:

    def __init__(self, body=None, direction=None):
        if body is None:
            body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        if direction is None:
            direction = Vector2(1, 0)

        self.new_block = False
        self.fruit_ate = False

        self.body = body
        self.direction = direction

    def draw_snake(self, screen):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        print(self.fruit_ate)
        if self.new_block:
            body_copy = self.body[:]
            self.fruit_ate=True
            #print(self.fruit_ate)
            #print(body_copy)
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            #print(body_copy)

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.fruit_ate=False

        self.new_block = False

    def reset2(self):
        #for bumping into wall
        self.body = [Vector2(13, 10), Vector2(12, 10), Vector2(11, 10), Vector2(11, 9), Vector2(11, 8),
                     Vector2(11, 7), Vector2(12, 7), Vector2(13, 7), Vector2(14, 7)]
        self.direction = Vector2(1, 0)
        self.fruit_ate=False

        self.new_block = False

    def reset3(self):
        # for bumping into itself

        self.body = [Vector2(9, 10), Vector2(8, 10), Vector2(7, 10), Vector2(7, 9), Vector2(7, 8),
                     Vector2(7, 7), Vector2(8, 7), Vector2(9, 7), Vector2(10, 7), Vector2(10, 6),
                     Vector2(10, 5), Vector2(10, 4)]
        self.direction = Vector2(0, -1)
        self.fruit_ate = False

        self.new_block = False

    def check_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.direction.y != 1:
                    self.direction = Vector2(0, -1)

            if event.key == pygame.K_DOWN:
                if self.direction.y != -1:
                    self.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT:
                if self.direction.x != 1:
                    self.direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT:
                if self.direction.x != -1:
                    self.direction = Vector2(1, 0)

            print(self.direction)