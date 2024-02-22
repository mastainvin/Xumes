import json
from socket import socket, AF_INET, SOCK_STREAM
from typing import Dict, Any

from xumes.core.utils import parse_json_with_eval
from xumes.test_runner.i_communication_service_game import ICommunicationServiceGame


class CommunicationServiceGameSocket(ICommunicationServiceGame):

    def __init__(self, host: str):
        self.host = host
        self.socket = None
        self.conn = None
        self.addr = None
        self.is_running = False

    def get_state(self) -> Dict[str, Any]:
        if self.is_running:
            data = self.conn.recv(1024)
            data = data.decode()
            data = json.loads(data)
            data = parse_json_with_eval(data)
        return data

    def push_action(self, action) -> None:
        if self.is_running:
            r = {
                "inputs": action,
            }
            self.conn.sendall(json.dumps(r).encode())

    def push_event(self, event) -> None:
        if self.is_running:
            r = {
                "event": event,
            }
            self.conn.sendall(json.dumps(r).encode())

    def init_socket(self, port) -> None:
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.host, port))

    def stop_socket(self) -> None:
        """
        Used to stop the communication service.
        """
        self.is_running = False
        self.conn.close()
        self.socket.close()
