from typing import List

from xumes import TestStep, Input
from xumes.modules.godot.input.joy_motion import JoyAxis, JoyMotion

class GodotJoyToDirectionStep(TestStep):
    def __init__(self, joy_axis: JoyAxis, value: float, duration=10):
        super().__init__()
        self.joy_axis = joy_axis
        self.value = value
        self.joy_motion = JoyMotion(self.joy_axis, self.value)
        self.initial_duration = duration
        self.duration = duration

    def step(self) -> List[Input]:
        if self.duration > 0:
            self.duration -= 1

        return [self.joy_motion]

    def is_complete(self) -> bool:
        if self.duration > 0:
            return False
        return True

    def reset(self):
        self.duration = self.initial_duration
