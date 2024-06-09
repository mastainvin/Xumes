from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.test_manager import TestManager


def play(behavior):
    try:
        behavior.test_runner().reset()
        while True:
            behavior.test_runner().push_action_and_get_state([])

            if behavior.terminated():
                try:
                    behavior.test_runner().episode_finished()
                    behavior.test_runner().reset()
                except RunningEndsError:
                    break
    except Exception as e:
        print("Error in manual playing: ", e)
    finally:
        behavior.test_runner().finished()
        exit(0)


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

            play(behavior)
