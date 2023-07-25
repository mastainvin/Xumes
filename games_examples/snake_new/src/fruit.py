import random

import pygame
from pygame import Vector2

cell_size = 30
cell_number = 15


class Fruit:
    def __init__(self):

        self.randomize()

    def draw_fruit(self, screen):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (200, 100, 50), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def reset(self):

        self.randomize()

    # def reset(self,x,y):
    #     # you can set the coordinates of the fruit
    #     self.y = y
    #     self.x = x
    #     self.pos = Vector2(self.x, self.y)