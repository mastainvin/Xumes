import sys
import logging
import time

import pygame

from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.play import Game
from games_examples.dont_touch.src.services.music_service import MusicService
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import is_close_app_event, update_background_using_scroll
from games_examples.dont_touch.src.components.hand_side import HandSide

from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State


class DontTouchTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["end_game", "reset"]))

        def get_pos(pos):
            return [pos[0], pos[1]]

        self.game.P1 = self.bind(Player(), name="player", state=[
            State("player_position", func=get_pos, methods_to_observe="update"),
        ])
        self.game.H1 = self.bind(Hand(HandSide.RIGHT), name="right_hand", state=[
            State("new_x", methods_to_observe="move"),
            State("new_y", methods_to_observe="move"),
            State("new_spd", methods_to_observe="move")
        ])
        self.game.H2 = self.bind(Hand(HandSide.LEFT), name="left_hand", state=[
            State("new_x", methods_to_observe="move"),
            State("new_y", methods_to_observe="move"),
            State("new_spd", methods_to_observe="move")
        ])
        self.game.scoreboard = self.bind(Scoreboard(), name="scoreboard", state=[
            State("_current_score", methods_to_observe="increase_current_score"),
            State("_max_score", methods_to_observe="update_max_score")
        ])

        self.game.hands = pygame.sprite.Group()
        self.game.hands.add(self.game.H1)
        self.game.hands.add(self.game.H2)
        self.game.all_sprites = pygame.sprite.Group()
        self.game.all_sprites.add(self.game.P1)
        self.game.all_sprites.add(self.game.H1)
        self.game.all_sprites.add(self.game.H2)

    def run_test(self) -> None:

        while self.game.running:

            self.test_client.wait()
            events = pygame.event.get()

            for event in events:
                if is_close_app_event(event):
                    self.game.running = False
                if event.type == pygame.KEYDOWN:
                    self.game.P1.update_state(event)

            self.game.H1.move(self.game.scoreboard, self.game.P1.player_position)
            self.game.H2.move(self.game.scoreboard, self.game.P1.player_position)

            if pygame.sprite.spritecollide(self.game.P1, self.game.hands, False, pygame.sprite.collide_mask):
                print("Collision")
                self.game.scoreboard.update_max_score()
                self.game.end_game()
                time.sleep(0.5)

            #self.game.check_end()

            self.game.dt = 0.09

    def run_test_render(self) -> None:

        while self.game.running:
            self.test_client.wait()

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self.game.terminated = True
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.game.P1.update_state(event)

            self.game.H1.move(self.game.scoreboard, self.game.P1.player_position)
            self.game.H2.move(self.game.scoreboard, self.game.P1.player_position)

            if pygame.sprite.spritecollide(self.game.P1, self.game.hands, False, pygame.sprite.collide_mask):
                self.game.scoreboard.update_max_score()
                self.game.end_game()
                time.sleep(0.5)

            self.game.render()

    def reset(self) -> None:
        self.game.reset()

    def random_reset(self) -> None:
        self.reset()

    def delete_screen(self) -> None:
        pass

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-test":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        if sys.argv[1] == "-render":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        game_service = GameService(test_runner=DontTouchTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()
