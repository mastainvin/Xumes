import logging
import math
import os
import string
import sys
from traceback import print_tb
import numpy as np
import random

import pygame
from games_examples.batkill.src.enemy_generation import random_bat

from games_examples.batkill.src.spriteful_player import Player
from games_examples.batkill.src.backend_player import MOVE_LEFT, MOVE_RIGHT, JUMP, ATTACK

#class Command():
#    def __init__(self, key_pressed: int):
#        self.key_pressed = key_pressed

#    def keyPressed(self) -> string:
#        return self.key_pressed

###

current_directory = os.path.dirname(__file__)

bat_sprite_path = os.path.join(current_directory, 'static', 'sprites', 'Bat')
background = os.path.join(current_directory, 'static', 'backgrounds', 'forest', 'background.png')
adventurer_sprites = os.path.join(current_directory, 'static', 'sprites', 'adventurer')

worldx = 928
worldy = 793
nb_bats = 2


class Game():


    def __init__(self, max_bats=nb_bats, bat_speed=6, attack_cooldown=10, jump=False) -> None:
        self.max_bats = max_bats
        self.bat_speed = bat_speed
        self.attack_cooldown = attack_cooldown
        self.jump = jump
        self.initialize_values()

    def initialize_values(self) -> None:

        pygame.init()
        pygame.font.init()

        self.deterministic_bats = False
        self.sorted_bats = {n: None for n in range(self.max_bats)}

        self.loop = 0

        self.fps = 30  # frame rate
        self.clock = pygame.time.Clock()

        self.world = pygame.display.set_mode([worldx, worldy])
        self.backdrop = pygame.image.load(background).convert()
        self.backdropbox = self.world.get_rect()
        self.player = Player(adventurer_sprites, self.attack_cooldown)  # spawn player        
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)

        self.score_font = pygame.font.SysFont(os.path.join('static', 'fonts', 'SourceCodePro-Medium.ttf'), 30)
        self.score_surface = self.score_font.render(f"SCORE: {round(self.player.sp.score * 1000)}, LIVES: {self.player.sp.lives}",
                                                    True, (0, 0, 0, 0))

        self.enemies = pygame.sprite.Group()
        self.running = True

        self.dt = 1

    def input(self):
        player_actions = []
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_actions.append(MOVE_LEFT)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_actions.append(MOVE_RIGHT)
        if self.jump:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_actions.append(JUMP)
        if keys[pygame.K_SPACE]:
            player_actions.append(ATTACK)
        return player_actions

    def run(self) -> None:

        while True:
            moving_towards = False
            attained_score = 0
            action = self.input()


            if action is None:
                action = []
            self.actions = action

            self.player.control(action, self.dt)

            if any([v is None for v in self.sorted_bats.values()]):
                new_bat = random_bat(current_score=self.player.sp.score, sprite_path=bat_sprite_path,
                                     base_speed=self.bat_speed)
                if new_bat:
                    for k, v in self.sorted_bats.items():
                        if v is None:
                            self.sorted_bats[k] = new_bat
                            self.player_list.add(new_bat)
                            self.enemies.add(new_bat)
                            break

            for idx, bat in self.sorted_bats.items():
                if bat is not None:
                    bat.update_state()
                    if bat.direction == -1:
                        if bat.rect.x < self.player.sp.rect.x:
                            moving_towards = True
                    else:
                        if bat.rect.x > self.player.sp.rect.x:
                            moving_towards = True

                    if self.player.sp.attack.attack_poly is not None and not bat.dying:
                        killed = self.player.sp.attack.attack_poly.rect.colliderect(bat.collider_rect)
                        if killed:
                            bat.die()
                            attained_score += 1
                    if bat.dead or bat.rect.x > worldx or bat.rect.x < 0:
                        self.enemies.remove(bat)
                        bat.kill()
                        self.sorted_bats[idx] = None
                        del bat
                    elif bat.collider_rect is not None and self.player.sp.collider_rect.colliderect(bat.collider_rect):
                        bat.die()
                        self.player.sp.lives -= 1

            self.player.sp.score += attained_score

            self.render(custom_message='Manual Play')

    def render(self, session=None, build=None, **kwargs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.running = False
                sys.exit()
        self.world.blit(self.backdrop, self.backdropbox)
        score_surface = self.score_font.render(f"BATS KILLED: {round(self.player.sp.score)}, LIVES: {self.player.sp.lives}",
                                               True, (0, 0, 0, 0))
        self.world.blit(score_surface, (10, 10))
        if session is not None:
            session_surface = self.score_font.render(str(session), True, (0, 0, 0, 0))
            self.world.blit(session_surface, (10, 30))
        if build is not None:
            build_surface = self.score_font.render(str(''.join(["build: ", build])), True, (0, 0, 0, 0))
            self.world.blit(build_surface, (10, 50))

        self.player.update()
        self.player_list.draw(self.world)
        self.player_list.draw(self.world)
        pygame.display.flip() #Update the full display Surface to the screen
        self.dt = self.clock.tick_busy_loop(self.fps)

    def reset(self):

        #pygame.event.clear()

        self.deterministic_bats = False
        self.sorted_bats = {n: None for n in range(self.max_bats)}

        self.loop = 0

        self.backdrop = pygame.image.load(background).convert()
        self.backdropbox = self.world.get_rect()
        self.player = Player(adventurer_sprites, self.attack_cooldown)  # spawn player
        self.player_list = pygame.sprite.Group()
        self.player_list.add(self.player)
        self.enemies = pygame.sprite.Group()
        self.running = True


if __name__ == "__main__":
    game = Game(max_bats=nb_bats, bat_speed=6, attack_cooldown=10, jump=True)
    game.run()
