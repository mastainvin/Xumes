import logging
import traceback
from abc import abstractmethod
from typing import List, Dict, Any

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.input import Input


class Script(Behavior):

    def execute(self, feature, scenario):
        try:
            self.test_runner.reset()
            game_state = self.test_runner.push_action_and_get_state([])
            while True:
                game_state = self.test_runner.push_action_and_get_state(self.step())

                if self.terminated():
                    try:
                        self.test_runner.episode_finished()
                        self.test_runner.reset()
                    except RunningEndsError:
                        break
        except Exception as e:
            logging.error("Error in scripted testing: ", e)
            logging.error(traceback.format_exc())
        finally:
            self.test_runner.finished()
            exit(0)

    @abstractmethod
    def step(self) -> List[Input]:
        raise NotImplementedError

