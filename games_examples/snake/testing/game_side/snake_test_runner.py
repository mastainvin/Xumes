import sys
import logging
import time


import pygame
from pygame import Vector2


from games_examples.snake.play import Main
from games_examples.snake.src.fruit import Fruit
from games_examples.snake.src.snake import Snake


from xumes.test_runner import TestRunner, GameService, PygameEventFactory, CommunicationServiceGameMq, State

cell_size = 30
cell_number = 15

# 问题1：拿不到self.game.snake.new_block 可能能传了，样本比例低
# 问题2： SnakeTestRunner拿不到结束一次后的所有数据 已解决
# 问题3：训练时输入的方向只有up down  只有前两个
# 猜测问题2、3的原因是： SnakeTestRunner只有在游戏刚开始时获取了数据  错误的
# 现在的问题：正确地传递吃水果和lose的状态到reward func  重要
# 问题2：不要让每局游戏太快结束 解决
class SnakeTestRunner(TestRunner):

    def __init__(self):
        super().__init__()
        self.game = Main()
        self.game = self.bind(self.game, "game", state=State("terminated", methods_to_observe=["game_over","run","update","check_fail"]))
    #     newly added
        def get_body(bodies):
            result = []
            for body in bodies:
                result.extend([body[0], body[1]])
            # print(result)
            return result
        def get_dir(dir):
            return [dir[0],dir[1]]

        def get_fruit(fruit):
            # print([fruit[0],fruit[1]])
            return [fruit[0],fruit[1]]
        def get_new(new):
            # print(new)
            return new
        self.game.snake = self.bind(Snake(), name="snake", state=[
            State("body", func=get_body, methods_to_observe=["__init__", "move_snake"] ),
            # move_snake
            State("direction", func=get_dir,methods_to_observe=["__init__","change_direction"]),
            State("new_block", func=get_new,methods_to_observe=["__init__","add_block","move_snake","update"])
        ])
        self.game.fruit = self.bind(Fruit(), name="fruit", state=[
            State("pos", func=get_fruit,methods_to_observe=["__init__","randomize","draw_fruit"]),

        ])
        self.game.all_sprites = pygame.sprite.Group()
        self.game.all_sprites.add(self.game.snake)
        self.game.all_sprites.add(self.game.fruit)

    def fruit_ate(self):
        super().fruit_ate()
        self.update_state("fruit_ate")
        print("ate")

    def game_over(self):
        self.update_state("lose")

    def run_test(self) -> None:
        while self.game.running:
            self.test_client.loop()
            for event in pygame.event.get():
                self.game.check_events(event)
            a = self.game.update()
            # print(a)
            self.game.clock.tick(0)

    def run_test_render(self) -> None:
        # self.game.run()
        while self.game.running:
            self.test_client.loop()
            for event in pygame.event.get():
                self.game.check_events(event)
            a = self.game.update()
            # print(a)
            self.game.screen.fill((175, 215, 70))
            self.game.draw_elements()
            pygame.display.update()
            self.game.clock.tick(0)



    def reset(self) -> None:
        # print("gg")
        self.game.game_over()

    def random_reset(self) -> None:
        # print("gg")
        self.game.game_over()


    def delete_screen(self) -> None:
        pass


if __name__ == "__main__":

    if len(sys.argv) > 1:

        if sys.argv[1] == "-test":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        if sys.argv[1] == "-render":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

        game_service = GameService(test_runner=SnakeTestRunner(),
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip="localhost"))
        if sys.argv[1] == "-test":
            game_service.init_socket()
        if sys.argv[1] == "-render":
            game_service.run_render()

    else:
        game = Main()
        game.run()
