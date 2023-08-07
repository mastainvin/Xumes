import logging
import urllib
from time import sleep

import requests

from xumes.game_module.i_communication_service_test_manager import ICommunicationServiceTestManager


class CommunicationServiceTestManagerRestApi(ICommunicationServiceTestManager):

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def connect_trainer(self, test_manager, scenario) -> None:
        while True:
            try:
                # noinspection HttpUrlsUsage
                urllib.request.urlopen(f'http://{self.ip}:{self.port}/ping')
                break
            except urllib.error.URLError:
                logging.info(f"Waiting for connection with {self.ip}:{self.port}...")
                sleep(1)

        port = test_manager.get_free_port(scenario)

        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/connect',
                      json={
                          'feature': scenario.feature.name,
                          'scenario': scenario.name,
                          'port': port
                      })
        test_manager.add_game_service_data(scenario=scenario, ip=self.ip, port=port)

    def disconnect_trainer(self, test_manager, scenario) -> None:
        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/disconnect',
                      json={
                          'feature': scenario.feature.name,
                          'scenario': scenario.name
                      })

    def start_training(self, test_manager) -> None:
        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/start')

    def reset(self, test_manager) -> None:
        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/reset')

    def run(self, test_manager) -> None:
        pass

    def stop(self) -> None:
        # noinspection HttpUrlsUsage
        requests.post(f'http://{self.ip}:{self.port}/shutdown')

