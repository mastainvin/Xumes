import sys
import time
import numpy as np
import pygame

from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.hand_side import HandSide
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import update_background_using_scroll, update_press_key, \
                                                      is_close_app_event

from games_examples.dont_touch.src.components.game_status import GameStatus


class Game:
    terminated = False

    def __init__(self):

        pygame.init()

        self.FramePerSec = pygame.time.Clock()

        GlobalState.load_main_screen()
        #VisualizationService.load_main_game_displays()

        self.running = True
        self.scoreboard = Scoreboard()

        # Sprite Setup
        self.P1 = Player()
        self.H1 = Hand(HandSide.LEFT, offset_x=0, speed=3, random_hand=False)
        self.H1.offset_x = 119
        #self.H1 = None
        #self.H2 = Hand(HandSide.RIGHT, offset_x=280, speed=3, random_hand=False)
        self.H2 = None

        # Sprite Groups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.P1)
        self.hands = pygame.sprite.Group()
        if self.H1 is not None:
            self.hands.add(self.H1)
        if self.H2 is not None:
            self.hands.add(self.H2)
        if self.H1 is not None:
            self.all_sprites.add(self.H1)
        if self.H2 is not None:
            self.all_sprites.add(self.H2)

        self.dt = 0

        GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
        VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)
        #GlobalState.PRESS_Y = update_press_key(GlobalState.PRESS_Y)
        #VisualizationService.draw_main_menu(GlobalState.SCREEN, self.scoreboard.get_max_score(), GlobalState.PRESS_Y)

        #pygame.display.update()

    def run(self):

        while self.running:

            #self.render()
            events = pygame.event.get()

            for event in events:
                if is_close_app_event(event):
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    self.P1.update(event, self.dt)
            if self.H1 is not None:
                self.H1.move(self.scoreboard, self.P1.player_position, self.dt)
            if self.H2 is not None:
                self.H2.move(self.scoreboard, self.P1.player_position, self.dt)

            self.render()

            #print("----------------- DISTANCE TO RIGHT HAND -----------------\n", np.abs(self.P1.player_position[1] - self.H2.new_y))
            #print("----------------- DISTANCE TO LEFT HAND -----------------\n", np.abs(self.P1.player_position[1] - self.H1.new_y))
            #print("----------------- PLAYER - HAND -----------------\n", self.P1.pos[0] - self.H2.new_x)

            if pygame.sprite.spritecollide(self.P1, self.hands, False, pygame.sprite.collide_mask):
                self.scoreboard.update_max_score()
                self.end_game()
                time.sleep(0.5)

            self.check_end()

            self.dt = self.FramePerSec.tick(Config.FPS) / 1000


    def render(self):

        GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
        VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)

        if self.P1 is not None:
            self.P1.draw(GlobalState.SCREEN)
        if self.H1 is not None:
            self.H1.draw(GlobalState.SCREEN)
        if self.H2 is not None:
            self.H2.draw(GlobalState.SCREEN)
        self.scoreboard.draw(GlobalState.SCREEN)

        pygame.display.update()

        self.dt = self.FramePerSec.tick(Config.FPS) / 1000

    def check_end(self):
        if self.terminated:
            self.reset()

    def end_game(self):
        self.terminated = True

    def reset(self):
        self.scoreboard.reset_current_score()
        self.P1.reset()
        if self.H1 is not None:
            self.H1.reset()
        if self.H2 is not None:
            self.H2.reset()
        self.FramePerSec = pygame.time.Clock()
        self.terminated = False
        # time.sleep(0.5)


if __name__ == "__main__":
    game = Game()
    game.run()
