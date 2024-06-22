from xumes.modules.godot.input.event import Event


class JoyButton(Event):

    def __init__(self, button):
        super().__init__('JOY_BUTTON_EVENT')
        self['button'] = button
