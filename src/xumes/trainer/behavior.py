from abc import abstractmethod

from xumes.test_runner.test_runner import TestRunner
from xumes.trainer.entity_manager import AutoEntityManager
from xumes.trainer.game_service import GameService
from xumes.trainer.implementations.json_impl.json_game_element_state_converter import JsonGameElementStateConverter


class Behavior:

    def __init__(self):
        self._game_service: GameService = None
        self._mode = None

    def set_mode(self, mode: str):
        self._mode = mode

    def set_game_service(self, test_runner: TestRunner):
        self._game_service = GameService(AutoEntityManager(JsonGameElementStateConverter()), test_runner)

    def game_service(self):
        return self._game_service

    @abstractmethod
    def execute(self, feature, scenario):
        """
        Execute the behavior algorithm.
        """
        raise NotImplementedError
