from xumes import Script
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.test_manager import TestManager


class HumanTestingScript(Script):

    def __init__(self, behavior: Behavior):
        super().__init__()
        self._behavior = behavior

    def step(self):
        return []

    def terminated(self) -> bool:
        return self._behavior.terminated()


class HumanPlayingTestManager(TestManager):

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
