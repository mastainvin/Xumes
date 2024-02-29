import json
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep
from typing import Dict, Any

from xumes.core.utils import parse_json_with_eval
from xumes.test_runner.i_communication_service_game import ICommunicationServiceGame


class CommunicationServiceGameSocket(ICommunicationServiceGame):

    def __init__(self, host: str):
        self.host = host
        self.socket = None
        self.addr = None
        self.is_running = False

    def push_dict(self, dictionary) -> None:
        if self.is_running:
            self.socket.sendall(json.dumps(dictionary).encode())

    def get_dict(self) -> Dict[str, Any]:
        data = {}
        if self.is_running:
            data = self.socket.recv(1024)
            data = data.decode()
            data = json.loads(data)
            data = parse_json_with_eval(data)
        return data

    def get_int(self) -> int:
        data = 0
        if self.is_running:
            data = self.socket.recv(1024)
            data = eval(data)
        return data

    def init_socket(self, port) -> None:
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(None)
        self.socket.connect((self.host, port))
        self.is_running = True

    def stop_socket(self) -> None:
        """
        Used to stop the communication service.
        """
        self.is_running = False
        self.socket.close()


