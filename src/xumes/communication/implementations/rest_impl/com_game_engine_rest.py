import logging
from typing import Dict, List

import requests
from xumes.communication.i_com_game_engine import IComGameEngine


class ComGameEngineRest(IComGameEngine):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.session = requests.Session()
        self.ports = []

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
        ports_pids = {}
        http_response = requests.post(f"http://{self.host}:{self.port}/start_scenarios/", json=scenarios_methods)
        if http_response.status_code == 200:
            ports_response = http_response.json()
            for scenario_method in scenarios_methods:
                scenario_name = scenario_method["name"]
                port_pid = ports_response[scenario_name]
                scenario = next(scenario for scenario in scenarios if scenario.name == scenario_name) # TODO change this to a dict
                ports_pids[scenario] = port_pid
                logging.log(logging.INFO, f"Scenario {scenario_name} started on port {port_pid[0]} with pid {port_pid[1]}.")

        return ports_pids

    def stop_scenario(self, port: int) -> None:
        http_response = self.session.post(f"http://{self.host}:{self.port}/stop_scenario/", json=port)
        if http_response.status_code == 200:
            logging.log(logging.INFO, f"Scenario on port {port} stopped.")

    def stop_scenarios(self, pids: List[int]) -> None:
        http_response = requests.post(f"http://{self.host}:{self.port}/stop_scenarios/", json=pids)
        if http_response.status_code == 200:
            logging.log(logging.INFO, "Scenarios stopped.")
