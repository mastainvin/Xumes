import logging
import traceback
from abc import abstractmethod
from typing import List

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.given_script import GivenScript
from xumes.test_automation.input import Input

from xumes.test_automation.given_script import TestStep


class Script(Behavior):

    def __init__(self):
        super().__init__()
        self.given_script = None

    def execute(self, feature, scenario):
        try:
            self.reset()
            game_state = self.test_runner.push_action_and_get_state([])
            while True:
                actions = self.step()
                if isinstance(actions, TestStep):
                    if self.given_script is None:
                        self.given_script = GivenScript(self.test_runner)
                    self.given_script.clean()
                    self.given_script.add_step(actions)
                    self.given_script.execute()
                else:
                    game_state = self.test_runner.push_action_and_get_state(self.step())

                if self.terminated():
                    try:
                        self.test_runner.episode_finished()
                        self.reset()
                    except RunningEndsError:
                        break
        except Exception as e:
            logging.error("Error in scripted testing: ", e)
            logging.error(traceback.format_exc())
        finally:
            self.test_runner.finished()

    @abstractmethod
    def step(self) -> List[Input] | TestStep:
        """
        Method executed at each game frame.

        :return: A list of `Input` objects or an instance of `TestStep`.
        """
        raise NotImplementedError

    def reset(self):
        self.test_runner.reset()
