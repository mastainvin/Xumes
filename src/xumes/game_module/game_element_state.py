from typing import Generic, TypeVar

ST = TypeVar("ST")


class GameElementState(Generic[ST]):
    """
    The `GameElementState` class represents the state of a game element.

    Attributes:
        _state: The state object representing the game element state.

    Methods:
        state: Property representing the game element state.
    """
    def __init__(self, state_obj: ST):
        self._state: ST = state_obj

    @property
    def state(self) -> ST:
        return self._state
