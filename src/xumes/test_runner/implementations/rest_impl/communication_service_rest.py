import json
import logging
from typing import Dict, List

import requests
import time


class CommunicationServiceRest:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()

    def start_scenario(self, name: str, methods: List[Dict]) -> int:
        port = 0
        # call the REST API to get the port
        http_response = self.session.post(f"http://{self.host}:{self.port}/start_scenario/", json=methods)
        if http_response.status_code == 200:
            port = http_response.json()
            logging.log(logging.INFO, f"Scenario {name} started on port {port}.")
        return port
