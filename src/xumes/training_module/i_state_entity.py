from typing import TypeVar

ST = TypeVar("ST")


class IStateEntity:
    """
    The `IStateEntity` interface defines the methods for managing the state of an entity in the game.

    Methods:
        update: Updates the entity's attributes from a state.
        build: Builds an `IStateEntity` object from a state.
    """
    def update_state(self, state: ST):
        """
        Updates his attributes from a state.
        :param state: representation of the updates.
        """
        raise NotImplementedError

    @staticmethod
    def build(state: ST):
        """
        Build a IStateEntity from a state (initiate attributes).
        :param state: representation of the first state of the game object.
        """
        raise NotImplementedError
