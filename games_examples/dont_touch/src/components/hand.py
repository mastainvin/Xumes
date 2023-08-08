import random

import pygame

from games_examples.dont_touch.src.components.hand_side import HandSide
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import sine


class Hand(pygame.sprite.Sprite):
    def __init__(self, hand_side: HandSide, offset_x: int, speed: float, random_hand: bool):
        super().__init__()
        if random_hand is True:
            self.new_spd = random.uniform(2.5, 3)
            self.offset_x = 0
        self.new_spd = speed
        self.new_y = 0
        #self.hand_side = 0
        self.offset_x = offset_x #0
        self.random_hand = random_hand
        self.new_x = sine(100.0, 1280, 20.0, self.offset_x)
        self.side = hand_side
        self.can_score = True #When a hand is above the player, the player can score
        self.move_counter = 0
        self.SPEED_HANDS = 0.016
        self._load_hand()

    def reset(self):
        if self.random_hand is True:
            self.new_spd = random.uniform(2.5, 3)
        self.can_score = True

        if self.side == HandSide.RIGHT:
            if self.random_hand is True:
                self.offset_x = random.randint(260, 380)
            self.new_y = -40
            self.new_x = 0

        if self.side == HandSide.LEFT:
            if self.random_hand is True:
                self.offset_x = random.randint(-50, 120)
            self.new_y = -320
            self.new_x = 0

    def _load_hand(self):
        if self.side == HandSide.RIGHT:
            self.hand_side = 1
            self._load_right_hand()

        if self.side == HandSide.LEFT:
            self.hand_side = 0
            self._load_left_hand()

    def _load_left_hand(self):

        self.image = VisualizationService.get_left_hand_image()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if self.random_hand is True:
            self.offset_x = random.randint(-50, 120)
        self.new_y = -320

    def _load_right_hand(self):
        self.image = VisualizationService.get_right_hand_image()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        if self.random_hand is True:
            self.offset_x = random.randint(260, 380)
        self.new_y = -40

    def move(self, scoreboard: Scoreboard, player_position, dt):
        self.move_counter += dt
        if self.move_counter > 0.016:
            self.new_x = sine(100.0, 620, 20.0, self.offset_x)
            self.new_y += self.new_spd
            self.rect.center = (self.new_x, self.new_y)

            if self.rect.top > player_position.y - 35 and self.can_score:
                # On marque un point quand le bas de la main player à passer le haut de la main obstacle
                scoreboard.increase_current_score()
                self.can_score = False

            if self.rect.top > Config.HEIGHT:
                self.rect.bottom = 0
                # Play Kung Fu Sound
                if self.random_hand is True:
                    self.new_spd = random.uniform(0.5, 8)

                if self.side == HandSide.RIGHT:
                    if self.random_hand is True:
                        self.offset_x = random.randint(260, 380)
                    self.new_y = -40

                if self.side == HandSide.LEFT:
                    if self.random_hand is True:
                        self.offset_x = random.randint(-50, 120)
                    self.new_y = -320

                if self.new_spd >= 6:
                    self.new_spd = 8
                    MusicService.play_chop_sound()

                self.can_score = True
            self.move_counter = 0

    def draw(self, screen):
        dotted_line = VisualizationService.get_dotted_line()
        screen.blit(dotted_line, (0, self.rect.y + 53))
        screen.blit(self.image, self.rect)
