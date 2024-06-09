from abc import abstractmethod

from xumes.test_automation.test_runner import TestRunner


class Behavior:

    def __init__(self):
        self._test_runner: TestRunner = None
        self._mode = None

    def set_mode(self, mode: str):
        self._mode = mode

    def set_test_runner(self, test_runner):
        self._test_runner = test_runner

    def test_runner(self):
        return self._test_runner

    @abstractmethod
    def execute(self, feature, scenario):
        """
        Execute the behavior algorithm.
        """
        raise NotImplementedError

    def __getattr__(self, item):
        """
        Retrieves an entity from the game service.
        """
        return self._test_runner.get_entity(item)

    @abstractmethod
    def terminated(self) -> bool:
        """
        Check if the game has terminated.
        """
        raise NotImplementedError
