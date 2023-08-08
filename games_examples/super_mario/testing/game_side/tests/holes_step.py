import pygame

from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game


@given("A game with a player")
def test_impl(test_context):
    def _get_rect(rect):

        if rect is not None:
            return [rect.x, rect.y]

    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["run", "reset"]),
                                            levelname="hole_feature", feature=None)

    test_context.game.mario = test_context.create(Mario, "mario", state=[
        State("rect", func=_get_rect, methods_to_observe="moveMario"),
        State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
        State("ending_level", methods_to_observe="end_level"),
        State("restart", methods_to_observe="gameOver")],
                                                  x=0, y=0, level=test_context.game.level,
                                                  screen=test_context.game.screen,
                                                  dashboard=test_context.game.dashboard,
                                                  gravity=0.8)


@when("There is {nb_holes} holes")
def test_impl(test_context, nb_holes):
    test_context.game.reset(None)

    def _get_rect(rect):
        if rect is not None:
            return [rect.x, rect.y]

    test_context.game.mario = test_context.create(Mario, "mario", state=[
        State("rect", func=_get_rect, methods_to_observe="moveMario"),
        State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
        State("restart", methods_to_observe="gameOver"),
        State("ending_level", methods_to_observe="end_level")
    ],
                                                  x=0, y=0, level=test_context.game.level,
                                                  screen=test_context.game.screen,
                                                  dashboard=test_context.game.dashboard,
                                                  gravity=0.8)
    test_context.game.mario.notify()
    test_context.game.clock.tick(0)


@loop
def test_impl(test_context):
    pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(test_context.game.clock.get_fps())))
    test_context.game.level.drawLevel(test_context.game.mario.camera, test_context.game.dt)
    test_context.game.dashboard.update()
    test_context.game.mario.update(test_context.game.dt)
    test_context.game.dt = test_context.game.clock.tick(60) / 1000


@then("The player should have passed {nb_holes} holes at {position}")
def test_impl(test_context, nb_holes, position):
    print("------------------PRINT THEN --------------------")
    if int(nb_holes) == 1:
        test_context.assert_true(test_context.game.mario.rect.x > int(position))
        #test_context.assert_greater(test_context.game.mario.rect.x, int(position))


@render
def test_impl(test_context):
    # Background
    pygame.display.update()
    test_context.game.clock.tick(test_context.game.max_frame_rate)

    test_context.game.dt = test_context.game.clock.tick(60) / 1000


@log
def test_impl(test_context):
    x, y = test_context.game.mario.rect[0], test_context.game.mario.rect[1]

    return {
        "player": {
            "position": {
                "x": x,
                "y": y,
            },
            "powerUp": test_context.game.mario.powerUpState,
            "restart": test_context.game.mario.restart,
        }
    }
