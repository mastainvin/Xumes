from typing import List

from xumes import TestStep, Input
from xumes.modules.godot.input.joy_button import JoyButton


class GodotJoyActionStep(TestStep):
    def __init__(self, action_key, duration=1):
        super().__init__()
        self.action_key = action_key
        self.action_performed = False

    def step(self) -> List[Input]:
        actions = [JoyButton(self.action_key)]
        self.action_performed = True
        return actions

    def is_complete(self) -> bool:
        return self.action_performed

    def reset(self):
        self.action_performed = False
