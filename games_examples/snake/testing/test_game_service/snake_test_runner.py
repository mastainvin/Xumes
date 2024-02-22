import random
import sys
from abc import ABC

import pygame
from pygame import Vector2

from src.xumes import GameService
from src.xumes import JsonGameStateObserver
from src.xumes import \
    CommunicationServiceGameMq
from src.xumes import PygameEventFactory
from src.xumes import JsonTestRunner
from games_examples.snake.play import Main
from games_examples.snake.src.fruit import cell_number
from games_examples.snake.testing.test_game_service.snake_observables import SnakeObservable, FruitObservable


class MainTestRunner(Main, JsonTestRunner, ABC):

    def __init__(self, observers):
        Main.__init__(self)
        JsonTestRunner.__init__(self, game_loop_object=self, observers=observers)

        self.snake = SnakeObservable(observers, "snake")
        self.fruit = FruitObservable(observers, "fruit")

    def fruit_ate(self):
        super().fruit_ate()
        self.update_state("fruit_ate")

    def game_over(self):
        self.update_state("lose")

    def run_test(self) -> None:
        while True:
            self.test_client.loop()
            for event in pygame.event.get():
                self.check_events(event)
            self.update()
            self.clock.tick(0)

    def run_test_render(self) -> None:
        while True:
            self.test_client.loop()
            for event in pygame.event.get():
                self.check_events(event)
            self.update()
            self.screen.fill((175, 215, 70))
            self.draw_elements()
            pygame.display.update()
            self.clock.tick(8)

    def random_reset(self) -> None:
        self.snake.detach_all()
        self.fruit.detach_all()

        self.snake = SnakeObservable(self.observers, "snake")
        self.fruit = FruitObservable(self.observers, "fruit")

        start_x = random.randint(0, cell_number - 1)
        start_y = random.randint(0, cell_number - 1)

        self.snake.body.clear()
        self.snake.body.append(Vector2(start_x, start_y))
        tail_x, tail_y = start_x, start_y
        for i in range(random.randint(2, 6)):
            possibilities = []
            if tail_x - 1 >= 0 and Vector2(tail_x - 1, tail_y) not in self.snake.body:
                possibilities.append((tail_x - 1, tail_y))
            if tail_x + 1 < cell_number and Vector2(tail_x + 1, tail_y) not in self.snake.body:
                possibilities.append((tail_x + 1, tail_y))
            if tail_y - 1 >= 0 and Vector2(tail_x, tail_y - 1) not in self.snake.body:
                possibilities.append((tail_x, tail_y - 1))
            if tail_y + 1 < cell_number and Vector2(tail_x, tail_y + 1) not in self.snake.body:
                possibilities.append((tail_x, tail_y + 1))
            if possibilities:
                tail_x, tail_y = random.choice(possibilities)
            else:
                break
            if i == 0:
                d_x, d_y = start_x - tail_x, start_y - tail_y
                self.snake.direction = Vector2(d_x, d_y)
            self.snake.body.append(Vector2(tail_x, tail_y))

        self.snake.notify()

    def reset(self) -> None:
        self.snake.detach_all()
        self.fruit.detach_all()

        self.snake = SnakeObservable(self.observers, "snake")
        self.fruit = FruitObservable(self.observers, "fruit")

    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) == 2:
        game_service = GameService(observer=JsonGameStateObserver.get_instance(),
                                   test_runner=MainTestRunner(observers=[JsonGameStateObserver.get_instance()]),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-tests":
            game_service.run_communication_service()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Main()
        game.run()
