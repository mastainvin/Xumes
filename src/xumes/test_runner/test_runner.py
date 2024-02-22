from typing import List
from xumes.test_runner.i_communication_service_game import ICommunicationServiceGame


class TestRunner:
    """
    The `GameService` class is a central component of Xumes. It manages communication between communication service,
    the execution of the game itself, and external events that can modify the game state.

    Attributes:
        communication_service (ICommunicationServiceGame): An object responsible for communication with other the training service.

    Methods:
        run_communication_service(): Starts the communication service thread.
        run_test_runner(run_func): Starts the game loop if this is the main thread. `run_func` is the game loop function to execute.
        run(): Executes the game by starting both the communication service and the game loop.
        run_render(): Similar to `run()`, but runs the game loop with rendering.
        stop(): Stops both threads currently running.
        wait(): The first method executed in the game loop. It allows the game to wait for an event sent by the training service.
        update_event(event): Method used to accept external modifications to the game, such as reset. `event` represents an external event that can modify the game state.
    """

    def __init__(self,
                 communication_service: ICommunicationServiceGame,
                 ):

        self.inputs = []

        self.communication_service = communication_service

        self.is_finished = False

    def run_communication_service(self, port: int):
        self.communication_service.init_socket(port)

    def run(self, port: int):
        """
        - The communication service thread, used to send state and get actions.\n
        """
        self.run_communication_service(port)

    def stop(self):
        """
        Stop the communication service.
        """
        self.communication_service.stop_socket()

    def reset(self):
        self.communication_service.push_event("reset")

    def finish(self):
        self.communication_service.push_event("finish")

    def push_actions(self, actions: List):
        self.communication_service.push_action(actions)

    def get_state(self):
        return self.communication_service.get_state()

