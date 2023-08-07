class ICommunicationServiceTestManager:

    def connect_trainer(self, test_manager, scenario) -> None:
        raise NotImplementedError

    def disconnect_trainer(self, test_manager, scenario) -> None:
        raise NotImplementedError

    def start_training(self, test_manager) -> None:
        raise NotImplementedError

    def reset(self, test_manager) -> None:
        raise NotImplementedError

    def run(self, test_manager) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        """
        Used to stop the communication service.
        """
        raise NotImplementedError
