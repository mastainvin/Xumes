import importlib.util
import importlib.util
import os

from xumes.core.registry import create_registry
from xumes.trainer.entity_manager import AutoEntityManager
from xumes.trainer.i_trainer import ITrainer
from xumes.trainer.implementations.gym_impl.stable_baselines_trainer import OBST, StableBaselinesTrainer
from xumes.trainer.implementations.json_impl.json_game_element_state_converter import JsonGameElementStateConverter

import logging
import time

import multiprocess
from typing import List, Dict

from xumes.core.colors import bcolors
from xumes.core.modes import TEST_MODE, TRAIN_MODE, RENDER_MODE
from xumes.test_runner.assertion_bucket import AssertionReport
from xumes.test_runner.feature_strategy import FeatureStrategy, Scenario
from xumes.test_runner.i_communication_service_test_manager import ICommunicationServiceTestManager
from xumes.test_runner.implementations.socket_impl.communication_service_game_socket import \
    CommunicationServiceGameSocket
from xumes.test_runner.test_runner import TestRunner

observation = create_registry()
action = create_registry()
reward = create_registry()
terminated = create_registry()
config = create_registry()

observation_registry = observation.all
action_registry = action.all
reward_registry = reward.all
terminated_registry = terminated.all
config_registry = config.all


class ScenarioData:

    def __init__(self, test_runner: TestRunner = None, process: multiprocess.Process = None, ip: str = None,
                 port: int = None):
        self.test_runner = test_runner
        self.process = process
        self.ip = ip
        self.port = port


