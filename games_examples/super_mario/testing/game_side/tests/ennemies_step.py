import pygame

from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.super_mario.entities.Mario import Mario
from games_examples.super_mario.main import Game


@given("A game with a player against {i} ennemies")
def test_impl(test_context, i):
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
                                            levelname="ennemies_feature", feature=["ennemies", "2-0"])

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


@when("There is {i} Goomba and {j} Koopa")
def test_impl(test_context, i, j):
    level = ["ennemies", str(i + "-" + j)]
    test_context.game.reset(level)

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


@then("The player should have killed {nb_ennemies} ennemies")
def test_impl(test_context, nb_ennemies):
    if int(nb_ennemies) == 1:
        test_context.assert_greater_equal(test_context.game.mario.dashboard.points, 100)


@render
def test_impl(test_context):
    # Background
    pygame.display.update()
    test_context.game.clock.tick(test_context.game.max_frame_rate)


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
        },
        "dashboard": {
            "points": test_context.game.mario.dashboard.points,
            "coins": test_context.game.mario.dashboard.coins,
        },
    }
    for idx, entity in enumerate(test_context.game.mario.levelObj.entityList):
        dct[f'entity_{idx}_position'] = [entity.rect.x, entity.rect.y]
        dct[f'entity_{idx}_alive'] = entity.alive
        dct[f'entity_{idx}_active'] = entity.active
        dct[f'entity_{idx}_bouncing'] = entity.bouncing
        dct[f'entity_{idx}_onGround'] = entity.onGround
    return dct
