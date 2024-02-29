import logging
from abc import abstractmethod, ABC
from typing import TypeVar, final, List

from xumes.trainer.entity_manager import EntityManager
from xumes.trainer.i_trainer import ITrainer
from xumes.test_runner.test_runner import TestRunner

OBST = TypeVar("OBST")


class TrainingService:
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

    def __init__(self,
                 entity_manager: EntityManager,
                 test_runner: TestRunner
                 ):
        self._entity_manager = entity_manager
        self._test_runner = test_runner

    @final
    def reset(self):
        self._test_runner.when()

    @final
    def push_actions(self, actions):
        logging.debug(f"Pushing actions: {actions}")
        self._test_runner.push_actions(actions)

    @final
    def push_action_and_get_state(self, actions):
        logging.debug(f"Pushing actions: {actions}")
        states = self._test_runner.push_actions_and_get_state(actions)
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._entity_manager.convert(state)

    @final
    def on_episode_end(self):
        self._test_runner.episode_finished()

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
            self._entity_manager.convert(state)

    @final
    @property
    def game_state(self):
        return self._entity_manager.game_state

    @final
    def get_entity(self, name: str):
        try:
            return self._entity_manager.get(name)
        except KeyError:
            return None

    def __getattr__(self, item):
        return self.get_entity(item)


class MarkovTrainingService(TrainingService, ITrainer, ABC):  # TODO Move class to implementations folder

    @final
    def reward(self):
        return self.convert_reward()

    @final
    def terminated(self):
        return self.convert_terminated() or self._entity_manager.game_state == "reset" or self._entity_manager.game_state == "random_reset"

    @final
    def push_raw_actions(self, actions):
        self.push_actions(actions=self.convert_actions(actions))

    @final
    def get_obs(self) -> OBST:
        self.retrieve_state()
        return self.convert_obs()

    @final
    def push_actions_and_get_obs(self, actions) -> OBST:
        self.push_action_and_get_state(self.convert_actions(actions))
        return self.convert_obs()

    @abstractmethod
    def convert_obs(self) -> OBST:
        raise NotImplementedError

    @abstractmethod
    def convert_reward(self) -> float:
        raise NotImplementedError

    @abstractmethod
    def convert_terminated(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def convert_actions(self, raws_actions) -> List[str]:
        raise NotImplementedError
