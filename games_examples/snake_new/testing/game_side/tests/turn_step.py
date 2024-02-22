import pygame
from pygame import Vector2
from xumes.test_runner import State, given, when, loop, then, render, log

from games_examples.snake_new.play import GameInherited
from games_examples.snake_new.src.fruit import Fruit
from games_examples.snake_new.src.snake import Snake


@given("A game with a snake")
def test_impl(test_context):
    def get_end(end):
        return end

    test_context.game = test_context.create(GameInherited, "game",
                                            state=State("terminated", func=get_end,
                                                        methods_to_observe=["reset", "end_game"]))

    # "end_game"
    def get_body(bodies):
        result = []
        for body in bodies:
            result.extend([body[0], body[1]])
        return result

    def get_dir(dir):
        return [dir[0], dir[1]]

    test_context.game.snake = test_context.create(Snake, name="snake", state=[
        State("body", func=get_body, methods_to_observe=["move_snake"]),
        State("direction", func=get_dir, methods_to_observe=["check_events"]),
        State("new_block", methods_to_observe=["add_block"])
    ])
    test_context.game.dt = 0.09


@given("A fruit")
def test_impl(test_context):
    def get_fruit(fruit):
        return [fruit[0], fruit[1]]

    test_context.game.fruit = test_context.create(Fruit, name="fruit", state=[
        State("pos", func=get_fruit, methods_to_observe=["randomize"]),
    ])

@when("There is one fruit")
def test_impl(test_context):
    test_context.game.reset()


@loop
def test_impl(test_context):
    for event in pygame.event.get():
        test_context.game.snake.check_events(event)
        if event.type == test_context.game.SCREEN_UPDATE:
            test_context.game.update()


@then("The snake should grow {nb_blocks} block")
def test_impl(test_context, nb_blocks):
    a = 2 * int(nb_blocks)
    test_context.assert_true(len(test_context.game.snake.body) >= a)


@render
def test_impl(test_context):
    test_context.game.render()
    pygame.display.flip()


@log
def test_impl(test_context):
    return {

        "points": [{"x": b[0], "y": b[1]} for b in test_context.game.snake.body],
        "terminated": test_context.game.terminated

    }
