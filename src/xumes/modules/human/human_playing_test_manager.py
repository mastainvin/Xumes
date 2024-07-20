import numpy as np

from xumes import Script
from xumes.core.parameters_registry import ParametersRegistry
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.test_manager import TestManager


class HumanTestingScript(Script):

    def __init__(self, behavior: Behavior):
        super().__init__()
        self._behavior = behavior

        self._episode_length = (ParametersRegistry()).get("episode_length")
        if self._episode_length is None:
            self._episode_length = None
        else:
            self._episode_length = int(self._episode_length)
        self._step_count = 0

    def step(self):
        self._step_count += 1
        return []

    def terminated(self) -> bool:
        if self._episode_length is not None and self._step_count >= self._episode_length:
            self._step_count = 0
            return True
        return self._behavior.terminated()


class HumanPlayingTestManager(TestManager):
    """
    Test manager for human playing doing the manual testing.
    """

    def _run_scenarios(self, feature, scenario_datas, active_processes):
        reversed_scenario_datas = list(scenario_datas.keys())
        for scenario in reversed_scenario_datas:
            feature = scenario.feature
            test_runner = scenario_datas[scenario].test_runner

            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Behavior = when_result[next(iter(when_result))]
            behavior.set_mode(self._mode)
            behavior.set_test_runner(test_runner)

            human_testing_script = HumanTestingScript(behavior)
            human_testing_script.set_mode(self._mode)
            human_testing_script.set_test_runner(test_runner)
            human_testing_script.set_do_logging(self.do_logs)
            human_testing_script.execute(scenario.feature, scenario)
