from xumes.game_module import given
import random
from games_examples.connected.main import Game
from xumes.game_module import State, given, when, loop, then, render, log
import pygame
from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
from games_examples.connected.src.generator import Generator
from games_examples.connected.src.tile import Tiles
from games_examples.connected.src.ball import Balls
from games_examples.connected.src.coin import Coins
BACKGROUND_COLOR = (137, 207, 240)
@given("A game with a ball")
def test_impl(test_context):

    def get_end(end):
        # print(end,"end")
        return end
    # modification:move the creation of ball, coin.py and tile into the creation of game
    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["end_game", "reset"]))

    test_context.game.ball = test_context.create(Balls, name="ball", state=[
        State("x", methods_to_observe=["update", "reset"]),
        State("y", methods_to_observe=["update", "reset"]),
        State("center", methods_to_observe=["update", "reset"]),
        State("dtheta", methods_to_observe=["update","change_direction","reset"]),
        State("points", methods_to_observe=["gain_point", "reset"])],  y=CENTER[1],game=test_context.game)






@given("A generator")
def test_impl(test_context):
    def get_rect(x):
        return [x.left, x.top, x.right, x.bottom]
    test_context.game.generator = test_context.create(Generator, name="generator",
                                                           state=State("pipes",
                                                                       [
                                                                           State(
                                                                               "rect",
                                                                               func=get_rect),
                                                                           State("kind", methods_to_observe=[
                                                                                                          "reset"]),

                                                                       ],
                                                                       methods_to_observe=["move", "reset"]
                                                                       ),


                                                           game=test_context.game)

    test_context.game.dt = 0.09






def get_height(x):
    x = 1 - (x / 100)
    return x * (140) + CENTER[1]


@when("The first coin is at {i} % and the tile is at {j} % and the second coin is at {k} %")
def test_impl(test_context,i ,j,k):
    i, j, k= int(i), int(j), int(k)
    test_context.game.reset()

    test_context.game.generator.pipes = [
                                        # Coins(y=get_height(i),
                                        #        ball=test_context.game.ball,
                                        #        generator=test_context.game.generator),
                                         # Tiles(y=get_height(j),
                                         #       type_=random.randint(1, 3),
                                         #       ball=test_context.game.ball,
                                         #       generator=test_context.game.generator),
                                         # Coins(y=get_height(k),
                                         #       ball=test_context.game.ball,
                                         #       generator=test_context.game.generator),
]
    test_context.game.generator.notify()

    test_context.game.clock.tick(0)
    test_context.game.dt=0.09

# The player should have 2 point
@then("The ball should have {nb_points} point")
def test_impl(test_context, nb_points):
    # print("then")
    test_context.assert_true(test_context.game.ball.points == int(nb_points))
    # test_context.assert_greater_equal(test_context.game.score, int(nb_points))
    # test_context.assert_true(test_context.game.score >= int(nb_points))
    # test_context.assert_greater_equal(test_context.game.score, int(nb_points))
    # test_context.assert_true(test_context.game.score >= int(nb_points))

@then("The ball should have at least {nb_points} point")
def test_impl(test_context, nb_points):
        # print("then")

    test_context.assert_greater_equal(test_context.game.ball.points, int(nb_points))

    # test_context.assert_greater_equal(test_context.game.score, int(nb_points))
    # test_context.assert_true(test_context.game.score >= int(nb_points))
    # test_context.assert_greater_equal(test_context.game.score, int(nb_points))
    # test_context.assert_true(test_context.game.score >= int(nb_points))


@loop
def test_impl(test_context):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP :
                test_context.game.ball.up()
            elif  event.key == pygame.K_DOWN :
                test_context.game.ball.down()

    # keys = pygame.key.get_pressed()
    # if True:
    #     if keys[pygame.K_UP]:
    #         test_context.game.ball.dtheta = -2
    #     elif keys[pygame.K_DOWN]:
    #         test_context.game.ball.dtheta = 2

    # Make all game state modification

    test_context.game.generator.generator(test_context.game.dt)
    test_context.game.ball.update(test_context.game.dt)
    test_context.game.generator.move(test_context.game.dt)

@render
def test_impl(test_context):
    test_context.game.win.fill(BACKGROUND_COLOR)
    test_context.game.render()
    pygame.display.flip()

    test_context.game.dt = 0.0009

@log
def test_impl(test_context):
    return {

        "terminated": test_context.game.terminated

    }




