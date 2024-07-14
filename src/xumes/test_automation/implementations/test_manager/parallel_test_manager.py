import traceback

import multiprocess
from xumes.test_automation.behavior import Behavior

from xumes.test_automation.test_manager import TestManager

import logging


class ParallelTestManager(TestManager):

    def _run_scenarios(self, feature, scenario_datas, active_processes):
        for scenario in scenario_datas:
            feature = scenario.feature
            test_runner = scenario_datas[scenario].test_runner

            def run(nb_processes, t_runner, do_logging):
                try:
                    when_result = t_runner.when()
                    if len(when_result) > 1:
                        raise Exception("Only one when step is allowed")

                    behavior: Behavior = when_result[next(iter(when_result))]
                    behavior.set_mode(self._mode)
                    behavior.set_test_runner(t_runner)
                    behavior.set_do_logging(do_logging)
                    behavior.execute(scenario.feature, scenario)
                except Exception as e:
                    logging.error(f"Error occurs while {self._mode}: ", e)
                    traceback.print_exc()
                finally:
                    nb_processes.value -= 1
                    exit(0)

            process = multiprocess.Process(target=run, args=(active_processes, test_runner, self.do_logs))
            process.start()
            feature.processes.append(process)
            active_processes.value += 1
