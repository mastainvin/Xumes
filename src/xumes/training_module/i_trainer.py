from abc import abstractmethod
from typing import Optional


class ITrainer:

    @abstractmethod
    def train(self, save_path: str = None, eval_freq: int = 10000, logs_path: Optional[str] = None, logs_name: Optional[str] = None, previous_model_path: Optional[str] = None):
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
    def play(self, timesteps: Optional[int] = None):
        """
        Use the algorithm not in training mode.
        :param timesteps: Number maximum of step (action to perform).
        """
        raise NotImplementedError
