import multiprocess

from xumes.core.modes import TEST_MODE
from xumes.test_runner.feature_strategy import given_registry, when_registry, then_registry
from xumes.test_runner.test_manager import TestManager
from xumes.trainer import Behavior
from xumes.trainer.implementations.gym_impl.vec_stable_baselines_trainer import VecStableBaselinesTrainer


class VecRLTestManager(TestManager):

    def _run_feature(self, feature, active_processes):
        vec_sb_trainers = VecStableBaselinesTrainer()

        model_path = None
        for scenario in feature.scenarios:

            self.add_test_runner_data(scenario=scenario, ip="127.0.0.1", port=0)

            registry_queue = multiprocess.Queue()
            registry_queue.put((given_registry, when_registry, then_registry))

            test_runner = self.create_test_runner(scenario, self._assertion_queue, registry_queue)

            port = self._comm_service.start_scenario(scenario.feature.name)
            self._scenario_datas[scenario].port = port
            test_runner.run(port)

            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Behavior = when_result[next(iter(when_result))]
            behavior.set_mode(self._mode)
            behavior.set_game_service(test_runner)

            if not model_path:
                model_path = behavior.get_path()

            vec_sb_trainers.add_trainer(behavior.get_trainer())

        def run(_path, nb_processes, vec_trainers):
            if not _path:
                _path = "./models/" + feature.name
            else:
                _path = _path + "/" + feature.name

            if self._mode == TEST_MODE:
                vec_trainers.load(_path)
                vec_trainers.test()
            else:
                vec_trainers.train(save_path=_path)
                vec_trainers.save(_path)

            nb_processes.value -= 1

        process = multiprocess.Process(target=run, args=(model_path, active_processes, vec_sb_trainers))
        process.start()
        feature.processes.append(process)
        active_processes.value += 1