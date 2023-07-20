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
    test_context.game.dt = 0.09

# @when("The first pipe is at {i} % and the next pipe is at {j} %")
# def test_impl(test_context, i, j):
#     i, j = int(i), int(j)
#     test_context.game.reset()
#     test_context.game.pipe_generator.pipes = [Pipe(player=test_context.game.player,
#                                                    generator=test_context.game.pipe_generator,
#                                                    height=get_height(i),
#                                                    position=LEFT_POSITION + SIZE / 2 + SPACE_BETWEEN_PIPES - PIPE_WIDTH / 2),
#                                               Pipe(player=test_context.game.player,
#                                                    generator=test_context.game.pipe_generator,
#                                                    height=get_height(j),
#                                                    position=LEFT_POSITION + SIZE / 2 + 2 * SPACE_BETWEEN_PIPES - PIPE_WIDTH / 2)]
#     test_context.game.pipe_generator.notify()
#
#     test_context.game.clock.tick(0)

@loop
def test_impl(test_context):
    for event in pygame.event.get():
        test_context.snake.check_events(event) #########
        if event.type == test_context.Main.SCREEN_UPDATE:
            test_context.Main.update()
            test_context.Main.clock.tick(0)  #maybe should deleete this line

# @then("The player should have passed {nb_pipes} pipes")
# def test_impl(test_context, nb_pipes):
#     test_context.assert_true(test_context.game.player.points == int(nb_pipes))


@render
def test_impl(test_context):

    # whether the screen have been drawn?
    test_context.Main.render()
    pygame.display.flip()
    test_context.game.dt = test_context.game.clock.tick(60) / 1000

@when("There are no spaces between the head of the snake and the wall")
def test_impl(test_context):
    test_context.Main.reset()
    test_context.Main.snake = Snake(body=[Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)])




