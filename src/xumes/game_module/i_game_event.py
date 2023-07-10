

class IGameEvent:
    """
       The `IGameEvent` interface defines methods for adapting button press and release functions.

       Methods:
           press: Adapt the press function of a button.
           release: Adapt the release function of a button.
    """
    def press(self) -> None:
        """
        Method used to adapt the press function of a button.
        """
        raise NotImplementedError

    def release(self) -> None:
        """
        Method used to adapt the release function of a button.
        """
        raise NotImplementedError

