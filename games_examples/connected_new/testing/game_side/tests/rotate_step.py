from xumes.game_module import given
import random
from games_examples.connected_new.main import Game
from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.connected_new.objects import Balls, Coins, Tiles


@given("A game with a ball")
def test_impl(test_context):

    def get_end(end):
        print(end,"end")
        return end
    # modification:move the creation of ball, coin and tile into the creation of game
    test_context.game = test_context.create(Game, "game",
                                            state=[State("terminated", func=get_end,
                                                        methods_to_observe=["end_game", "reset"]
                                                        ),
    State("ball", [State("score"), State("highscore"), State("rect", [State("x"), State("y")])],
          methods_to_observe="update"),
    State("coin", [State("x"), State("y")], methods_to_observe="update"),
    State("t", [State("x"), State("y"), State("type")], methods_to_observe="update"),
                                                   ]
    )
    # test_context.game = test_context.create(Game, "game",
    #                                         state=State("terminated", func=get_end,  methods_to_observe=["end_game", "reset"]))
    # test_context.game.ball = test_context.create(Balls, name="ball", state=[
    #     State("rect", [State( "x" ), State( "y" )], methods_to_observe="update"),
    #     State("score" , methods_to_observe="update"),
    #     State("highscore", methods_to_observe="update")
    #
    # ],
    #                                              # add initializing params
    #                                              pos=(test_context.game.CENTER[0],
    #                                                   test_context.game.CENTER[1] + test_context.game.RADIUS),
    #                                              radius=test_context.game.RADIUS, angle=90, win=test_context.game.win
    #                                              )


@given("A coin")
def test_impl(test_context):
    pass
    # test_context.game.coin = test_context.create(Coins, name="coin", state=[
    #     State("rect", [State( "x" ), State( "y" )], methods_to_observe=["update"])
    # ],
    #                                              y=random.randint(test_context.game.CENTER[1] - test_context.game.RADIUS,
    #                                                             test_context.game.CENTER[1] + test_context.game.RADIUS),
    #                                              win=test_context.game.win)


@given("A tile")
def test_impl(test_context):
    pass
    # change game.tile into game.t, because the game developer does so in the class Game
    # test_context.game.t = test_context.create(Tiles, name="tile", state=[
    #     State("rect", [State("x"), State("y")], methods_to_observe=["update"]),
    #     State("type", methods_to_observe=["update"]),
    # ],
    #     y=random.choice([test_context.game.CENTER[1] - 80,
    #                      test_context.game.CENTER[1], test_context.game.CENTER[1] + 80]),
    #                                              type_=random.randint(1, 3),
    #                                              win=test_context.game.win)




@when("There is one coin")
def test_impl(test_context):
    # recreate for the new ball; remove the old ball in the group; and notify
    test_context.game.reset()
    test_context.game.ball_group.remove(test_context.game.ball)
    test_context.game.ball = test_context.create(Balls, name="ball", state=[
        State("rect", [State("x"), State("y")], methods_to_observe="update"),
        State("score", methods_to_observe="update"),
        State("highscore", methods_to_observe="update")

    ],
                                                 # add initializing params
                                                 pos=(test_context.game.CENTER[0],
                                                      test_context.game.CENTER[1] + test_context.game.RADIUS),
                                                 radius=test_context.game.RADIUS, angle=90, win=test_context.game.win
                                                 )
    test_context.game.ball_group.add(test_context.game.ball)
    test_context.game.ball.notify()


@then("The ball should have {nb_points} point")
def test_impl(test_context, nb_points):
    print("then")
    test_context.assert_true(test_context.game.ball.score == int(nb_points))



@loop
def test_impl(test_context):
    test_context.game.update_check()

@render
def test_impl(test_context):
    # while test_context.game.running:
        # test_context.test_client.wait()
        # test_context.game.update()

    test_context.game.render()

@log
def test_impl(test_context):
    return {

        "score": test_context.game.ball.score,
        "terminated": test_context.game.terminated

    }




