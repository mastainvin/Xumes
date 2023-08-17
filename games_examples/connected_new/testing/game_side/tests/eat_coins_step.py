from xumes.game_module import given
import random
from games_examples.connected_new.main import Game
from xumes.game_module import State, given, when, loop, then, render, log
import pygame
from games_examples.connected_new.objects import Balls, Coins, Tiles


@given("A game with a ball")
def test_impl(test_context):

    def get_end(end):
        print(end,"end")
        return end
    # modification:move the creation of ball, coin and tile into the creation of game
    test_context.game = test_context.create(Game, "game",
                                            state=[State("terminated", func=get_end,
                                                        methods_to_observe=["end_game", "reset","reset2"]
                                                        ),
    State("ball", [State("x"), State("y"),State("score"), State("highscore"), State("rect", [State("x"), State("y")])],
          methods_to_observe="update_main"),
    State("coin", [State("x"), State("y"),State("rect", [State( "x" ), State( "y" )])], methods_to_observe="update_main"),
    State("tile", [State("x"), State("y"), State("type"),State("rect", [State( "x" ), State( "y" )])], methods_to_observe="update_main"),
    State("highscore", methods_to_observe="update_main")                  ,
    State("score", methods_to_observe="update_main")
                                                   ]
    )
    test_context.game.ball = test_context.bind(test_context.game.ball, name="ball",
                                               state=[
                                                   State("x", methods_to_observe=["update_main"]),
                                                   State("y", methods_to_observe=["update_main"]),
                                                   State("rect", [State("x"), State("y")], methods_to_observe="update"),
                                                   State("score", methods_to_observe="update"),
                                                   State("highscore", methods_to_observe="update")

                                               ])
    test_context.game.coin = test_context.bind(test_context.game.coin, name="coin", state=[
        State("x", methods_to_observe=["update_main"]),
        State("y", methods_to_observe=["update_main"]),
        State("rect", [State("x"), State("y")], methods_to_observe=["update_main"])
    ])
    test_context.game.tile = test_context.bind(test_context.game.tile, name="tile", state=[
        State("x", methods_to_observe=["update_main"]),
        State("y", methods_to_observe=["update_main"]),
        State("rect", [State("x"), State("y")], methods_to_observe=["update_main"])
    ])



@given("A coin")
def test_impl(test_context):
    # pass
    # test_context.game.coin_group.remove(test_context.game.coin)
    test_context.game.coin = test_context.create(Coins, name="coin", state=[
        State("x", methods_to_observe=["update_main"]),
        State("y", methods_to_observe=["update_main"]),
        State("rect", [State("x"), State("y")], methods_to_observe=["update_main"])
    ],
                                                 y=random.randint(
                                                     test_context.game.CENTER[1] - test_context.game.RADIUS,
                                                     test_context.game.CENTER[1] + test_context.game.RADIUS),
                                                 win=test_context.game.win)

    test_context.game.tile = test_context.create(Tiles, name="tile", state=[
        State("x", methods_to_observe=["update_main"]),
        State("y", methods_to_observe=["update_main"]),
        State("rect", [State("x"), State("y")], methods_to_observe=["update_main"]),
        State("type", methods_to_observe=["update_main"]),
    ],
                                                 y=random.choice([test_context.game.CENTER[1] - 80,
                                                                  test_context.game.CENTER[1],
                                                                  test_context.game.CENTER[1] + 80]),
                                                 type_=random.randint(1, 3),
                                                 win=test_context.game.win)

    test_context.game.ball_group = pygame.sprite.Group()
    test_context.game.coin_group = pygame.sprite.Group()
    test_context.game.tile_group = pygame.sprite.Group()
    test_context.game.all_sprites = pygame.sprite.Group()
    test_context.game.all_sprites.add(test_context.game.ball)
    test_context.game.all_sprites.add(test_context.game.coin)
    test_context.game.all_sprites.add(test_context.game.tile)
    test_context.game.reset2()


@given("A tile")
def test_impl(test_context):
    pass
    # change game.tile into game.t, because the game developer does so in the class Game





@when("There is one coin")
def test_impl(test_context):
    test_context.game.reset()
    # pass

@then("The ball should have {nb_points} point")
def test_impl(test_context, nb_points):
    print("then")
    test_context.assert_true(test_context.game.score >= int(nb_points))
    test_context.assert_greater_equal(test_context.game.score, int(nb_points))



@loop
def test_impl(test_context):
    test_context.game.update_check()

@render
def test_impl(test_context):
    test_context.game.render()

@log
def test_impl(test_context):
    return {

        "score": test_context.game.score,
        "terminated": test_context.game.terminated

    }




