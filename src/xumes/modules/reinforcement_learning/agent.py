from abc import ABC, abstractmethod
from typing import TypeVar, List, Optional

from xumes.core.model_helper import trainer_name, model_path
from xumes.core.modes import TEST_MODE, TRAIN_MODE
from xumes.behavior.behavior import Behavior
from xumes.modules.reinforcement_learning.i_trainer import ITrainer
from xumes.modules.reinforcement_learning.stable_baselines_trainer import StableBaselinesTrainer

OBST = TypeVar("OBST")


class Agent(Behavior, ABC):
    """
    The `Agent` class represents a machine learning agent that interacts with the game.

    Attributes:
        - `_save_path` (str): The path to save the trained model.
        - `_eval_freq` (int): The evaluation frequency during training.
        - `_logs_path` (Optional[str]): The path to save training logs.
        - `_logs_name` (Optional[str]): The name of the log files.
        - `_previous_model_path` (Optional[str]): The path to a pre-trained model, if available.
    """

    def __init__(self, save_path: str = None, eval_freq: int = 1000, logs_path: Optional[str] = None,
                 logs_name: Optional[str] = None, previous_model_path: Optional[str] = None, **kwargs):
        super().__init__()
        self._trainer: ITrainer = StableBaselinesTrainer(self, **kwargs)

        self._save_path = save_path
        self._eval_freq = eval_freq
        self._logs_path = logs_path
        self._logs_name = logs_name
        self._previous_model_path = previous_model_path

    def get_trainer_info(self):
        return {
            "eval_freq": self._eval_freq,
            "logs_path": self._logs_path,
            "logs_name": self._logs_name,
            "previous_model_path": self._previous_model_path
        }

    def get_trainer(self) -> ITrainer:
        """
        Returns the agent's behavior.
        """
        return self._trainer

    def get_path(self) -> str:
        """
        Returns the agent's model save path.
        """
        return self._save_path

    def execute(self, feature, scenario):
        """
        Executes the training or testing process based on the current mode (TRAIN_MODE or TEST_MODE).

        Args:
            feature: The specific feature to use.
            scenario: The specific scenario to use.
        """
        if not self._trainer:
            raise Exception("Trainer not set")

        _path = self._save_path
        if not _path:
            _path = model_path(feature, scenario)
        else:
            _path = _path + "/" + feature.name + "/" + scenario.name

        if self._mode == TRAIN_MODE:
            self._trainer.train(_path + "/" + trainer_name(feature, scenario), self._eval_freq, self._logs_path,
                                self._logs_name, self._previous_model_path)
            self._trainer.free()
        elif self._mode == TEST_MODE:
            self._trainer.load(_path + "/" + trainer_name(feature, scenario) + "/best_model")
            self._trainer.play()
            self._trainer.free()

    def predict(self, observation):
        """
        Predicts the next action based on the given observation.

        Args:
            observation: The observation to predict the next action.

        Returns:
            The predicted action.
        """
        return self._trainer.predict(observation)

    @abstractmethod
    def observation(self) -> OBST:
        """
        Abstract method to obtain observations from the environment.

        Returns:
            OBST: The observations from the environment.
        """
        raise NotImplementedError

    @abstractmethod
    def reward(self) -> float:
        """
        Abstract method to obtain the agent's current reward.

        Returns:
            float: The current reward.
        """
        raise NotImplementedError

    @abstractmethod
    def terminated(self) -> bool:
        """
        Abstract method to check if the episode is terminated.

        Returns:
            bool: True if the episode is terminated, otherwise False.
        """
        raise NotImplementedError

    @abstractmethod
    def actions(self, raws_actions) -> List[str]:
        """
        Abstract method to obtain the list of possible actions for the agent.

        Args:
            raws_actions: The raw actions to process.

        Returns:
            List[str]: The list of possible actions.
        """
        raise NotImplementedError
