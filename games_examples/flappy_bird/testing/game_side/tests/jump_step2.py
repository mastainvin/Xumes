import pygame

from games_examples.flappy_bird.params import HEIGHT, LEFT_POSITION, SPACE_BETWEEN_PIPES, PIPE_SPACE, PIPE_WIDTH, SIZE
from games_examples.flappy_bird.play import Game, BACKGROUND_COLOR
from games_examples.flappy_bird.src.pipe import Pipe
from games_examples.flappy_bird.src.pipe_generator import PipeGenerator
from games_examples.flappy_bird.src.player import Player

from xumes.game_module import State, given, when, loop, then, render, log


@given("A game with a player")
def test_impl(test_context):
    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["end_game", "reset"]))

    test_context.game.player = test_context.create(Player, name="player", state=[
        State("center", methods_to_observe=["move", "reset"]),
        State("speedup", methods_to_observe=["jump", "move", "reset"]),
        State("points", methods_to_observe=["gain_point", "reset"])], position=HEIGHT // 2, game=test_context.game)

    def get_rect(x):
        return [x.left, x.top, x.right, x.bottom]

    test_context.game.pipe_generator = test_context.create(PipeGenerator, name="pipe_generator",
                                                           state=State("pipes",
                                                                       [
                                                                           State(
                                                                               "rect1",
                                                                               func=get_rect),
                                                                           State(
                                                                               "rect2",
                                                                               func=get_rect),
                                                                       ],
                                                                       methods_to_observe=["move", "reset"]
                                                                       ),
                                                           game=test_context.game)

    test_context.game.dt = 0.09


def get_height(x):
    x = x / 100
    return x * (HEIGHT - 100 - PIPE_SPACE) + 50


@when("The first pipe is at {i} % and the next pipe is at {j} %")
def test_impl(test_context, i, j):
    i, j = int(i), int(j)
    test_context.game.reset()
    test_context.game.pipe_generator.pipes = [Pipe(player=test_context.game.player,
                                                   generator=test_context.game.pipe_generator,
                                                   height=get_height(i),
                                                   position=LEFT_POSITION + SIZE / 2 + SPACE_BETWEEN_PIPES - PIPE_WIDTH / 2),
                                              Pipe(player=test_context.game.player,
                                                   generator=test_context.game.pipe_generator,
                                                   height=get_height(j),
                                                   position=LEFT_POSITION + SIZE / 2 + 2 * SPACE_BETWEEN_PIPES - PIPE_WIDTH / 2)]
    test_context.game.pipe_generator.notify()

    test_context.game.clock.tick(0)


@loop
def test_impl(test_context):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                test_context.game.player.jump()

    # Make all game state modification
    test_context.game.player.move(test_context.game.dt)
    test_context.game.pipe_generator.move(test_context.game.dt)


@then("The player should have passed {nb_pipes} pipes")
def test_impl(test_context, nb_pipes):
    test_context.assert_true(test_context.game.player.points == int(nb_pipes))


@then("The player should have passed at least {nb_pipes} pipes")
def test_impl(test_context, nb_pipes):
    test_context.assert_greater_equal(test_context.game.player.points, int(nb_pipes))


@render
def test_impl(test_context):
    # Background
    test_context.game.screen.fill(BACKGROUND_COLOR)

    test_context.game.render()
    pygame.display.flip()

    test_context.game.dt = test_context.game.clock.tick(60) / 1000


@log
def test_impl(test_context):
    x, y = test_context.game.player.center
    return {
        "player": {
            "points": test_context.game.player.points,
            "x": x,
            "y": y,
        },
    }
