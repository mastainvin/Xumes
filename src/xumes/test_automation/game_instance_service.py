from typing import List

from xumes.communication.i_com_game_instance import IComGameInstance


class Behavior:
    pass


class GameInstanceService:
    """
    Class responsible for the communication between the game instance and the test automation.
    Used by the test runner to interact with the game instance.
    Attributes:
        - communication_service (IComGameInstance): The communication service.
        - is_finished (bool): A flag indicating if the game instance is finished.
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
