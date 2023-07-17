import random
import sys
import logging

import pygame
from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State

from games_examples.connected.main import Game
from games_examples.connected.objects import Balls, Coins, Tiles, Particle, CENTER


class ConnectedTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game = self.bind(self.game, "game", state=[
            State("terminated",[State("score"),State("highscore")], methods_to_observe=["update", "reset"]),
            State("ball",[State( "score" ), State( "highscore" ), State("rect", [State( "x" ), State( "y" )])], methods_to_observe="update"),
            State("coin", [State("x"), State("y")], methods_to_observe="update"),
            State("t", [State("x"), State("y"),  State("type") ], methods_to_observe="update")

            ])

        self.game.all_sprites = pygame.sprite.Group()


    def run_test(self) -> None:

        while self.game.running:
            self.test_client.wait()
            self.game.update()



    def run_test_render(self) -> None:

        while self.game.running:
            self.test_client.wait()
            self.game.update()

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
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

        game_service = GameService(test_runner=ConnectedTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game()
        game.run()

