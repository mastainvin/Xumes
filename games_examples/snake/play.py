import pygame
import sys
from pygame.math import Vector2

from games_examples.snake.src.fruit import Fruit
from games_examples.snake.src.snake import Snake

cell_size = 30
cell_number = 15


class Main:
    terminated = False
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (cell_number * cell_size, cell_number * cell_size))
        self.clock = pygame.time.Clock()
        self.running = True
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

        self.snake = Snake()
        self.fruit = Fruit()


    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit(self.screen)
        self.snake.draw_snake(self.screen)

    def fruit_ate(self):
        self.fruit.randomize()
        self.snake.add_block()
        # update state fruit ate

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit_ate()

    def game_over(self):

        self.snake = Snake()
        self.fruit = Fruit()
        self.terminated = False

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.terminated = True
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.terminated = True
                self.game_over()

    def check_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.snake.direction.y != 1:
                    self.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if self.snake.direction.y != -1:
                    self.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if self.snake.direction.x != 1:
                    self.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if self.snake.direction.x != -1:
                    self.snake.direction = Vector2(1, 0)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.check_events(event)
                if event.type == self.SCREEN_UPDATE:
                    self.update()

            self.screen.fill((175, 215, 70))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.run()
