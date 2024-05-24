import time

import multiprocess

from xumes import Agent
from xumes.core.modes import TEST_MODE
from xumes.test_runner.test_manager import TestManager
from xumes.modules.reinforcement_learning.vec_stable_baselines_trainer import VecStableBaselinesTrainer


class VecRLTestManager(TestManager):

    def _run_scenarios(self, feature, scenario_datas, active_processes):

        vec_sb_trainers = VecStableBaselinesTrainer()

        model_path = None
        trainers_info = {}

        for scenario in scenario_datas:

            test_runner = scenario_datas[scenario].test_runner
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
