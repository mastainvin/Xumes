import pygame
import random
import math

from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
pygame.font.init()
pygame.mixer.init()
class Coins:
    def __init__(self, y,\
                 # newly added:
                 ball=None, generator=None):
        super(Coins, self).__init__()
        self.kind='coin'
        self.y = y
        self.size = 16
        self.width = 16
        self.height = 16
        self.ball = ball
        self.generator=generator
        self.x = WIDTH+20
        self.dx = -1
        self.s = 1
        self.player_passed=False
        self.rect = pygame.Rect((self.x-8, self.y-8, self.width, self.height))
        self.h=16
        # print("generated coin", self.x,self.y)

    def update(self, dt):
        self.kind = 'coin'
        self.x -= dt*SPEED
        self.rect.move(-dt*SPEED, 0)

        # if self.x < 20:
            # self.kill()
        self.rect = pygame.Rect(self.x-8, self.y-8, self.width, self.height)
        if not self.collision():
            # Check if player passed the pipe (win one point)
            self.is_player_passed()
    # def draw(self, canvas):
    #     pygame.draw.rect(self.win, (200, 200, 200), (self.x + self.s, self.y + self.s, self.size, self.size))
    #     pygame.draw.rect(self.win, "aqua", (self.x, self.y, self.size, self.size))
    #     pygame.draw.circle(self.win, (255, 255, 255), self.rect.center, 2)


    def is_player_passed(self):
        # if the mid point of the pipe passes the x coordinate of the player
        if self.x +  self.size/ 2 < 88\
                and not self.player_passed:
            self.player_passed = True
            self.ball.penalize()
            self.generator.pipes.remove(self)


    def collision(self):
        # if the pipe collides we stop the game
        if (
                # player's x coordinate is between the width of the pipe
                #       100                                           88-
                94+6>= self.x-round(self.width/2)  and self.x+round(self.width/2)>=94-6) and (
                # player's y coordinate touches one edge of the pipe
                self.ball.y - 6 < self.y + round(self.height/2) and \
                self.ball.y + 6 > self.y - round(self.height/2)):
            print(self.rect.left)
            # self.generator.end()
            self.ball.gain_point()
            self.generator.pipes.remove(self)
            return True
        return False

    def draw(self,win):
        pygame.draw.rect(win,"purple",(self.x-8, self.y-8, self.width, self.height))
