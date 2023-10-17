import random
import numpy as np
import pygame

from games_examples.connected_new.objects import Tiles, Coins, WIDTH, HEIGHT

CENTER = WIDTH // 2, HEIGHT // 2
RADIUS = 70
SPEED = 2
SCREEN  =WIDTH,HEIGHT
class PipeGenerator:

    def __init__(self, game=None,win=None):
        self.pipes = []
        self.game = game
        self.time_between = (CENTER[0]) / SPEED
        self.time_spent = 0
        self.next = 0 #0->the next is coin.py, 1-> the next is tile
        self.win = win
    def reset(self):
        self.pipes = []
        self.time_spent = 0

    # def reset_random(self):
    #     number_of_pipes = WIDTH // (SPACE_BETWEEN_PIPES + PIPE_WIDTH)
    #     self.pipes = []
    #     start_position = np.random.uniform(LEFT_POSITION, WIDTH / 3)
    #     for i in range(number_of_pipes):
    #         self.pipes.append(
    #             Pipe(self.game.player, self, position=start_position + i * (PIPE_WIDTH + SPACE_BETWEEN_PIPES),
    #                  height=random.randint(50, HEIGHT - 50 - PIPE_SPACE)))

    def gen_tile(self):
        # Create a pipe with random height
        # TODO make an easy way to change how we compute the height (random or not)
        # if WIDTH >= HEIGHT:
        #     win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
        # else:
        #     win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
        self.next=0
        return Tiles(random.choice([CENTER[1] - 80,CENTER[1],CENTER[1] + 80]),
                                              random.randint(1, 3),
                                              self.win)
    def gen_coin(self):
        # Create a pipe with random height
        # TODO make an easy way to change how we compute the height (random or not)
        # if WIDTH >= HEIGHT:
        #     win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
        # else:
        #     win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)
        self.next=1
        return Coins(random.randint(CENTER[1] - RADIUS,CENTER[1] + RADIUS),
                                                 self.win)

    def generator(self, dt):
        self.time_spent += dt
        # We wait enough time and create a new pipe
        if self.pipes:
            if WIDTH - self.pipes[-1].x + 100 > WIDTH/2 and self.next==1:
                self.time_spent = 0
                self.pipes.append(self.gen_tile())
            elif WIDTH - self.pipes[-1].x + 100 > WIDTH/2 and self.next==0:
                self.time_spent = 0
                self.pipes.append(self.gen_coin())
        else:
            self.pipes.append(self.gen_coin())

    def move(self):
        pipes_to_delete = []
        for pipe in self.pipes:
            pipe.update()
            # if the pipe is out screen we delete him
            if pipe.x < -100:
                pipes_to_delete.append(pipe)
        for pipe in pipes_to_delete:
            self.pipes.remove(pipe)

    def draw(self, canvas):
        for pipe in self.pipes:
            pipe.draw(canvas)

    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 14)
        text_surface = my_font.render(f'pipes: {len(self.pipes)}', False, (0, 0, 0))
        canvas.blit(text_surface, (0, 20))

    def end(self):
        self.game.end_game()
