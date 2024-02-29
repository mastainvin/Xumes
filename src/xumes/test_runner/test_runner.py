from abc import abstractmethod
from typing import List
from xumes.test_runner.i_communication_service_game import ICommunicationServiceGame


class TestRunner:
    """
    The `TestRunner` class is a central component of Xumes. It manages communication between communication service,
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
        self.communication_service = communication_service
        self.is_finished = False

    def run_communication_service(self, port: int):
        self.communication_service.init_socket(port)

    def run(self, port: int):
        self.run_communication_service(port)

    def stop(self):
        self.communication_service.stop_socket()

    def finish(self):
        self.communication_service.push_dict({"event": "finish"})
        self.communication_service.get_int()

    def push_actions_and_get_state(self, actions: List):
        self.communication_service.push_dict({"event": "action", "inputs": actions})
        return self.communication_service.get_dict()

    def get_state(self):
        self.communication_service.push_dict({"event": "get_state"})
        return self.communication_service.get_dict()

    def given(self):
        self.communication_service.push_dict({"event": "given"})
        self.communication_service.get_int()

    def when(self):
        self.communication_service.push_dict({"event": "when"})
        self.communication_service.get_int()

    def then(self):
        self.communication_service.push_dict({"event": "then"})
        return self.communication_service.get_dict()

    def get_steps(self):
        self.communication_service.push_dict({"event": "get_steps"})
        return self.communication_service.get_dict()

    def push_args(self, args):
        self.communication_service.push_dict({"event": "args", "args": args})
        self.communication_service.get_int()

    @abstractmethod
    def episode_finished(self) -> bool:
        raise NotImplementedError
