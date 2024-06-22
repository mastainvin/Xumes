from xumes.modules.godot.input.event import Event


class JoyMotion(Event):

    def __init__(self, axis, value):
        super().__init__('JOY_MOTION_EVENT')
        self['axis'] = axis
        self['axis_value'] = value
