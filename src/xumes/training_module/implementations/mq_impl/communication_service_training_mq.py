import json
import logging
from typing import List

import zmq
from zmq import ZMQError

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.training_module.i_communication_service_training import ICommunicationServiceTraining


class CommunicationServiceTrainingMq(ICommunicationServiceTraining):
    def __init__(self, port=5555):
        logging.info("Training server creation...")
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(port))

    def push(self, data):
        try:
            self.socket.send(json.dumps(data).encode("utf-8"))
        except ZMQError:
            pass

    def push_event(self, event: str) -> None:
        self.push({
            'event': event,
            'inputs': []
        })

    def push_actions(self, actions: List[str]) -> None:
        self.push({
            'inputs': actions,
            'event': ''
        })

    def get_states(self) -> List:
        response = self.socket.recv().decode("utf-8")
        if response == "finished":
            raise RunningEndsError
        else:
            # Use .items to convert dict to list of tuple (KEY, VALUE).
            states = json.loads(eval(response)).items()
            return states

    def close(self) -> None:
        self.socket.close()