class Manager:

    def __init__(self, communication_service: ICommunicationServiceTestManager, feature_strategy: FeatureStrategy,
                 timesteps=None, iterations=None, mode: str = TEST_MODE, model_path: str = None,
                 logging_level=logging.NOTSET, trainers_path=None):

        self._communication_service = communication_service
        self._scenario_datas: Dict[Scenario, ScenarioData] = {}
        self._mode = mode
        self._timesteps = timesteps
        self._iterations = iterations
        self._feature_strategy: FeatureStrategy = feature_strategy
        self._assertion_queue = multiprocess.Queue()
        self._logging_level = logging_level
        self._delta_time = 0

        self._load_trainers(trainers_path)
        self._trainer_processes: Dict[str, multiprocess.Process] = {}
        self._mode = mode
        self._previous_model_path = model_path
        self._logging_level = logging_level

    # noinspection DuplicatedCode
    @staticmethod
    def _load_trainers(path: str = "./"):
        for file in os.listdir(path):
            if file.endswith(".py"):
                module_path = os.path.join(path, file)
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

    def add_game_service_data(self, scenario: Scenario, ip: str, port: int):
        # Add a game service data to the list of game services data
        self._scenario_datas[scenario] = ScenarioData(ip=ip, port=port)

    def create_game_service(self, scenario: Scenario, scenario_data: ScenarioData, assertion_queue: multiprocess.Queue,
                            ) -> TestRunner:
        test_runner = self._feature_strategy.build_test_runner(mode=self._mode, timesteps=self._timesteps,
                                                               iterations=self._iterations, scenario=scenario,
                                                               test_queue=assertion_queue,
                                                               comm_service=CommunicationServiceGameSocket(),
                                                               )
        scenario_data.test_runner = test_runner
        return test_runner

    def _init_logging(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)

    def test_all(self, path) -> None:
        test_time_start = time.time()

        # Retrieve features and scenarios
        self._feature_strategy.retrieve_feature(path)
        features = self._feature_strategy.features

        # For all scenarios, we run the test
        for feature in features:
            # Check if all tests are finished
            active_processes = multiprocess.Value('i', 0)

            for scenario in feature.scenarios:

                self._communication_service.connect_trainer(self, scenario)

                if self._mode == TEST_MODE or self._mode == TRAIN_MODE:  # no render
                    process = multiprocess.Process(target=self.run_test, args=(
                        scenario, active_processes, self._assertion_queue,
                        self._scenario_datas[scenario].registry_queue,))
                else:  # render
                    process = multiprocess.Process(target=self.run_test_render,
                                                   args=(scenario, active_processes,
                                                         self._assertion_queue,
                                                         self._scenario_datas[scenario].registry_queue,
                                                         ))
                process.start()
                active_processes.value += 1
                self._scenario_datas[scenario].process = process

            # Send to the training manager that the training is started
            self._communication_service.start_training(self)

            # Wait for all tests to be finished
            while active_processes.value > 0:
                pass

            # Close all processes and delete all game services
            for scenario, scenario_data in self._scenario_datas.items():
                scenario_data.process.kill()
                self._communication_service.disconnect_trainer(self, scenario)
            self._delete_game_services()
            self._communication_service.reset(self)

        test_time_end = time.time()
        self._delta_time = round(test_time_end - test_time_start, 3)

        if self._mode == TEST_MODE or self._mode == RENDER_MODE:
            self._assert()

        self._communication_service.stop()

    def _assert(self):

        results: List[AssertionReport] = []
        successes = 0
        tests_passed_names = ''
        error_logs = ''

        while not self._assertion_queue.empty():
            assertion_report = self._assertion_queue.get()
            if assertion_report is None:
                break
            results.append(assertion_report)
            if assertion_report.passed:
                successes += 1
                tests_passed_names += '    - ' + assertion_report.test_name + '\n'
            else:
                error_logs += assertion_report.error_logs

        # log results
        nb_test = len(results)
        header = f"{bcolors.BOLD}{bcolors.UNDERLINE}{'':15}TEST REPORT{'':15}{bcolors.ENDC}\n"
        details = f"{successes} tests passed on a total of {nb_test} in {self._delta_time}s.\n"
        details += f"Tests passed:\n{tests_passed_names}\n" if successes > 0 else ""
        details += error_logs

        if successes < nb_test:
            print(f"{bcolors.FAIL}{header}")
            print(f"{bcolors.FAIL}{details}")
        else:
            print(f"{bcolors.OKGREEN}{header}")
            print(f"{bcolors.OKGREEN}{details}")

    def _delete_game_services(self) -> None:
        self._scenario_datas.clear()

    def run_test(self, scenario: Scenario, active_processes, assertion_queue: multiprocess.Queue,
                 registry_queue: multiprocess.Queue) -> None:
        self._init_logging()
        game_service = self.create_game_service(scenario, self._scenario_datas[scenario], assertion_queue,
                                                registry_queue)
        game_service.init_socket()

        with active_processes.get_lock():
            active_processes.value -= 1

        game_service.stop_socket()

    def run_test_render(self, scenario: Scenario, active_processes, assertion_queue: multiprocess.Queue,
                        registry_queue: multiprocess.Queue) -> None:
        self._init_logging()
        game_service = self.create_game_service(scenario, self._scenario_datas[scenario], assertion_queue,
                                                registry_queue)
        game_service.run_render()

        with active_processes.get_lock():
            active_processes.value -= 1

        game_service.stop_socket()

    def run(self):
        if self._mode == TRAIN_MODE:
            self.train()
        elif self._mode == TEST_MODE:
            self.play()

    def _init_logger(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)

    def create_trainer(self, test_runner: TestRunner, feature: str, scenario: str, observation_r, action_r,
                       reward_r, terminated_r,
                       config_r) -> ITrainer:
        # We use the decorators to implement the trainer's methods

        class ConcreteTrainer(StableBaselinesTrainer):
            def convert_obs(self) -> OBST:
                return observation_r[feature](self)

            def convert_reward(self) -> float:
                return reward_r[feature](self)

            def convert_terminated(self) -> bool:
                return terminated_r[feature](self)

            def convert_actions(self, raws_actions) -> List[str]:
                return action_r[feature](self, raws_actions)

        try:
            trainer = ConcreteTrainer(entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
                                      test_runner=test_runner, )

            config_r[feature](trainer)
            trainer.make()
        except Exception as e:
            raise Exception(f"Error while creating trainer: {e}")

        return trainer

    def connect_trainer(self, feature: str, scenario: str) -> None:
        # Create a new process to train or  use an agent
        name = self._trainer_name(feature, scenario)

        test_runner = self._build_game_service()

        registry_queue = multiprocess.Queue()
        registry_queue.put(
            (observation_registry, action_registry, reward_registry, terminated_registry, config_registry))

        if self._mode == TRAIN_MODE:
            self.create_and_train(test_runner, feature, scenario, registry_queue)
        elif self._mode == TEST_MODE:
            self.create_and_play(test_runner, feature, scenario, registry_queue)

    def disconnect_trainer(self, feature: str, scenario: str) -> None:
        # Terminate the process
        name = self._trainer_name(feature, scenario)
        if name in self._trainer_processes:
            self._trainer_processes[name].terminate()
            self._trainer_processes[name].join()
            del self._trainer_processes[name]

    def create_and_train(self, feature: str, scenario: str, queue: multiprocess.Queue):
        self._init_logger()

        # Create a new trainer and train it
        observation_r, action_r, reward_r, terminated_r, config_r = queue.get()
        trainer = self.create_trainer(feature, scenario, observation_r, action_r, reward_r, terminated_r,
                                      config_r)
        trainer.train(self._model_path(feature, scenario),
                      logs_path=self._model_path(feature, scenario) + "/../_logs" if self._do_logs else None,
                      logs_name=scenario, previous_model_path=self._previous_model_path)

    def create_and_play(self, feature: str, scenario: str, queue: multiprocess.Queue):
        self._init_logger()
        # Create a new trainer and play it
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)
        observation_r, action_r, reward_r, terminated_r, config_r = queue.get()
        trainer = self.create_trainer(feature, scenario, observation_r, action_r, reward_r, terminated_r,
                                      config_r)
        trainer.load(self._model_path(feature, scenario) + "/best_model")
        trainer.play(timesteps=None)

    def _trainer_name(self, feature, scenario) -> str:
        return feature + "_" + scenario

    def _model_path(self, feature, scenario) -> str:
        return "./models/" + feature + "/" + scenario
