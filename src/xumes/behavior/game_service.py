import logging
from typing import TypeVar, final

OBST = TypeVar("OBST")


class TestRunner:
    pass


class GameService:
    """
    The GameService class is responsible for managing the game state and interacting with the TestRunner.

    Attributes:
        _test_runner (TestRunner): An instance of the TestRunner class.
    """

    def __init__(self, test_runner: TestRunner):
        """
        The constructor for the GameService class.

        Parameters:
            test_runner (TestRunner): An instance of the TestRunner class.
        """
        self._test_runner = test_runner

    @final
    def reset(self):
        """
        Resets the game state by calling the given and reset methods of the TestRunner instance.
        """
        self._test_runner.given()
        self._test_runner.reset()

    @final
    def push_action_and_get_state(self, actions):
        """
        Pushes actions to the TestRunner and retrieves the game state.

        Parameters:
            actions: The actions to be pushed to the TestRunner.
        """
        logging.debug(f"Pushing actions: {actions}")
        states = self._test_runner.push_actions_and_get_state(actions)
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._test_runner.get_entity_manager().convert(state)

    @final
    def episode_finished(self):
        """
        Checks if the episode has finished by calling the episode_finished method of the TestRunner instance.

        Returns:
            bool: True if the episode has finished, False otherwise.
        """
        return self._test_runner.episode_finished()

    @final
    def finished(self):
        """
        Checks if the game has finished by calling the finish method of the TestRunner instance.

        Returns:
            bool: True if the game has finished, False otherwise.
        """
        return self._test_runner.finish()

    @final
    def retrieve_state(self) -> None:
        """
        Retrieves the game state by calling the get_state method of the TestRunner instance.
        """
        # self._test_runner.run_loop()
        states = self._test_runner.get_state()
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._test_runner.get_entity_manager().convert(state)

    @final
    @property
    def game_state(self):
        """
        Retrieves the game state by calling the get_entity_manager method of the TestRunner instance.

        Returns:
            The current game state.
        """
        return self._test_runner.get_entity_manager()

    def __getattr__(self, item):
        """
        Retrieves an entity by calling the get_entity method with the given item as parameter.

        Parameters:
            item: The name of the entity to be retrieved.

        Returns:
            The entity with the given name.
        """
        return self.get_entity(item)

    def get_entity(self, name):
        """
        Retrieves an entity by calling the get_entity method of the TestRunner instance with the given name as parameter.

        Parameters:
            name: The name of the entity to be retrieved.

        Returns:
            The entity with the given name.
        """
        return self._test_runner.get_entity(name)
