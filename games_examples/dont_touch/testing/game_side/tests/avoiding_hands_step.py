import time

import pygame

from xumes.game_module import State, given, when, loop, then, render, log

from games_examples.dont_touch.play import Game
from games_examples.dont_touch.src.components.hand import Hand
from games_examples.dont_touch.src.components.hand_side import HandSide
from games_examples.dont_touch.src.components.scoreboard import Scoreboard
from games_examples.dont_touch.src.components.player import Player
from games_examples.dont_touch.src.config import Config
from games_examples.dont_touch.src.global_state import GlobalState
from games_examples.dont_touch.src.services.music_service import MusicService
from games_examples.dont_touch.src.services.visualization_service import VisualizationService
from games_examples.dont_touch.src.utils.tools import is_close_app_event, update_background_using_scroll


def _get_rect(rect):
    return [rect.center[0], rect.center[1]]

@given("A game with a player")
def test_impl(test_context):

    test_context.game = test_context.create(Game, "game",
                                            state=State("terminated", methods_to_observe=["run", "reset"]))

    test_context.game.scoreboard = test_context.create(Scoreboard, name="scoreboard", state=[
        State("_current_score", methods_to_observe="increase_current_score"),
        State("_max_score", methods_to_observe="update_max_score")
    ])

    test_context.game.P1 = test_context.create(Player, name="player", state=[
        State("rect", func=_get_rect, methods_to_observe="update")
    ])


@given("{nb_left_hand} left hand and {nb_right_hand} right hand")
def test_impl(test_context, nb_left_hand, nb_right_hand):
    nb_left_hand, nb_right_hand = int(nb_left_hand), int(nb_right_hand)

    def create_hand_context(side, name, offset, speed):
        return test_context.create(Hand, name,
                                   state=[
                                       State("rect", func=_get_rect, methods_to_observe="move"),
                                       State("new_spd", methods_to_observe="move")
                                   ],
                                   hand_side=side, offeset_x=offset, speed=speed, random_hand=False)

    if nb_right_hand == 1 and nb_left_hand == 0:
        test_context.game.H1 = None
        test_context.game.H2 = create_hand_context(HandSide.RIGHT, "right_hand", 0, 3)

    if nb_right_hand == 0 and nb_left_hand == 1:
        test_context.game.H1 = create_hand_context(HandSide.LEFT, "left_hand", 0, 3)
        test_context.game.H2 = None

    if nb_right_hand == 1 and nb_left_hand == 1:
        test_context.game.H1 = create_hand_context(HandSide.RIGHT, "right_hand", 0, 3)
        test_context.game.H2 = create_hand_context(HandSide.LEFT, "left_hand", 0, 3)

    test_context.game.hands = pygame.sprite.Group()
    test_context.game.all_sprites = pygame.sprite.Group()
    test_context.game.all_sprites.add(test_context.game.P1)
    if test_context.game.H1 is not None:
        test_context.game.hands.add(test_context.game.H1)
        test_context.game.all_sprites.add(test_context.game.H1)
    if test_context.game.H2 is not None:
        test_context.game.hands.add(test_context.game.H2)
        test_context.game.all_sprites.add(test_context.game.H2)


@when("There is {nb_left_hand} left hand at position {left_x} and {nb_right_hand} right hand at {right_x}")
def test_impl(test_context, nb_left_hand, nb_right_hand, left_x, right_x):
    nb_left_hand, nb_right_hand = int(nb_left_hand), int(nb_right_hand)
    left_x, right_x = int(left_x), int(right_x)

    test_context.game.reset()

    if nb_right_hand == 0 and nb_left_hand == 1:
        test_context.game.H1.offset_x = left_x
        test_context.game.H1.notify()
    elif nb_right_hand == 1 and nb_left_hand == 0:
        test_context.game.H2.offset_x = right_x
        test_context.game.H2.notify()
    else:
        test_context.game.H1.offset_x = left_x
        test_context.game.H1.notify()
        test_context.game.H2.offset_x = right_x
        test_context.game.H2.notify()
    test_context.game.clock.tick(0)


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
        MusicService.play_slap_sound()
        test_context.game.end_game()
        time.sleep(0.5)

    test_context.game.dt = test_context.game.FramePerSec.tick(Config.FPS) / 1000


@then("The player should avoid {nb_hands} hands")
def test_impl(test_context, nb_hands):
    test_context.assert_greater_equal(test_context.game.scoreboard._current_score, int(nb_hands))


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

    test_context.game.dt = test_context.game.FramePerSec.tick(Config.FPS) / 1000
    pygame.display.update()


@log
def test_impl(test_context):
    dct = {
        "player": {
            "position": {
                "x": test_context.P1.rect[0],
                "y": test_context.P1.rect[1]
            }
        },
        "scoreboard": {
            "current_score": test_context.game.scoreboard._current_score,
            "max_score": test_context.game.scoreboard._max_score
        }
    }
    if test_context.game.H1 is not None:
        dct["left_hand"] = {
            "position": {
                "x": test_context.game.left_hand.rect[0],
                "y": test_context.game.left_hand.rect[1]
            },
            "new_speed": test_context.game.left_hand.new_spd
        }
    if test_context.game.H2 is not None:
        dct["right_hand"] = {
            "position": {
                "x": test_context.game.right_hand.rect[0],
                "y": test_context.game.right_hand.rect[1]
            },
            "new_speed": test_context.game.right_hand.new_spd
        }