from abc import abstractmethod

from xumes.test_automation.test_runner import TestRunner


class Behavior:

    def __init__(self):
        self._test_runner: TestRunner = None
        self._mode = None
        self._logging = False

    def set_mode(self, mode: str):
        self._mode = mode

    def set_test_runner(self, test_runner):
        self._test_runner = test_runner

    @property
    def context(self):
        return self._test_runner.get_context()

    @property
    def test_runner(self):
        return self._test_runner

    def set_do_logging(self, do_logging: bool):
        """
        Sets the logging mode.

        Args:
            do_logging: True to enable logging, otherwise False.
        """
        self._logging = do_logging

    @abstractmethod
    def execute(self, feature, scenario):
        """
        Execute the behavior algorithm.
        """
        raise NotImplementedError

    @abstractmethod
    def terminated(self) -> bool:
        """
        Check if the game has terminated.
        """
        raise NotImplementedError
