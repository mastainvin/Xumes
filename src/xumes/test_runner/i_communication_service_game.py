from typing import Any, Dict


class ICommunicationServiceGame:
    """
      Communication between the test_runner and the game.
      Methods:
          observe: Send the game state to the training server.
          action: Wait for the training server to send an action.
          run: Start the communication service (e.g., start the app of a REST API).
    """

    def push_dict(self, dictionary) -> None:
        """
        Send a dictionary to the game.
        """
        raise NotImplementedError

    def get_dict(self) -> Dict[str, Any]:
        """
        Receive a dictionary from the game.
        """
        raise NotImplementedError

    def get_int(self) -> int:
        """
        Receive an integer from the game.
        """
        raise NotImplementedError

    def init_socket(self, port) -> None:
        """
        Used to start the communication service (using threads).
        For example: start the app of a REST API.
        """
        raise NotImplementedError

    def stop_socket(self) -> None:
        """
        Used to stop the communication service.
        """
        raise NotImplementedError

