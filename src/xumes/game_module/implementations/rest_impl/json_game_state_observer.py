import json
from typing import Dict

from xumes.game_module.i_game_state_observer import IGameStateObserver


class JsonGameStateObserver(Dict, IGameStateObserver):
    instance = None

    def update_state(self, obs) -> None:
        self[obs.name] = obs.state().state

        def base_class():
            for base in obs.object.__class__.__bases__:
                if base.__name__ != "ABC" and base.__name__ != obs.object.__class__.__name__:
                    return base.__name__
                return "error"

        self[obs.name]['__type__'] = base_class()

    def remove_state(self, obs):
        if id(obs.object) in self.keys():
            self.pop(id(obs.object))

    def get_state(self):
        state = json.dumps(self)
        self.clear()
        return state

    @classmethod
    def get_instance(cls):
        if JsonGameStateObserver.instance is None:
            JsonGameStateObserver.instance = JsonGameStateObserver()
        return JsonGameStateObserver.instance

    def __hash__(self):
        return id(self).__hash__()