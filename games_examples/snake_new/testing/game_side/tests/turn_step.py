from games_examples.snake.play import Main
from src.xumes.game_module.feature_strategy import given
from src.xumes.game_module.state_observable import State


@given("A game with a player")
def test_impl(test_context):
    test_context.game = test_context.create(Main, "game",
                                            state=State("terminated", methods_to_observe=["end_game", "reset"]))

    test_context.game.player = test_context.create(Player, name="player", state=[
        State("center", methods_to_observe=["move", "reset"]),
        State("speedup", methods_to_observe=["jump", "move", "reset"]),
        State("points", methods_to_observe=["gain_point", "reset"])], position=HEIGHT // 2, game=test_context.game)
