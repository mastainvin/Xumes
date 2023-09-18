import pygame
import random
import math


from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
pygame.font.init()
pygame.mixer.init()


class Tiles:
    def __init__(self, y,type_,\
                 ball=None, generator=None, ):
        super(Tiles, self).__init__()
        self.ball=ball
        self.generator=generator

        self.player_passed=False

        self.x = WIDTH + 10
        self.y = y
        self.type = type_
        self.kind='tile'
        self.angle = 0
        self.dtheta = 0
        # self.dx = -2

        self.height = 0
        self.width = 0

        if self.type == 1:
            self.width = 50
            self.height = 20
            self.h = 20
        elif self.type == 2:
            self.width = 20
            self.height = 50
            self.h = 50
        elif self.type == 3:
            self.width = 50
            self.height = 50
            self.h = 50

        # self.dtheta = 2


        self.rect = pygame.Rect(self.x-self.width/2,self.y- self.height/2,self.width,self.height)

    # def rotate(self):
    #     image = pygame.transform.rotozoom(self.image, self.angle, 1)
    #     rect = image.get_rect(center=self.rect.center)
    #
    #     return image, rect




    def update(self, dt):
        self.kind = 'tile'
        self.x -= dt*SPEED
        self.rect.move(-dt * SPEED, 0)
        # if self.x < 20:
            # self.kill()
        self.rect = pygame.Rect(self.x-self.width/2,self.y- self.height/2,self.width,self.height)
        if not self.collision():
            # Check if player passed the pipe (win one point)
            self.is_player_passed()
    # def draw(self, canvas):
    #     pygame.draw.rect(self.win, (200, 200, 200), (self.x + self.s, self.y + self.s, self.size, self.size))
    #     pygame.draw.rect(self.win, "aqua", (self.x, self.y, self.size, self.size))
    #     pygame.draw.circle(self.win, (255, 255, 255), self.rect.center, 2)


    def is_player_passed(self):
        # if the mid point of the pipe passes the x coordinate of the player
        if self.x +  self.width/ 2 < 88\
                and not self.player_passed:
            self.player_passed = True
            self.generator.pipes.remove(self)
            self.ball.gain_point_avoid()


    def collision(self):
        # if the pipe collides we stop the game
        if (
                # player's x coordinate is between the width of the pipe
                94+6>= self.x-round(self.width/2)  and self.x+round(self.width/2)>=94-6) and (
                # player's y coordinate touches one edge of the pipe
                self.ball.y-6 < self.y + round(self.height/2) and \
                self.ball.y + 6 > self.y - round(self.height/2)):
            self.generator.pipes.remove(self)
            self.generator.end()
            return True
        return False

    def draw(self,win):
        left=int(self.x-int(self.width/2))
        top=int(self.y- int(self.height/2))
        pygame.draw.rect(win,"red",(self.x-int(self.width/2),self.y- int(self.height/2),self.width,self.height))

