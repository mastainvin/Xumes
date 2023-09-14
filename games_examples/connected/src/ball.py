import pygame
import random
import math


from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
pygame.font.init()
pygame.mixer.init()


class Balls:
    points = 0
    def __init__(self,y=CENTER[1],game=None):
        self.initial_pos = (CENTER[0] - 50, y)
        self.radius = 0
        self.accumulation = 0  # accumulation  used to be  angle
        self.reset()
        self.score = 0
        self.highscore = 0
        self.dtheta = 0
        self.rect = pygame.Rect (self.x - 6, self.y - 6, 12, 12)

        self.game=game
        self.x=CENTER[0] - 50
        self.y=y
        self.center=(self.x,self.y)


    def update(self,dt):
        # print("called update--ball")
        # x = round(CENTER[0] + self.radius * math.cos(self.angle * math.pi / 180))

        # y = round(CENTER[1] + self.radius * math.sin(self.angle * math.pi / 180))
        # if CENTER[1]-70<(self.accumulation + self.dtheta)<CENTER[1]+70:


        # print(self.x,self.y,self.rect.top,self.rect.bottom,self.rect.left,self.rect.right)
        if self.y  >= CENTER[1] + 66 and self.dtheta > 0:
            self.dtheta = 0
        elif self.y  <= CENTER[1] - 66 and self.dtheta < 0:
            self.dtheta = 0
        self.x = CENTER[0] - 50
        self.y += dt*SPEED*self.dtheta
        # self.rect.y+=dt*SPEED*self.dtheta
        self.center=(self.x,self.y)
        self.step += 1
        if self.step % 5 == 0:
            self.pos_list.append((self.x, self.y))
        if len(self.pos_list) > 5:
            self.pos_list.pop(0)

        # self.rect = pygame.draw.circle(self.win, color, (x, y), 6)

        # for index, pos in enumerate(self.pos_list):
        #     if index < 3:
        #         radius = 1
        #     else:
        #         radius = 2
        #     pygame.draw.circle(self.win, color, pos, radius)

    # def update_score(self, score):
    #     self.score = score
    #     print(self.score)

    # def update_highscore(self, highscore):
    #     self.highscore = highscore
    #     print(self.highscore)

    def reset(self):
        self.x, self.y = self.initial_pos
        self.angle = 0
        self.dtheta = 0
        self.points = 0
        self.pos_list = []
        self.step = 0
        self.center=(self.x,self.y)

    def change_direction(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.up()
        elif keys[pygame.K_DOWN]:
            self.down()

    def up(self):
        if self.y <= CENTER[1] - 66:
            self.dtheta = 0
        else:
            self.dtheta =-2
    def down(self):
        if self.y  >= CENTER[1] + 66 :
            self.dtheta = 0
        else :
            self.dtheta = 2
        # print(self.dtheta,self.x,self.y,"ball coordinates")
        # if not CENTER[1]-70<(self.y)<CENTER[1]+70:
        #     self.dtheta=0





    def logs(self, canvas):
        my_font = pygame.font.SysFont('Arial', 28)
        text_surface = my_font.render(f'points: {self.points} ',
                                      False, (0, 0, 0))
        canvas.blit(text_surface, (0, 0))

    def gain_point(self):
        self.points += 1
        self.reward = True
    # USE DRAW() TO RENDER THE BALL
    def draw(self,win):
        pygame.draw.rect(win, "yellow", (self.x-6, self.y-6,12,12))




class Particle:
    def __init__(self, x, y, color, win):
        super(Particle, self).__init__()
        self.x = x
        self.y = y
        self.color = color
        self.win = win
        self.size = random.randint(4, 7)
        xr = (-3, 3)
        yr = (-3, 3)
        f = 2
        self.life = 40
        self.x_vel = random.randrange(xr[0], xr[1]) * f
        self.y_vel = random.randrange(yr[0], yr[1]) * f
        self.lifetime = 0

    def update(self):
        self.size -= 0.1
        self.lifetime += 1
        if self.lifetime <= self.life:
            self.x += self.x_vel
            self.y += self.y_vel
            s = int(self.size)
            pygame.draw.rect(self.win, self.color, (self.x, self.y, s, s))
        else:
            self.kill()



#
# class Button(pygame.sprite.Sprite):
#     def __init__(self, img, scale, x, y):
#         super(Button, self).__init__()
#
#         self.scale = scale
#         self.image = pygame.transform.scale(img, self.scale)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#         self.clicked = False
#
#     def update_image(self, img):
#         self.image = pygame.transform.scale(img, self.scale)
#
#     def draw(self, win):
#         action = False
#         pos = pygame.mouse.get_pos()
#         if self.rect.collidepoint(pos):
#             if pygame.mouse.get_pressed()[0] and not self.clicked:
#                 action = True
#                 self.clicked = True
#
#             if not pygame.mouse.get_pressed()[0]:
#                 self.clicked = False
#
#         win.blit(self.image, self.rect)
#         return action