from typing import Any, Dict


class ICommunicationServiceGame:
    """
      Communication between the test_runner and the game.
      Methods:
          observe: Send the game state to the training server.
          action: Wait for the training server to send an action.
          run: Start the communication service (e.g., start the app of a REST API).
    """

    def get_state(self) -> Dict[str, Any]:
        """
        Receive the game state from the server.
        """
        raise NotImplementedError

    def push_action(self, action) -> None:
        """
        Send an action to the game.
        """
        raise NotImplementedError

    def push_event(self, event) -> None:
        """
        Push event to the game.
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

    def given(self) -> None:
        """
        Send the given step to the training server.
        """
        raise NotImplementedError

    def when(self) -> None:
        """
        Send the when step to the training server.
        """
        raise NotImplementedError

    def then(self) -> None:
        """
        Send the then step to the training server.
        """
        raise NotImplementedError
