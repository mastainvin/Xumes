from abc import abstractmethod

from xumes.behavior.game_service import GameService


class Behavior:

    def __init__(self):
        self._game_service: GameService = None
        self._mode = None

    def set_mode(self, mode: str):
        self._mode = mode

    def set_game_service(self, test_runner):
        self._game_service = GameService(test_runner)

    def game_service(self):
        return self._game_service

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
        return self._game_service.get_entity(item)

    @abstractmethod
    def terminated(self) -> bool:
        """
        Check if the game has terminated.
        """
        raise NotImplementedError
