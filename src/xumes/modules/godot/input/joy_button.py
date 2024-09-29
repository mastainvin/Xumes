from enum import Enum

from xumes.modules.godot.input.event import Event

class JoyKey(Enum):
    A = "A"
    B = "B"
    X = "X"
    Y = "Y"


class JoyButton(Event):

    def __init__(self, button: JoyKey):
        super().__init__('JOY_BUTTON_EVENT')
        self['button'] = button.value
