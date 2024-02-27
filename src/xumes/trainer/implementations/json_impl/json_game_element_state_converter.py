from typing import Tuple

from xumes.trainer.game_element_state import GameElementState
from xumes.trainer.i_game_element_state_converter import IGameElementStateConverter


class JsonGameElementStateConverter(IGameElementStateConverter):

    def convert(self, state_wrapper: Tuple) -> GameElementState:
        name, content = state_wrapper
        if isinstance(content, dict):
            if "__type__" in content:
                element_type = content["__type__"]
                state = {}
                for k in content:
                    state[k] = content[k]

                return GameElementState(name=name, element_type=element_type, state_obj=state)

        return GameElementState(name=name, element_type="unknown", state_obj=content)

