import unittest

import gymnasium as gym
import numpy as np

from xumes.test_automation.i_communication_service import ICommunicationService


class GameInstanceMock:
    def __init__(self):
        self.env = gym.make("CartPole-v1")
        self._observation = None

    def get_game_state(self):
        return self._observation

    def push_actions(self, actions):
        self._observation, _, _, _, _ = self.env.step(actions)

    def reset(self):
        self._observation = self.env.reset(seed=42)

    def close(self):
        self.env.close()

    def handle_notification(self, notification):
        if notification['event'] == "action":
            self.push_actions(notification["inputs"])
            return self.get_game_state()
        elif notification['event'] == "reset":
            self.reset()
            return 1
        elif notification['event'] == "stop":
            self.close()
            return 1


class SocketMock(ICommunicationService):

    def __init__(self):
        self._game_instance = GameInstanceMock()
        self._return_value = None

    def push_dict(self, dictionary):
        self._return_value = self._game_instance.handle_notification(dictionary)

    def get_dict(self):
        return self._return_value

    def get_int(self):
        return self._return_value

    def init_socket(self, port):
        pass

    def stop_socket(self):
        pass


class TestSocketMock(unittest.TestCase):

    def setUp(self):
        self._socket = SocketMock()
        self._socket.init_socket(1234)

    def test_push_reset(self):
        self._socket.push_dict({"event": "reset"})
        assert self._socket.get_int() == 1

    def test_push_action(self):
        self._socket.push_dict({"event": "reset"})
        self._socket.push_dict({"event": "action", "inputs": 0})
        assert np.allclose(self._socket.get_dict(), [0.02727336, -0.20172954, 0.03625453, 0.32351476], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "action", "inputs": 1})
        assert np.allclose(self._socket.get_dict(), [0.02323877, -0.00714208, 0.04272482, 0.04248186], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "action", "inputs": 0})
        assert np.allclose(self._socket.get_dict(), [0.02309593, -0.20284982, 0.04357446, 0.34833285], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "action", "inputs": 1})
        assert np.allclose(self._socket.get_dict(), [0.01903893, -0.00837385, 0.05054112, 0.06970263], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "reset"})
        self._socket.push_dict({"event": "action", "inputs": 0})
        assert np.allclose(self._socket.get_dict(), [0.02727336, -0.20172954, 0.03625453, 0.32351476], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "action", "inputs": 1})
        assert np.allclose(self._socket.get_dict(), [0.02323877, -0.00714208, 0.04272482, 0.04248186], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "action", "inputs": 0})
        assert np.allclose(self._socket.get_dict(), [0.02309593, -0.20284982, 0.04357446, 0.34833285], rtol=1e-05, atol=1e-08)
        self._socket.push_dict({"event": "action", "inputs": 1})
        assert np.allclose(self._socket.get_dict(), [0.01903893, -0.00837385, 0.05054112, 0.06970263], rtol=1e-05, atol=1e-08)

    def test_push_stop(self):
        self._socket.push_dict({"event": "stop"})
        assert self._socket.get_int() == 1

    def tearDown(self):
        self._socket.stop_socket()


if __name__ == '__main__':
    unittest.main()

