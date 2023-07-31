import pygame
from pygame import Vector2
from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.snake_new.play import Game
from games_examples.snake_new.play import GameInherited
from games_examples.snake_new.src.fruit import Fruit
from games_examples.snake_new.src.snake import Snake



@given("A game with a snake")
def test_impl(test_context):

    def get_end(end):
        print(end,"end")
        return end
    test_context.game = test_context.create(GameInherited, "game",
                                            state=State("terminated2",func=get_end,      methods_to_observe = [ "reset", "end_game"]))

    # "end_game"
    def get_body(bodies):
        result = []
        for body in bodies:
            result.extend([body[0], body[1]])
        # print(result)
        return result

    def get_dir(dir):
        return [dir[0], dir[1]]

    def get_new(new):
        # print(new)
        return new

    test_context.game.snake = test_context.create(Snake, name="snake", state=[
        State("body",  func=get_body, methods_to_observe=["move_snake"]),
        State("direction", func=get_dir, methods_to_observe=["check_events"]),
        State("new_block",  methods_to_observe=["add_block"])
    ])
    #test_context.game.dt = 0.09

@given("A fruit")
def test_impl(test_context):
    def get_fruit(fruit):
        # print([fruit[0],fruit[1]])
        return [fruit[0], fruit[1]]

    test_context.game.fruit= test_context.create(Fruit, name="fruit", state=[
        State("pos", func=get_fruit, methods_to_observe=["randomize"]),
    ])


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
@when("There is one fruit")
def test_impl(test_context):
    test_context.game.reset()
    test_context.game.clock.tick(0)
    # pass

@loop
def test_impl(test_context):
    for event in pygame.event.get():
        test_context.game.snake.check_events(event) #########
        if event.type == test_context.game.SCREEN_UPDATE:
            test_context.game.update()


# @then("The player should have passed {nb_pipes} pipes")
# def test_impl(test_context, nb_pipes):
#     test_context.assert_true(test_context.game.player.points == int(nb_pipes))


@then("The snake should be longer")
def test_impl(test_context):
    test_context.assert_greater(test_context.game.snake.body, 3)

@render
def test_impl(test_context):

    # whether the screen have been drawn?
    test_context.game.render()
    pygame.display.flip()
    test_context.game.dt = test_context.game.clock.tick(60) / 1000






@log
def test_impl(test_context):
    return {

        "points": test_context.game.snake.body,
        "terminated": test_context.game.terminated2

    }






