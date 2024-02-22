import logging
from os import wait
from time import sleep

import pygame

from xumes.test_runner import State, given, when, loop, then, render, log

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game


@given("A game with a player")
def test_impl(test_context):
    def _get_rect(rect):
        return [rect.x, rect.y]

    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["run", "reset"]),
                                            levelname="jump_feature", feature=["jump", "100-100"])

    test_context.game.mario = test_context.create(Mario, "mario", state=[
        State("rect", func=_get_rect, methods_to_observe="moveMario"),
        State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
        State("ending_level", methods_to_observe="end_level"),
        State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                  "_onCollisionWithBlock",
                                                                                  "killEntity",
                                                                                  "_onCollisionWithItem"])
    ],
                                                  x=0, y=0, level=test_context.game.level,
                                                  screen=test_context.game.screen,
                                                  dashboard=test_context.game.dashboard,
                                                  gravity=0.8)


@when("The first pipe is at {i} % and the next pipe is at {j} %")
def test_impl(test_context, i, j):
    level = ["jump", str(i + "-" + j)]
    test_context.game.reset(level)

    def _get_rect(rect):
        return [rect.x, rect.y]

    test_context.game.mario = test_context.create(Mario, "mario", state=[
        State("rect", func=_get_rect, methods_to_observe="moveMario"),
        State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
        State("ending_level", methods_to_observe="end_level"),
        State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                  "_onCollisionWithBlock",
                                                                                  "killEntity",
                                                                                  "_onCollisionWithItem"])
    ],
                                                  x=0, y=0, level=test_context.game.level,
                                                  screen=test_context.game.screen,
                                                  dashboard=test_context.game.dashboard,
                                                  gravity=0.8)
    test_context.game.mario.notify()
    test_context.game.clock.tick(0)
    test_context.game.dt = 0.09


@loop
def test_impl(test_context):
    pygame.display.set_caption("Super Mario running with {:d} FPS".format(int(test_context.game.clock.get_fps())))
    test_context.game.level.drawLevel(test_context.game.mario.camera, test_context.game.dt)
    test_context.game.dashboard.update()
    test_context.game.mario.update(test_context.game.dt)




@then("The player should have passed {nb_pipes} pipes")
def test_impl(test_context, nb_pipes):
    if int(nb_pipes) == 2:
        test_context.assert_greater(test_context.game.mario.rect.x, 448)
    elif int(nb_pipes) == 0:
        test_context.assert_less(test_context.game.mario.rect.x, 448)


@render
def test_impl(test_context):
    # Background
    pygame.display.update()
    test_context.game.dt = test_context.game.clock.tick(test_context.game.max_frame_rate) / 1000


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
        },
        "dashboard": {
            "points": test_context.game.mario.dashboard.points,
            "coins": test_context.game.mario.dashboard.coins,
        },
    }
