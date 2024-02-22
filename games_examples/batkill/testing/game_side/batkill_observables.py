from abc import ABC

from xumes.test_runner.game_element_state import GameElementState
from xumes.test_runner.state_observable import StateObservable

from games_examples.batkill.src.backend_player import StandardPlayer
from games_examples.batkill.src.spriteful_bat import Bat


class PlayerObservable(StandardPlayer, StateObservable, ABC):

    def __init__(self, ground_y, rect, collider_rect, x_step, attack_cooldown, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        StandardPlayer.__init__(self, x=300, y=653, ground_y=ground_y, rect=rect, collider_rect=collider_rect, x_step=x_step, attack_cooldown=attack_cooldown)
        self.facing_nearest_bat = False
        self.bool_attack_rect = False
        self.notify()

    def update(self, actions=None, dt=None):
        super().update(actions=actions, dt=dt)
        self.notify()

    def state(self):
        return GameElementState({
            "position": {
                "x": self.rect.x,
                "y": self.rect.y
            },
            "direction": self.facing,
            "jump": self.jumping,
            "attack_state": self.attack.attack_state,
            "attack_duration": self.attack.attack_duration,
            "cool_down_state": self.attack.cool_down_state,
            "cool_down_duration": self.attack.cool_down_duration,
            "attack_rect": self.bool_attack_rect,
            "facing_nearest_bat": self.facing_nearest_bat,
            "lives": self.lives,
            "score": self.score
        })


class BatObservable(Bat, StateObservable, ABC):
    def __init__(self, direction, step, sprite_path, *groups, observers, name):
        StateObservable.__init__(self, observable_object=self, observers=observers, name=name)
        Bat.__init__(self, direction, step, sprite_path, *groups)
        self.bool_collider_rect = False
        self.notify()

    def update(self):
        super().update()
        self.notify()

    def state(self):
        return GameElementState({
            "position": {
                "x": self.rect.x,
                "y": self.rect.y
            },
            "direction": self.direction,
            "speed": self.step,
            "dead": self.dead,
            "collider_rect": self.bool_collider_rect
        })
