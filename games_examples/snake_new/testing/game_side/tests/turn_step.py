import pygame
from pygame import Vector2
from xumes.game_module import loop, render, when

from games_examples.snake.play import Main
from games_examples.snake_new.src import snake
from games_examples.snake_new.src.fruit import Fruit
from src.xumes.game_module.feature_strategy import given

from games_examples.snake_new.src.snake import Snake
from src.xumes.game_module.state_observable import State


@given("A game with a snake")
def test_impl(test_context):
    test_context.game = test_context.create(Main, "game",
                                            state=State("terminated", methods_to_observe=["end_game", "reset"]))

    def get_body(bodies):
        result = []
        for body in bodies:
            result.extend([body[0], body[1]])
            print(result)
        return result

    def get_dir(dir):
        return [dir[0], dir[1]]

    def get_new(new):
        # print(new)
        return new



    test_context.game.snake = test_context.create(Snake, name="snake", state=[
        State("body",  func=get_body, methods_to_observe=["move_snake"]),
        State("direction", func=get_dir,methods_to_observe=["check_events"])
    ])
@given("A fruit")

def get_fruit(fruit):
    # print([fruit[0],fruit[1]])
    return [fruit[0], fruit[1]]
def test_impl(test_context):


    test_context.game.fruit= test_context.create(Fruit, name="fruit", state=[
        State("pos", func=get_fruit, methods_to_observe=["__init__", "randomize", "draw_fruit"]),
    ])

@loop
def test_impl(test_context):
    for event in pygame.event.get():
        test_context.snake.check_events(event)
        if event.type == test_context.Main.SCREEN_UPDATE:
            test_context.Main.update()
            test_context.Main.clock.tick(0)


@render
def test_impl(test_context):
    test_context.Main.render()

@when("There are no spaces between the head of the snake and the wall")
def test_impl(test_context):
    test_context.Main.reset()
    test_context.Main.snake = Snake(body=[Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])




