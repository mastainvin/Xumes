import multiprocess

from xumes.test_runner.feature_strategy import given_registry, when_registry, then_registry, config_registry
from xumes.test_runner.test_manager import TestManager
from xumes.behavior import Behavior


class RLTestManager(TestManager):

    def _run_scenarios(self, feature, scenario_datas, active_processes):
        for scenario in scenario_datas:
            feature = scenario.feature
            test_runner = scenario_datas[scenario].test_runner

            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Behavior = when_result[next(iter(when_result))]
            behavior.set_mode(self._mode)
            behavior.set_game_service(test_runner)

            def run(nb_processes, trainer):
                behavior.execute(scenario.feature, scenario)
                nb_processes.value -= 1

            process = multiprocess.Process(target=run, args=(active_processes, behavior.get_trainer()))
            process.start()
            feature.processes.append(process)
            active_processes.value += 1



