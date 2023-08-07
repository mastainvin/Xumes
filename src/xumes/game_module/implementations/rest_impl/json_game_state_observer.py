import json
from typing import Dict

from xumes.game_module.i_game_state_observer import IGameStateObserver


class JsonGameStateObserver(Dict, IGameStateObserver):
    instance = None

    def update_state(self, obs) -> None:
        state = obs.state()
        if obs.name not in self.keys():
            self[obs.name] = state.state
        else:
            self[obs.name].update(state.state)

        def base_class():
            if obs.__class__.__name__ != obs.object.__class__.__name__:
                return obs.object.__class__.__name__
            for base in obs.__class__.__bases__:
                if base.__name__ != "ABC" and base.__name__ != obs.__class__.__name__:
                    return base.__name__
                return "error"

        if isinstance(self[obs.name], dict):
            self[obs.name]['__type__'] = base_class()

    def remove_state(self, obs):
        if id(obs.object) in self.keys():
            self.pop(id(obs.object))

    def get_state(self):
        state = json.dumps(self)
        self.clear()
        return state

    @staticmethod
    def get_instance():
        if JsonGameStateObserver.instance is None:
            JsonGameStateObserver.instance = JsonGameStateObserver()
        return JsonGameStateObserver.instance

    def __hash__(self):
        return id(self).__hash__()
