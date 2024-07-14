from abc import abstractmethod

from xumes import Imitator


class Imitable:

    @abstractmethod
    def imitator(self) -> Imitator:
        """
        Returns the imitator to be used in the imitation learning process.
        Returns: The imitator.
        """
        pass
