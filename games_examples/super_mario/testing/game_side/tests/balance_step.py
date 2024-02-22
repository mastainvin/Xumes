import pygame

from xumes.test_runner import State, given, when, loop, then, render, log

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game


@given("A game with a player, {i} pipes, {j} goombas and {k} holes")
def test_impl(test_context, i, j, k):
    print("given passed")
    def _get_rect(rect):
        return [rect.x, rect.y]

    def _get_attributes(lst):
        return [{
            'position': {
                'x': item.rect.x,
                'y': item.rect.y
            },
            'alive': item.alive,
            'active': item.active,
            'bouncing': item.bouncing,
            'onGround': item.onGround
        } for item in lst]

    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["run", "reset"]),
                                            levelname="balance_feature", feature=["balance", str(i + "-" + j + "-" + k)])

    test_context.game.mario = test_context.create(Mario, "mario", state=[
        State("rect", func=_get_rect, methods_to_observe="moveMario"),
        State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
        State("ending_level", methods_to_observe="end_level"),
        State("levelObj", State("entityList", func=_get_attributes),
              methods_to_observe=["_onCollisionWithItem", "_onCollisionWithMob"]),
        State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                  "_onCollisionWithBlock",
                                                                                  "killEntity",
                                                                                  "_onCollisionWithItem"])
    ],
                                                  x=0, y=0, level=test_context.game.level,
                                                  screen=test_context.game.screen,
                                                  dashboard=test_context.game.dashboard,
                                                  gravity=0.8)


@when("There is {i} pipes, {j} goombas and {k} holes")
def test_impl(test_context, i, j, k):
    print("when passed")
    level = ["balance", str(i + "-" + j + "-" + k)]
    test_context.game.reset(level)

    def _get_rect(rect):
        return [rect.x, rect.y]

    def _get_attributes(lst):
        return [{
            #'type': item.type,
            'position': {
                'x': item.rect.x,
                'y': item.rect.y
            },
            'alive': item.alive,
            'active': item.active,
            'bouncing': item.bouncing,
            'onGround': item.onGround
        } for item in lst]

    test_context.game.mario = test_context.create(Mario, "mario", state=[
        State("rect", func=_get_rect, methods_to_observe="moveMario"),
        State("powerUpState", methods_to_observe=["powerup", "_onCollisionWithMob"]),
        State("restart", methods_to_observe="gameOver"),
        State("ending_level", methods_to_observe="end_level"),
        State("levelObj", State("entityList", func=_get_attributes),
              methods_to_observe=["_onCollisionWithItem", "_onCollisionWithMob"]),
        State("dashboard", [State("coins"), State("points")], methods_to_observe=["_onCollisionWithItem",
                                                                                  "_onCollisionWithBlock",
                                                                                  "killEntity"
                                                                                  ])
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

@then("The player should have passed {nb_pipes} pipes at x {position}")
def test_impl(test_context, nb_pipes, position):
    if int(nb_pipes) == 1:
        test_context.assert_true(test_context.game.mario.rect.x >= int(position))

@then("The player should have killed {nb_enemies} enemies")
def test_impl(test_context, nb_enemies):
    if int(nb_enemies) == 1:
        test_context.assert_true(test_context.game.mario.dashboard.points >= 100)

@then("The player should have passed {nb_holes} holes at x {position}")
def test_impl(test_context, nb_holes, position):
    if int(nb_holes) == 1:
        test_context.assert_true(test_context.game.mario.rect.x >= int(position))

@render
def test_impl(test_context):
    # Background
    pygame.display.update()
    test_context.game.clock.tick(test_context.game.max_frame_rate)

    test_context.game.dt = test_context.game.clock.tick(60) / 1000

@log
def test_impl(test_context):

    x, y = test_context.game.mario.rect[0], test_context.game.mario.rect[1]
    dct = {
        "player": {
            "position": {
                "x": x,
                "y": y,
            },
            "powerUp": test_context.game.mario.powerUpState,
            "restart": test_context.game.mario.restart
        },
        "dashboard": {
            "points": test_context.game.mario.dashboard.points,
            "coins": test_context.game.mario.dashboard.coins,
        },
    }
    #print(test_context.game.mario.levelObj.entityList)
    for idx, entity in enumerate(test_context.game.mario.levelObj.entityList):
        dct[f'entity_{idx}_position'] = [entity.rect.x, entity.rect.y]
        dct[f'entity_{idx}_alive'] = entity.alive
        dct[f'entity_{idx}_active'] = entity.active
        dct[f'entity_{idx}_bouncing'] = entity.bouncing
        dct[f'entity_{idx}_onGround'] = entity.onGround
    return dct
