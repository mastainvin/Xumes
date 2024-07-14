import logging
import traceback

import multiprocess

from xumes import Agent, Imitator, Imitable
from xumes.core.modes import TRAIN_MODE
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.test_manager import TestManager


class VecImitatorTestManager(TestManager):
    """
    This class extends the TestManager class and is responsible for managing the testing of the VecImitator.
    """

    def _run_scenarios(self, feature, scenario_datas, active_processes):
        """
        This method runs the scenarios for the given feature.

        :param feature: The feature to be tested.
        :param scenario_datas: The data for the scenarios to be run.
        :param active_processes: The number of active processes.
        """

        # Initialize the imitator, model path, trainers info and behaviors list
        imitator: Imitator = None
        model_path = None
        trainers_info = {}
        _behaviors = []

        # Iterate over the scenarios
        for scenario in scenario_datas:

            # Get the test runner for the current scenario
            test_runner = scenario_datas[scenario].test_runner

            # Get the behavior from when result
            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Behavior = when_result[next(iter(when_result))]

            # Check if the behavior is an instance of Agent or Imitable
            if not isinstance(behavior, (Agent, Imitable)):
                raise Exception("Only Agent or Imitable behavior is allowed")

            # Get the agent from the behavior
            agent: Agent = behavior

            # Check if the agent is not None
            if not agent:
                raise Exception("Only Agent behavior is allowed")

            # Get the imitable from the behavior
            imitable: Imitable = behavior
            if not imitable:
                raise Exception("Only Imitator behavior is allowed")

            # If the imitator is not initialized, initialize it with the imitable's imitator
            if not imitator:
                imitator = imitable.imitator()

            # Set the mode and test runner of the behavior
            behavior.set_mode(self._mode)
            behavior.set_test_runner(test_runner)

            # If the trainers info is not set, get it from the behavior
            if trainers_info == {}:
                trainers_info = behavior.get_trainer_info()

            # If the model path is not set, get it from the behavior
            if not model_path:
                model_path = behavior.get_path()

            # Add the trainer of the behavior to the imitator and set the agent of the imitator
            imitator.add_trainer(behavior.get_trainer())
            imitator.set_agent(agent)

            # Add the behavior to the behaviors list
            _behaviors.append(behavior)

        def run(_path, nb_processes, vec_imitator, behaviors, do_log=None):
            """
            This method runs the vec_imitator.

            :param _path: The path of the model.
            :param nb_processes: The number of processes.
            :param vec_imitator: The vec_imitator to be run.
            :param behaviors: The behaviors to be run.
            :param do_log: Whether to log or not.
            """

            try:
                # If the mode is TRAIN_MODE, execute the vec_imitator
                if self._mode == TRAIN_MODE:
                    vec_imitator.execute(feature, None)
                else:
                    raise Exception("Can only run in TRAIN_MODE")
            except SystemExit or KeyboardInterrupt:
                logging.warning("Training interrupted by user.")
            except Exception as e:
                logging.error(f"Error occurs while {self._mode}: {e}")
                logging.error(traceback.format_exc())
            finally:
                # Finish the test runner of each behavior and free the vec_imitator
                for agent in behaviors:
                    agent.test_runner.finished()
                vec_imitator.free()

                # Decrease the number of processes
                nb_processes.value -= 1

                exit(0)

        # Start a new process to run the vec_imitator
        process = multiprocess.Process(target=run,
                                       args=(model_path, active_processes, imitator, _behaviors, self.do_logs))
        process.start()
        feature.processes.append(process)
        active_processes.value += 1
