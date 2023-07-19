import sys

import pygame
from pygame import Vector2

cell_size = 30


class Snake:


    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False


    def draw_snake(self, screen):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
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