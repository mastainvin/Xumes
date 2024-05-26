from abc import abstractmethod
from typing import List

from xumes.behavior.entity_manager import AutoEntityManager
from xumes.behavior.implementations.json_impl.json_game_element_state_converter import JsonGameElementStateConverter
from xumes.test_runner.driver import Driver
from xumes.test_runner.i_communication_service import ICommunicationService


class Behavior:
    pass


class TestRunner:
    """
    The `TestRunner` class is a central component of Xumes. It manages communication between communication service,
    the execution of the game itself, and external events that can modify the game state.

    Attributes:
        communication_service (ICommunicationService): An object responsible for communication with other the training service.

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
                 communication_service: ICommunicationService,
                 ):
        self.communication_service = communication_service
        self._entity_manager = AutoEntityManager(JsonGameElementStateConverter())
        self.is_finished = False
        self.driver = Driver()

    def get_entity(self, name):
        try:
            return self._entity_manager.get(name)
        except KeyError:
            return None

    def get_entity_manager(self):
        return self._entity_manager

    def run_communication_service(self, port: int):
        self.communication_service.init_socket(port)

    def run(self, port: int):
        self.run_communication_service(port)

    def stop(self):
        self.communication_service.stop_socket()

    def finish(self):
        self.communication_service.push_dict({"event": "stop"})
        self.communication_service.get_int()

    def push_methods(self, methods: List):
        self.communication_service.push_dict({"event": "methods", "methods": methods})
        # self.communication_service.get_int()

    def push_actions_and_get_state(self, actions: List):
        methods = self.driver()
        data = {"event": "action", "inputs": actions, "methods": methods}
        # print(data)
        self.communication_service.push_dict(data)
        return self.communication_service.get_dict()

    def get_state(self):
        self.communication_service.push_dict({"event": "get_state"})
        return self.communication_service.get_dict()

    def get_steps(self):
        self.communication_service.push_dict({"event": "get_steps"})
        return self.communication_service.get_dict()

    def push_args(self, args):
        self.communication_service.push_dict({"event": "args", "args": args})
        self.communication_service.get_int()

    def reset(self):
        self.communication_service.push_dict({"event": "reset"})
        self.communication_service.get_int()

    def __getattr__(self, item):
        return self.get_entity(item)

    @abstractmethod
    def config(self):
        """
        Configures the game environment.
        """
        raise NotImplementedError

    @abstractmethod
    def given(self):
        raise NotImplementedError

    @abstractmethod
    def when(self) -> Behavior:
        raise NotImplementedError

    @abstractmethod
    def then(self):
        raise NotImplementedError

    @abstractmethod
    def episode_finished(self) -> bool:
        raise NotImplementedError
