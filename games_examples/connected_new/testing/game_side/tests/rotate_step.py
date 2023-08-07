from xumes.game_module import given

from games_examples.connected_new.main import Game
from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.connected_new.objects import Balls, Coins


@given("A game with a ball")
def test_impl(test_context):

    def get_end(end):
        print(end,"end")
        return end
    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", func=get_end,  methods_to_observe=["end_game", "reset"]))

    test_context.game.ball = test_context.create(Balls, name="ball", state=[
        State("rect", [State( "x" ), State( "y" )], methods_to_observe="update"),
        State("score" , methods_to_observe="update"),
        State("highscore", methods_to_observe="update")

    ])

@given("A coin")
def test_impl(test_context):

    test_context.game.coin = test_context.create(Coins, name="coin", state=[
        State("rect", [State( "x" ), State( "y" )], methods_to_observe=["update"])
    ])


@given("A tile")
def test_impl(test_context):
    test_context.game.tile = test_context.create(Coins, name="coin", state=[
        State("rect", [State("x"), State("y")], methods_to_observe=["update"]),
        State("type", methods_to_observe=["update"]),
    ])



@when("There is one coin")
def test_impl(test_context):
    test_context.game.reset()

@then("The ball should have {nb_points] point")
def test_impl(test_context, nb_points):
    print("then")
    test_context.assert_true(test_context.game.ball.score == int(nb_points))



@loop
def test_impl(test_context):

    while test_context.game.running:
        test_context.test_client.wait()
        test_context.game.update()

@render
def test_impl(test_context):
    while test_context.game.running:
        test_context.test_client.wait()
        test_context.game.update()

        test_context.game.render()

@log
def test_impl(test_context):
    return {

        "score": test_context.game.ball.score,
        "terminated": test_context.game.terminated

    }




