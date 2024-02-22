import logging
import sys

import pygame

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game

from xumes.test_runner import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State

class SuperMarioTestRunner(TestRunner):

    def get_rect(self, rect):
        return [rect.x, rect.y]

    def get_attributes(self, lst):
        return [{
            'name': item.__name__,
            'type': item.type,
            'position': {
                'x': item.rect.x,
                'y': item.rect.y
            },
            'alive': item.alive,
            'active': item.active,
            'bouncing': item.boucing,
            'onGround': item.onGround
        } for item in lst]

    def __init__(self, levelname, feature):
        super().__init__()
        self.game = Game(levelname, feature)
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["run", "reset"]))

        self.entities = ["Coin", "CoinBox", "CoinBrick", "EntityBase", "Goomba", "Item", "Koopa", "Mushroom", "RandomBox"]
        self.game.mario = self.bind(Mario(0, 0, self.game.level, self.game.screen, self.game.dashboard, self.game.sound), "mario", state=[
            State("rect", func=self.get_rect, methods_to_observe="move"),
            State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
            State("ending_level", methods_to_observe="end_level"),
            State("levelObj", State("entityList", [State(entity, func=self.get_attributes) for entity in self.entities]),
                  methods_to_observe=["_onCollisionWithItem", "_onCollisionWithMob"]),
            State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                      "_onCollisionWithBlock",
                                                                                      "killEntity",
                                                                                      "_onCollisionWithItem"])
        ])

    def run_test(self) -> None:

        while True:

            self.test_client.loop()
            self.game.level.drawLevel(self.game.mario.camera)
            self.game.dashboard.update()
            self.game.mario.update()

            if self.game.mario.restart or self.game.mario.ending_level:
                self.game.end_game()

            #self.game.check_end()

            self.game.render()

            #if self.game.mario.restart or self.game.mario.end_level:
            #    self.game.terminated = True
        #    self.game.reset()

    def run_test_render(self) -> None:

        while not self.game.mario.restart:

            self.test_client.loop()
            self.game.level.drawLevel(self.game.mario.camera)
            self.game.dashboard.update()
            self.game.mario.update()

            if self.game.mario.restart or self.game.mario.ending_level:
                self.game.end_game()

            self.game.render()

    def reset(self) -> None:
        self.game.reset(None)
        print(self.game.mario.rect)
        self.game.mario = self.bind(
            Mario(0, 0, self.game.level, self.game.screen, self.game.dashboard, self.game.sound), "mario", state=[
                State("rect", func=self.get_rect, methods_to_observe="move"),
                State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
                State("ending_level", methods_to_observe="end_level"),
                State("levelObj",
                      State("entityList", [State(entity, func=self.get_attributes) for entity in self.entities]),
                      methods_to_observe=["_onCollisionWithItem", "_onCollisionWithMob"]),
                State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                          "_onCollisionWithBlock",
                                                                                          "killEntity",
                                                                                          "_onCollisionWithItem"])
            ])

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

        game_service = GameService(test_runner=SuperMarioTestRunner("Level1-2", None),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.init_socket()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Game("Level1-2", None)
        game.run()






