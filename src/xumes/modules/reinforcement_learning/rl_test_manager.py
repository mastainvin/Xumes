import multiprocess

from xumes.test_runner.feature_strategy import given_registry, when_registry, then_registry, config_registry
from xumes.test_runner.test_manager import TestManager
from xumes.behavior import Behavior


class RLTestManager(TestManager):

    def _run_feature(self, feature, active_processes):

        for scenario in feature.scenarios:

            self.add_test_runner_data(scenario=scenario, ip="127.0.0.1", port=0)

            registry_queue = multiprocess.Queue()
            registry_queue.put((config_registry, given_registry, when_registry, then_registry))

            test_runner = self.create_test_runner(scenario, self._assertion_queue, registry_queue)

            methods = test_runner.config()
            port = self._comm_service.start_scenario(scenario.feature.name, methods)
            self._scenario_datas[scenario].port = port
            test_runner.run(port)

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
