import logging
from typing import TypeVar, final

OBST = TypeVar("OBST")


class TestRunner:
    pass


class GameService:
    """
    The `TrainingService` class is responsible for managing the training process of a game.

    Attributes:
        _entity_manager: An instance of `EntityManager` responsible for managing game entities.
        _test_runner: An instance of `TestRunner` responsible for managing the game test loop.

    Methods:
        train(): Implementation of the training algorithm.
        save(path): Saves the training model to a file specified by the `path`.
        load(path): Loads a training model from a file specified by the `path`.
        play(timesteps): Uses the algorithm in non-training mode for a specified number of `timesteps`.
        random_reset(): Requests a random reset of the game through the communication service.
        reset(): Requests a reset of the game through the communication service.
        push_actions(actions): Pushes a list of `actions` to the communication service.
        retrieve_state(): Calls the game service to retrieve and update the game state.
        game_state: Property representing the game state from the entity manager.
        get_entity(name): Retrieves an entity from the entity manager by `name`.
    """

    def __init__(self, test_runner: TestRunner):
        self._test_runner = test_runner

    @final
    def reset(self):
        self._test_runner.given()
        self._test_runner.reset()

    # @final
    # def push_actions(self, actions):
    #     logging.debug(f"Pushing actions: {actions}")
    #     self._test_runner.push_actions(actions)

    @final
    def push_action_and_get_state(self, actions):
        logging.debug(f"Pushing actions: {actions}")
        states = self._test_runner.push_actions_and_get_state(actions)
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._test_runner.get_entity_manager().convert(state)

    @final
    def episode_finished(self):
        return self._test_runner.episode_finished()

    @final
    def finished(self):
        return self._test_runner.finish()

    @final
    def retrieve_state(self) -> None:
        """
        Call the game service and update the state.
        """
        # self._test_runner.run_loop()
        states = self._test_runner.get_state()
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._test_runner.get_entity_manager().convert(state)

    @final
    @property
    def game_state(self):
        return self._test_runner.get_entity_manager()

    def __getattr__(self, item):
        return self.get_entity(item)

    def get_entity(self, name):
        return self._test_runner.get_entity(name)
