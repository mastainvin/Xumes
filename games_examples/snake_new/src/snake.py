import random
import sys

import pygame
from pygame import Vector2
import time
cell_size = 30


class Snake:

    def __init__(self, body=None, direction=None):
        if body is None:
            body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        if direction is None:
            direction = Vector2(1, 0)

        self.new_block = False
        self.fruit_ate = False
        self.last_keydown_time=0
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
        print(len(self.body))
        if self.new_block:
            body_copy = self.body[:]
            self.fruit_ate=True
            print(len(self.body))
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


    def check_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            current_time = pygame.time.get_ticks()

            # 检查时间差是否大于0.2秒
            if current_time - self.last_keydown_time >= 151:  # 200毫秒 = 0.2秒
                # 处理pygame.KEYDOWN事件
                # 更新上一次接收pygame.KEYDOWN事件的时间戳

                if event.key == pygame.K_UP:
                    if self.direction.y == 0:
                        self.direction = Vector2(0, -1)
                        self.last_keydown_time = current_time

                if event.key == pygame.K_DOWN:
                    if self.direction.y == 0:
                        self.direction = Vector2(0, 1)
                        self.last_keydown_time = current_time

                if event.key == pygame.K_LEFT:
                    if self.direction.x == 0:
                        self.direction = Vector2(-1, 0)
                        self.last_keydown_time = current_time

                if event.key == pygame.K_RIGHT:
                    if self.direction.x == 0:
                        self.direction = Vector2(1, 0)
                        self.last_keydown_time = current_time
            # print("Handling KEYDOWN event")

            print(self.direction)