import logging
from abc import abstractmethod, ABC
from typing import TypeVar, final

from xumes.training_module.entity_manager import EntityManager
from xumes.training_module.i_communication_service_training import ICommunicationServiceTraining

OBST = TypeVar("OBST")


class TrainingService:
    """
    The `TrainingService` class is responsible for managing the training process of a game.

    Attributes:
        _entity_manager: An instance of `EntityManager` responsible for managing game entities.
        _communication_service: An object implementing the `ICommunicationServiceTraining` interface for communication.

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
                 communication_service: ICommunicationServiceTraining,
                 ):
        self._entity_manager = entity_manager
        self._communication_service = communication_service

    @abstractmethod
    def train(self, save_path: str = None, eval_freq: int = 10000):
        """
        Implementation of the training algorithm.
        """
        raise NotImplementedError

    @abstractmethod
    def save(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def load(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def play(self, timesteps: int):
        """
        Use the algorithm not in training mode.
        :param timesteps: Number maximum of step (action to perform).
        """
        raise NotImplementedError

    @final
    def random_reset(self):
        self._communication_service.push_event("random_reset")

    @final
    def reset(self):
        self._communication_service.push_event("reset")

    @final
    def push_actions(self, actions):
        logging.debug(f"Pushing actions: {actions}")
        self._communication_service.push_actions(actions)

    @final
    def retrieve_state(self) -> None:
        """
        Call the game service and update the state.
        """
        states = self._communication_service.get_states()
        logging.debug(f"Received states: {states}")
        for state in states:
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


class MarkovTrainingService(TrainingService, ABC):  # TODO Move class to implementations folder

    @abstractmethod
    def get_obs(self) -> OBST:
        """
        Method needed in the Markov Decision Process.
        Convert game state to observation.
        """
        raise NotImplementedError

    @abstractmethod
    def reward(self) -> float:
        """
        Method needed in the Markov Decision Process.
        Convert game state to reward.
        """
        raise NotImplementedError

    @abstractmethod
    def push_raw_actions(self, actions):
        """
        Method needed in the Markov Decision Process.
        Convert actions (ex: list of int), to list of str.
        :param actions: Any type of actions.
        """
        raise NotImplementedError

    @abstractmethod
    def terminated(self) -> bool:
        """
        Method needed in the Markov Decision Process.
        Get if the episode is terminated from the game state.
        """
        raise NotImplementedError
