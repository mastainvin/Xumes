from xumes.modules.godot.input.event import Event


class MouseMotion(Event):

    def __init__(self, position):
        super().__init__('MOUSE_MOTION_EVENT')
        self['position'] = position
