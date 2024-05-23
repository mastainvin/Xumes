import time

import multiprocess

from xumes import Agent
from xumes.core.modes import TEST_MODE
from xumes.test_runner.feature_strategy import given_registry, when_registry, then_registry, config_registry
from xumes.test_runner.test_manager import TestManager
from xumes.modules.reinforcement_learning.vec_stable_baselines_trainer import VecStableBaselinesTrainer


class VecRLTestManager(TestManager):

    def _run_feature(self, feature, active_processes):
        vec_sb_trainers = VecStableBaselinesTrainer()

        model_path = None
        trainers_info = {}

        for scenario in feature.scenarios:
            self.add_test_runner_data(scenario=scenario, ip="127.0.0.1", port=0)

            registry_queue = multiprocess.Queue()
            registry_queue.put((config_registry, given_registry, when_registry, then_registry))

            test_runner = self.create_test_runner(scenario, self._assertion_queue, registry_queue)

            methods = test_runner.config()
            port = self._comm_service.start_scenario(scenario.feature.name, methods, self._fps_limit, self._render)
            self._scenario_datas[scenario].port = port
            test_runner.run(port)

            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Agent = when_result[next(iter(when_result))]
            behavior.set_mode(self._mode)
            behavior.set_game_service(test_runner)

            if trainers_info == {}:
                trainers_info = behavior.get_trainer_info()

            if not model_path:
                model_path = behavior.get_path()

            vec_sb_trainers.add_trainer(behavior.get_trainer())

        def run(_path, nb_processes, vec_trainers):
            if not _path:
                _path = "./models/" + feature.name

            if self._mode == TEST_MODE:
                vec_trainers.load(_path + "/best_model")
                vec_trainers.play()
                vec_trainers.free()
            else:
                vec_trainers.train(save_path=_path, **trainers_info)
                vec_trainers.free()
                # vec_trainers.save(_path)

            nb_processes.value -= 1

        process = multiprocess.Process(target=run, args=(model_path, active_processes, vec_sb_trainers))
        process.start()
        feature.processes.append(process)
        active_processes.value += 1
