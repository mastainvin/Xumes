import random
import numpy as np
import pygame
import pygame
import random
import math
from games_examples.connected.src.tile import Tiles
from games_examples.connected.src.ball import Balls
from games_examples.connected.src.coin import Coins

from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
pygame.font.init()
pygame.mixer.init()


class Generator:

    def __init__(self, game=None, pattern=random.randint(1,7)):
        self.pipes = []
        self.game = game
        self.time_between = (SPACE_BETWEEN) / SPEED
        self.time_spent = 0
        self.win=self.game.win
        self.next_is_coin=True
        self.terminate_after_generation=False
        self.pattern = pattern
        self.count=0
    def reset(self):
        self.pipes = []
        self.time_spent = 0
        self.next_is_coin = True
        self.pattern=random.randint(1,7)
        self.terminate_after_generation = False
        self.count = 0

    def gen_coin(self,y):
        # Create a pipe with random height
        # TODO make an easy way to change how we compute the height (random or not)
        # if self.next_is_coin == True:
        self.next_is_coin = False
        return Coins(y,self.game.ball,self)


    def gen_tile(self,y,type):
        # Create a pipe with random height
        # TODO make an easy way to change how we compute the height (random or not)
        self.next_is_coin = True
        return Tiles(y,type,self.game.ball,self)

    def generator(self, dt):
        self.time_spent += dt

        # print(self.pipes,"self.pipes")
        # We wait enough time and create a new pipe
        is_the_second_coin= False
        auto_addition = False

        # if there is already a pipe on the screen
        if self.count==0 and self.time_spent*SPEED>=WIDTH-50:
            if self.pattern == 1:
                self.pipes.append(self.gen_coin(CENTER[1] + 40))
            elif self.pattern == 2:
                self.pipes.append(self.gen_coin(CENTER[1] + 40))
            elif self.pattern == 3:
                self.pipes.append(self.gen_coin(CENTER[1] - 40))
            elif self.pattern == 4:
                self.pipes.append(self.gen_coin(CENTER[1] - 40))
            elif self.pattern == 5:
                self.pipes.append(self.gen_coin(CENTER[1] - 40))
            elif self.pattern == 6:
                self.pipes.append(self.gen_coin(CENTER[1]))
            elif self.pattern == 7:
                self.pipes.append(self.gen_coin(CENTER[1]))
            self.count+=1
            self.time_spent=0

        if self.count==1 and self.time_spent*SPEED>=WIDTH-50:
            if self.pattern == 1:
                self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            elif self.pattern == 2:
                self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            elif self.pattern == 3:
                self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            elif self.pattern == 4:
                self.pipes.append(self.gen_tile(CENTER[1], 1))
            elif self.pattern == 5:
                self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            elif self.pattern == 6:
                self.pipes.append(self.gen_tile(CENTER[1] - 40, 1))
            elif self.pattern == 7:
                self.pipes.append(self.gen_tile(CENTER[1], 1))
            self.count+=1
            self.time_spent = 0

        if self.count==2 and self.time_spent*SPEED>=WIDTH-50:
            if self.pattern == 1:
                self.pipes.append(self.gen_coin(CENTER[1] + 40))
            elif self.pattern == 2:
                self.pipes.append(self.gen_coin(CENTER[1] - 40))
            elif self.pattern == 3:
                self.pipes.append(self.gen_coin(CENTER[1] + 40))
            elif self.pattern == 4:
                self.pipes.append(self.gen_coin(CENTER[1] + 40))
            elif self.pattern == 5:
                self.pipes.append(self.gen_coin(CENTER[1]))
            elif self.pattern == 6:
                self.pipes.append(self.gen_coin(CENTER[1] + 40))
            elif self.pattern == 7:
                self.pipes.append(self.gen_coin(CENTER[1]))
            self.time_spent = 0
            self.count += 1
            self.terminate_after_generation = True
        if self.terminate_after_generation and self.time_spent*SPEED>=WIDTH-50:
            self.time_spent = 0
            self.count=0
            self.game.terminated = True



        # if self.pipes:
        #     print(self.pipes,"self.pipes1")
        #     if WIDTH - self.pipes[-1].x+self.pipes[-1].width/2 + 100 > SPACE_BETWEEN*2:
        #         self.time_spent = 0
        #         if self.next_is_coin == True:
        #
        #             # self.pipes.append(self.gen_coin(random.randint(CENTER[1]-50,CENTER[1],CENTER[1]+50)))
        #             # self.next_is_coin = False
        #
        #         else:
        #             if self.terminate_after_generation:
        #
        #
        #
        #             # self.pipes.append(self.gen_tile(random.randint(CENTER[1]-40,CENTER[1],CENTER[1]+40), 1))
        #             self.next_is_coin = True
        # else:
        #     print(self.pipes,self.next_is_coin,"self.pipes2")
        #     if self.next_is_coin:
        #
        #         # self.pipes.append(self.gen_coin(random.randint(CENTER[1]-50,CENTER[1]+50)))
        #         self.next_is_coin =False


            # else:
            #     if self.pattern == 1:
            #         self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            #     elif self.pattern == 2:
            #         self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            #     elif self.pattern == 3:
            #         self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            #     elif self.pattern == 4:
            #         self.pipes.append(self.gen_tile(CENTER[1], 1))
            #     elif self.pattern == 5:
            #         self.pipes.append(self.gen_tile(CENTER[1] + 40, 1))
            #     elif self.pattern == 6:
            #         self.pipes.append(self.gen_tile(CENTER[1] - 40, 1))
            #     elif self.pattern == 7:
            #         self.pipes.append(self.gen_tile(CENTER[1], 1))
            #     self.next_is_coin = True


    def move(self, dt):
        pipes_to_delete = []
        for pipe in self.pipes:
            pipe.update(dt)
            # if the pipe is out screen we delete him
            if pipe.x < -100:
                pipes_to_delete.append(pipe)
        # for pipe in pipes_to_delete:
        #     self.pipes.remove(pipe)

    def draw(self,win):
        for pipe in self.pipes:
            pipe.draw(win)

    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'pipes: {len(self.pipes)}', False, (0, 0, 0))
        canvas.blit(text_surface, (0, 20))

    def end(self):
        self.game.end_game()
