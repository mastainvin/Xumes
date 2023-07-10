from typing import List

import requests

from xumes.training_module.i_communication_service_training import ICommunicationServiceTraining


class CommunicationServiceTrainingRestApi(ICommunicationServiceTraining):

    def __init__(self, url: str):
        self.url = url

    def push_event(self, event: str) -> None:
        requests.post(self.url,
                      json={
                          'event': event,
                          'inputs': []
                      })

    def push_actions(self, actions: List[str]) -> None:
        requests.post(self.url,
                      json={
                          'inputs': actions,
                          'event': ''
                      })

    def get_states(self) -> List:
        # Use .items to convert dict to list of tuple (KEY, VALUE).
        return requests.get(self.url).json().items()
