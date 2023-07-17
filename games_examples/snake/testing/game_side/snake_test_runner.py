import sys
import logging
import time


import pygame
from pygame import Vector2


from games_examples.snake.play import Main
from games_examples.snake.src.fruit import Fruit
from games_examples.snake.src.snake import Snake


from xumes.game_module import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State

cell_size = 30
cell_number = 15
class SnakeTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Main()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["game_over"]))
    #     newly added
    #     todo:methods是否需要增加add_block
        self.game.snake = self.bind(Snake(), name="snake", state=[
            State("body", methods_to_observe="move_snake"),
            State("direction", methods_to_observe="move_snake"),
            State("new_block", methods_to_observe="move_snake")
        ])
        self.game.fruit = self.bind(Fruit(), name="fruit", state=[
            State("pos", methods_to_observe="randomize"),

        ])
        self.game.all_sprites = pygame.sprite.Group()
        self.game.all_sprites.add(self.game.snake)
        self.game.all_sprites.add(self.game.fruit)

    def fruit_ate(self):
        super().fruit_ate()
        self.update_state("fruit_ate")

    def game_over(self):
        self.update_state("lose")

    def run_test(self) -> None:
        while self.game.running:
            self.test_client.wait()
            for event in pygame.event.get():
                self.check_events(event)
            self.update()
            self.clock.tick(0)

    def run_test_render(self) -> None:
        # self.game.run()
        while self.game.running:
            self.test_client.wait()
            for event in pygame.event.get():
                self.check_events(event)
            self.update()
            self.screen.fill((175, 215, 70))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(8)



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

        game_service = GameService(test_runner=SnakeTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.run()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Main()
        game.run()
