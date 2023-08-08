class ICommunicationServiceGame:
    """
      The `ICommunicationServiceGame` interface provides methods for communication between the game and the training server.

      Methods:
          observe: Send the game state to the training server.
          action: Wait for the training server to send an action.
          run: Start the communication service (e.g., start the app of a REST API).
    """

    def observe(self, game_service) -> None:
        """
        Send the game state to the training server.
        :param game_service: GameService object.
        """
        raise NotImplementedError

    def action(self, game_service) -> None:
        """
        Wait the training server to send an action.
        :param game_service: GameService object.
        """
        raise NotImplementedError

    def run(self, game_service) -> None:
        """
        Used to start the communication service (using threads).
        For example: start the app of a REST API.
        :param game_service: GameService object.
        """
        raise NotImplementedError

    def stop(self) -> None:
        """
        Used to stop the communication service.
        """
        raise NotImplementedError
