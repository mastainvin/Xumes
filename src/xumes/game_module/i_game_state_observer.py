from typing import Generic, TypeVar

ST = TypeVar("ST")


class IGameStateObserver(Generic[ST]):
    """
       The `IGameStateObserver` interface defines the methods for observing and interacting with game state observables.

       Methods:
           update_state: Update or add an observable inside the observer.
           remove_state: Remove an observable from the collection.
           get_state: Get the changes between the last retrieval of state and now.
    """
    def update_state(self, obs) -> None:
        """
        Update or add an observable inside the observer.
        If the observation has not changed we don't update the
        collection.
        TODO - Add a parameter to update only a specific attribute change.
        As this: update_state(obs, "attribute_name")
        Then we update state only for this attribute.

        :param obs: StateObservable object.
        """
        raise NotImplementedError

    def remove_state(self, obs) -> None:
        """
        Remove an observable of the collection.
        :param obs: StateObservable object.
        """
        raise NotImplementedError

    def get_state(self) -> ST:
        """
        Get the changes between the last time we retrieve the
        state and now.
        """
        raise NotImplementedError

    def __hash__(self):
        """
        Every game state observer has to be hashable.
        :return: A hash of the object
        """
        raise NotImplementedError



