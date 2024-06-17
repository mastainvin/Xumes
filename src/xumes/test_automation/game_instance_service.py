from typing import List

from xumes.communication.i_com_game_instance import IComGameInstance


class Behavior:
    pass


class GameInstanceService:
    """
    The `TestRunner` class is a central component of Xumes. It manages communication between communication service,
    the execution of the game itself, and external events that can modify the game state.

    Attributes:
        communication_service (IComGameInstance): An object responsible for communication with other the training service.

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
                 communication_service: IComGameInstance,
                 ):
        self.communication_service = communication_service
        self.is_finished = False

    def run(self, port: int):
        self.communication_service.init_socket(port)

    def stop(self):
        self.communication_service.stop_socket()

    def finish(self):
        self.communication_service.push_dict({"event": "stop"})
        self.communication_service.get_int()

    def push_actions_and_get_state(self, actions: List, methods):
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
