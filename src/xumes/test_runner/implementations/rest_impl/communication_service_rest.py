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

    def start_scenario(self, name: str, methods: List[Dict], fps_limit: int, render: bool) -> int:
        port = 0
        body = {
            "methods": methods,
            "fps_limit": fps_limit,
            "render": render
        }
        http_response = self.session.post(f"http://{self.host}:{self.port}/start_scenario/", json=body)
        if http_response.status_code == 200:
            port = http_response.json()
            logging.log(logging.INFO, f"Scenario {name} started on port {port}.")
        return port

    def start_scenarios(self, scenarios_methods, scenarios, fps_limit: int, render: bool) -> Dict[str, int]:
        ports = {}
        http_response = self.session.post(f"http://{self.host}:{self.port}/start_scenarios/", json=scenarios_methods)
        if http_response.status_code == 200:
            ports_response = http_response.json()
            for scenario_method in scenarios_methods:
                scenario_name = scenario_method["name"]
                port = ports_response[scenario_name]
                scenario = next(scenario for scenario in scenarios if scenario.name == scenario_name) # TODO change this to a dict
                ports[scenario] = port
                logging.log(logging.INFO, f"Scenario {scenario_name} started on port {port}.")

        return ports
