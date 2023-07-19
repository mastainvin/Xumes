from games_examples.snake.play import Main
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

    test_context.game.snake = test_context.create(Snake, name="snake", state=[
        State("body",  func=get_body, methods_to_observe=["move_snake"]),
        State("direction", func=get_dir,methods_to_observe=["check_events"])


