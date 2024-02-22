import time

import pygame

from xumes.test_runner import State, given, when, loop, then, render, log

from games_examples.dont_touch.play import Game
from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.hand_side import HandSide
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import is_close_app_event, update_background_using_scroll

def _get_pos(pos):
    return [pos[0], pos[1]]


@given("A game with a player")
def test_impl(test_context):

    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["run", "reset"]))

    test_context.game.scoreboard = test_context.create(Scoreboard, name="scoreboard", state=[
        State("current_score", methods_to_observe="increase_current_score"),
        State("max_score", methods_to_observe="update_max_score")
    ])
    print(test_context.game.P1)
    test_context.game.P1 = test_context.bind(test_context.game.P1, name="player", state=State("player_position", func=_get_pos,
                                                                                  methods_to_observe="update"))


@given("1 left hand and 1 right hand")
def test_impl(test_context):

    def create_hand_context(name, side):
        return test_context.create(Hand, name,
                                   state=[
                                       State("new_x", methods_to_observe="move"),
                                       State("new_y", methods_to_observe="move"),
                                       State("new_spd", methods_to_observe="move"),
                                   ],
                                   hand_side=side, offset_x=0, speed=2.7, random_hand=False)

    test_context.game.H1 = create_hand_context("left_hand", HandSide.LEFT)
    test_context.game.H2 = create_hand_context("right_hand", HandSide.RIGHT)

    test_context.game.hands = pygame.sprite.Group()
    test_context.game.all_sprites = pygame.sprite.Group()
    test_context.game.all_sprites.add(test_context.game.P1)
    if test_context.game.H1 is not None:
        test_context.game.hands.add(test_context.game.H1)
        test_context.game.all_sprites.add(test_context.game.H1)
    if test_context.game.H2 is not None:
        test_context.game.hands.add(test_context.game.H2)
        test_context.game.all_sprites.add(test_context.game.H2)


@when("There is 1 left hand at {x_left} and 1 right hand at {x_right}")
def test_impl(test_context, x_left, x_right):
    x_left, x_right = int(x_left), int(x_right)
    test_context.game.reset()

    test_context.game.H1.offset_x = x_left
    test_context.game.H1.notify()
    test_context.game.H2.offset_x = x_right
    test_context.game.H2.notify()

    test_context.game.FramePerSec.tick(0)
    test_context.game.dt = 0.09


@loop
def test_impl(test_context):

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            test_context.game.P1.update(event, test_context.game.dt)
    if test_context.game.H1 is not None:
        test_context.game.H1.move(test_context.game.scoreboard, test_context.game.P1.player_position, test_context.game.dt)
    if test_context.game.H2 is not None:
        test_context.game.H2.move(test_context.game.scoreboard, test_context.game.P1.player_position, test_context.game.dt)

    if pygame.sprite.spritecollide(test_context.game.P1, test_context.game.hands, False, pygame.sprite.collide_mask):
        test_context.game.scoreboard.update_max_score()
        test_context.game.end_game()
        # time.sleep(0.5)

    # test_context.game.dt = test_context.game.FramePerSec.tick(Config.FPS) / 1000


@then("The player should avoid {nb_hands} hands")
def test_impl(test_context, nb_hands):
    print("------------------------ CURRENT SCORE -----------------", test_context.game.scoreboard.current_score)
    test_context.assert_true(test_context.game.scoreboard.current_score == int(nb_hands))


@render
def test_impl(test_context):
    GlobalState.SCROLL = update_background_using_scroll(GlobalState.SCROLL)
    VisualizationService.draw_background_with_scroll(GlobalState.SCREEN, GlobalState.SCROLL)

    test_context.game.P1.draw(GlobalState.SCREEN)
    if test_context.game.H1 is not None:
        test_context.game.H1.draw(GlobalState.SCREEN)
    if test_context.game.H2 is not None:
        test_context.game.H2.draw(GlobalState.SCREEN)
    test_context.game.scoreboard.draw(GlobalState.SCREEN)

    # test_context.game.dt = test_context.game.FramePerSec.tick(Config.FPS) / 1000
    pygame.display.update()


@log
def test_impl(test_context):
    dct = {
        "player": {
            "position": {
                "x": test_context.game.P1.player_position[0],
                "y": test_context.game.P1.player_position[1]
            }
        },
        "scoreboard": {
            "current_score": test_context.game.scoreboard.current_score,
            "max_score": test_context.game.scoreboard.max_score
        }
    }
    if test_context.game.H1 is not None:
        dct["left_hand"] = {
            "position": {
                "x": test_context.game.H1.new_x,
                "y": test_context.game.H1.new_y
            },
            "new_speed": test_context.game.H1.new_spd
        }
    if test_context.game.H2 is not None:
        dct["right_hand"] = {
            "position": {
                "x": test_context.game.H2.new_x,
                "y": test_context.game.H2.new_y
            },
            "new_speed": test_context.game.H2.new_spd
        }

    return dct