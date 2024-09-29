from enum import Enum

from xumes.modules.godot.input.event import Event

class JoyAxis(Enum):
    LEFT_X = "LEFT_X"
    LEFT_Y = "LEFT_Y"
    RIGHT_X = "RIGHT_X"
    RIGHT_Y = "RIGHT_Y"

class JoyMotion(Event):

    def __init__(self, axis: JoyAxis, value: float):
        super().__init__('JOY_MOTION_EVENT')
        self['axis'] = axis.value
        self['axis_value'] = value
