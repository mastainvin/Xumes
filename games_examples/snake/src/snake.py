import pygame
from pygame import Vector2

cell_size = 30


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self, screen):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    # def move_snake(self):
    #     if self.new_block:
    #         body_copy = self.body[:]
    #         body_copy.insert(0, body_copy[0] + self.direction)
    #         self.new_block = False
    #         self.body = body_copy[:]
    #         return "longer"
    #     else:
    #         body_copy = self.body[:-1]
    #         body_copy.insert(0, body_copy[0] + self.direction)
    #         for i in range(len(body_copy) - 1, -1, -1):
    #             self.body[i] = body_copy[i]
    #     return " "



    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.new_block = False
            self.body = body_copy[:]
            return "longer"
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        return " "

    def add_block(self):
        self.new_block = True

    def update(self):
        self.move_snake()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        print("")

    def change_direction(self,key):
        if key == pygame.K_UP:
            if self.direction.y == 0:
                self.direction = Vector2(0, -1)
                return "dir_changed"
        elif key == pygame.K_DOWN:
            if self.direction.y == 0:
                self.direction = Vector2(0, 1)
                return "dir_changed"
        elif key == pygame.K_LEFT:
            if self.direction.x == 0:
                self.direction = Vector2(-1, 0)
                return "dir_changed"
        elif key == pygame.K_RIGHT:
            if self.direction.x == 0:
                self.direction = Vector2(1, 0)
                return "dir_changed"