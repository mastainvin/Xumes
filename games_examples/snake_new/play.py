import pygame
import sys
from pygame.math import Vector2
import time


from games_examples.snake.src.fruit import Fruit
from games_examples.snake_new.src.snake import Snake

cell_size = 30
cell_number = 15


class Game:
    terminated = False

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (cell_number * cell_size, cell_number * cell_size))
        self.clock = pygame.time.Clock()

        self.running = True

        self.dt = 0

        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.time.set_timer(self.SCREEN_UPDATE, 150)

        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


    def fruit_ate(self):
        self.fruit.randomize()
        self.snake.add_block()
        # update state fruit ate

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.fruit_ate = True
            self.fruit_ate()


    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            print("die1")
            #  hitting the wall
            # valid: [0, cell_number-1]
            self.end_game()
            # self.reset()
        else:
            if(self.snake.body.__len__()>=5):
                for block in self.snake.body[4:]:  # blocks after the head
                    if block == self.snake.body[0]:   #if a block's coords is the same as the head
                        print("die2")
                        # hitting itself
                        self.end_game()
                        # self.reset()





    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.snake.check_events(event)
                if event.type == self.SCREEN_UPDATE:
                    self.update()
                    print(self.snake.body)

            self.render()
            #pygame.display.update()
            # self.clock.tick(60)




            # limits FPS to 60
            # dt is delta time in seconds since last frame, used for framerate-
            # independent physics.
            # self.dt = self.clock.tick(60) / 1000


    def reset(self):
        # time.sleep(10000)
        self.snake.reset()
        self.fruit.reset()
        self.terminated = False



    def render(self):
        self.screen.fill((175, 215, 70))
        self.fruit.draw_fruit(self.screen)
        self.snake.draw_snake(self.screen)
        pygame.display.update()
    def end_game(self):
        # print("poi true")
        self.terminated = True

    def check_end(self):
        if self.terminated:
            self.reset()


class GameInherited(Game): # Inherited class
    terminated = False # new attribute

    def end_game(self):  # overloading end_game
        super().end_game()
        self.terminated = True

    def reset(self):  # overloading reset
        super().reset()
        self.terminated = False

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            print("die1")
            #  hitting the wall
            # valid: [0, cell_number-1]
            self.end_game()
            # self.reset()
        else:
            if(self.snake.body.__len__()>=5):
                for block in self.snake.body[4:]:  # blocks after the head
                    if block == self.snake.body[0]:   #if a block's coords is the same as the head
                        print("die2")
                        # hitting itself
                        self.end_game()
                        # self.reset()
#                         when training, the trainer call reset() automatically as long as we don't call
#                              it
if __name__ == "__main__":
    game = GameInherited()
    # game = Game()
    game.run()
