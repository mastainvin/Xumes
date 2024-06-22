from xumes.test_automation.input import Input


class Event(Input):
    def __init__(self, event_type):
        super().__init__()
        self['type'] = event_type

