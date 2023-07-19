import pygame
import sys
from pygame.math import Vector2
import time
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
        pygame.time.set_timer(self.SCREEN_UPDATE, 90)

        self.running = True

        self.snake = Snake()
        self.fruit = Fruit()


    def update(self):
        a = self.snake.move_snake()
        b = self.check_collision()
        c = self.check_fail()
        return  a + " " + b + " " + c

    def draw_elements(self):
        self.fruit.draw_fruit(self.screen)
        self.snake.draw_snake(self.screen)

    def fruit_ate(self):
        self.fruit.randomize()
        self.snake.add_block()
        # update state fruit ate
        return "ate"

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            a = self.fruit_ate()
            return a
        return ""

    def game_over(self):


        self.terminated = False
        time.sleep(0.05)
        self.snake.reset()
        self.fruit.reset()
        time.sleep(0.05)

    def check_fail(self):

        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.terminated = True
            time.sleep(0.05)
            self.game_over()
            a=str(self.snake.body[0].x)
            b=str(self.snake.body[0].y)
            c=a+b
            return c+" g"

        for index, block in enumerate(self.snake.body[1:]):

            if block == self.snake.body[0]:
                matching_index = index + 1  # 加上偏移量 1，因为切片从索引 1 开始
                self.terminated = True
                # print(self.snake.body[0].x)
                # print(self.snake.body[0].y)
                # print("index:",matching_index )
                # print(str(block.x))
                # print(str(block.y))
                # print("every:")
                # for b in self.snake.body[0:]:
                #     print("b.x:", b.x)
                #     print("b.y:", b.y)
                time.sleep(0.05)
                self.game_over()

                return "gg hitting itself"
        # print("every1:")
        # for b in self.snake.body[0:]:
        #     print("b.x:", b.x)
        #     print("b.y:", b.y)
        # a = str(self.snake.body[0].x)
        # b = str(self.snake.body[0].y )
        # c = a + b
        # return c+""
        return ""


    def check_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            self.snake.change_direction(event.key)


    def run(self):
        while self.running:

            for event in pygame.event.get():
                self.check_events(event)

                if event.type == self.SCREEN_UPDATE:
                    self.update()

            self.check_fail()
            self.screen.fill((175, 215, 70))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(0)

    def check_end(self):
        if self.terminated:
            self.reset()

    def end_game(self):
        self.terminated = True

if __name__ == "__main__":
    main = Main()
    main.run()
