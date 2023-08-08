from __future__ import annotations

from abc import ABC, abstractmethod
from typing import final, List, TypeVar

from xumes.game_module.implementations.rest_impl.json_game_state_observer import JsonGameStateObserver
from xumes.game_module.state_observable import State, ComposedGameStateObservable, InheritedGameStateObservable

OBJ = TypeVar("OBJ")


# decorator for notifying observers
def update_state_decorator(func, name):
    def wrapper(self, *arg, **kw):
        res = func(self, *arg, **kw)
        self.update_state(name)
        return res

    return wrapper


class TestRunner(ABC):
    """
       The `TestRunner` class is an abstract base class for implementing game test loop functionality and managing game state.

       Attributes:
            _test_client: The client object associated with the test runner.
            _observer: The observer associated with the test runner.
       Methods:
           update_state(state): Notifies changes in the game state. This method should be used when overloading game methods.
           set_client(client): Sets the client object for the test runner.
           run_test(): Runs a game loop without rendering. The game loop should start with `self.test_client.wait()`.
           run_test_render(): Runs a game loop with rendering. The game loop should start with `self.test_client.wait()`.
           random_reset(): Performs a random reset in the game, starting from a random state.
           reset(): Performs a reset from the beginning of the game.
           delete_screen(): Deletes the screen if the game engine supports it.
       """

    def __init__(self, observer=JsonGameStateObserver.get_instance()):
        self._observer = observer
        self._test_client = None

    @property
    @final
    def test_client(self):
        return self._test_client

    @final
    def set_client(self, client):
        self._test_client = client
        client.observer = self._observer

    @final
    def bind(self, observable_object: OBJ, name: str,
             state: List[State] | State | str | List[str] | None = None) -> ComposedGameStateObservable:
        """
        Add an observable object to the test runner.
        :param observable_object: the observable object to add.
        :param name: the name of the observable object.
        :param state: the state of the observable object.
        """
        return ComposedGameStateObservable(observable_object, name, [self._observer], state)

    @final
    def create(self, observable_class, name: str, state: List[State] | State | str | List[str] | None = None, *args,
               **kwargs):
        """
        Create an observable object from a class.
        :param observable_class: the class to create an observable object from.
        :param name: the name of the observable object.
        :param state: the state of the observable object.
        """
        observers = [self._observer]
        return InheritedGameStateObservable.create(observable_class, name, state, observers, *args, **kwargs)

    @abstractmethod
    def run_test(self) -> None:
        """
        Run a game loop without rendering.\n
        The game loop has to start with : self.test_client.wait()
        """
        raise NotImplementedError

    @abstractmethod
    def run_test_render(self) -> None:
        """
        Run a game loop with rendering.\n
        The game loop has to start with : self.test_client.wait()
        """
        raise NotImplementedError

    @abstractmethod
    def random_reset(self) -> None:
        """
        Perform a random reset in the game. A random reset,
        is a reset from a random state of the game and not from the beginning.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        Perform a reset from the beginning of the game.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_screen(self) -> None:
        """
        If the game engine able it, implement a way to delete the
        screen.
        """
        raise NotImplementedError
