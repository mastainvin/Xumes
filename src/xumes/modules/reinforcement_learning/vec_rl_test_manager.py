import logging
import traceback

import multiprocess

from xumes import Agent
from xumes.core.modes import TEST_MODE
from xumes.test_automation.test_manager import TestManager
from xumes.modules.reinforcement_learning.vec_stable_baselines_trainer import VecStableBaselinesTrainer


class VecRLTestManager(TestManager):

    def _run_scenarios(self, feature, scenario_datas, active_processes):

        vec_sb_trainers = VecStableBaselinesTrainer()

        model_path = None
        trainers_info = {}

        behaviors: Agent = []

        for scenario in scenario_datas:

            test_runner = scenario_datas[scenario].test_runner
            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Agent = when_result[next(iter(when_result))]
            behavior.set_mode(self._mode)
            behavior.set_test_runner(test_runner)

            if trainers_info == {}:
                trainers_info = behavior.get_trainer_info()

            if not model_path:
                model_path = behavior.get_path()

            vec_sb_trainers.add_trainer(behavior.get_trainer())

            # Add behavior to the list in order to free the resources after the training if error occurs
            behaviors.append(behavior)

        def run(_path, nb_processes, vec_trainers, behaviors, do_log=None):
            if not _path:
                _path = "./models/" + feature.name

            logging_path = None
            if do_log:
                logging_path = _path + "/logs"

            try:
                if self._mode == TEST_MODE:
                    vec_trainers.load(_path + "/best_model")
                    vec_trainers.play()
                else:
                    vec_trainers.train(save_path=_path, logs_path=logging_path, logs_name=feature.name, **trainers_info)
            except SystemExit or KeyboardInterrupt:
                logging.warning("Training interrupted by user.")
            except Exception as e:
                logging.error(f"Error occurs while {self._mode}: {e}")
                logging.error(traceback.format_exc())
            finally:
                vec_trainers.free()

                for agent in behaviors:
                    agent.test_runner.finished()

                nb_processes.value -= 1

                exit(0)

        process = multiprocess.Process(target=run, args=(model_path, active_processes, vec_sb_trainers, behaviors, self.do_logs))
        process.start()
        feature.processes.append(process)
        active_processes.value += 1
