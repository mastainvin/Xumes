from typing import Generic, TypeVar

ST = TypeVar("ST")


class GameElementState(Generic[ST]):
    """
        The `GameElementState` class represents the state of a game element.

        Attributes:
            _state: The state object representing the game element state.
            _type: The type of the game element.
            _name: The name of the game element.

        Methods:
            state: Property representing the game element state.
            name: Property representing the name of the game element.
            type: Property representing the type of the game element.
    """
    def __init__(self, name: str, element_type: str, state_obj: ST):
        self._state: ST = state_obj
        self._type = element_type
        self._name = name

    @property
    def state(self) -> ST:
        return self._state

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self):
        return self._type
