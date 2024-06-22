from xumes.modules.godot.input.event import Event


class Action(Event):
    def __init__(self, name):
        super().__init__('ACTION_EVENT')
        self['action_name'] = name
