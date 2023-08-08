from typing import TypeVar

from xumes.training_module.game_element_state import GameElementState

SW = TypeVar("SW")


class IGameElementStateConverter:
    """
      The `IGameElementStateConverter` interface defines the method for converting a state element
      to a game element state.

      Methods:
          convert: Converts a state element to a game element state.
    """
    def convert(self, state_wrapper: SW) -> GameElementState:  # TODO add type to state_wrapper
        """
        Converts a state element to a game element state.
        A game element state is easier to work with in order the build entities.
        :param state_wrapper: element of the game state list.
        :returns: A `GameElementState` object representing the converted game element state.
        """
        raise NotImplementedError
