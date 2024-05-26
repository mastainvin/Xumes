from xumes.behavior import Behavior
from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.test_runner.test_manager import TestManager


def play(behavior):
    behavior.game_service().reset()
    while True:
        behavior.game_service().push_action_and_get_state([])

        if behavior.terminated():
            try:
                behavior.game_service().episode_finished()
                behavior.game_service().reset()
            except RunningEndsError:
                break


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
            behavior.set_game_service(test_runner)

            play(behavior)
