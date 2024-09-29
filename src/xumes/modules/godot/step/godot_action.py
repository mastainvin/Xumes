from typing import List

from xumes import TestStep, Input
from xumes.modules.godot.input.event import Event


class GodotEventStep(TestStep):

    def __init__(self, event: Event):
        super().__init__()
        self.event = event
        self.event_performed = False


    def step(self) -> List[Input]:
        actions = [self.event]
        self.event_performed = True
        return actions

    def is_complete(self) -> bool:
        return self.event_performed

    def reset(self):
        self.event_performed = False
