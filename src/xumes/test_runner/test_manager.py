import logging
import time
from abc import abstractmethod

import multiprocess
from typing import List, Dict

from xumes.core.colors import bcolors
from xumes.core.modes import TEST_MODE, RENDER_MODE
from xumes.test_runner.assertion_bucket import AssertionReport
from xumes.test_runner.feature_strategy import FeatureStrategy, Scenario
from xumes.test_runner.implementations.socket_impl.communication_service_socket import \
    CommunicationServiceSocket

from xumes.test_runner.test_runner import TestRunner


class ScenarioData:

    def __init__(self, test_runner: TestRunner = None, process: multiprocess.Process = None, ip: str = None,
                 port: int = None):
        self.test_runner = test_runner
        self.process = process
        self.ip = ip
        self.port = port


class TestManager:
    """
    A class that manages the execution of tests in a game environment.

    The TestManager class is responsible for loading and running tests in a game environment. It provides functionality
    for creating game services, running tests, and managing communication with the training manager.

    Args:
        communication_service (ICommunicationServiceTestManager): An implementation of the
            ICommunicationServiceTestManager interface for communication with the training manager.
        mode (str, optional): The mode of the test execution. Can be 'test', 'render', or 'train'.
            Defaults to 'test'.
        timesteps (int, optional): The maximum number of steps to run in a test. Defaults to None.
        iterations (int, optional): The maximum number of iterations to run a test. Defaults to None.

    Methods:
        get_port(feature: str, scenario: str) -> int:
            Retrieves the port number for a given feature and scenario.
        add_test_runner_data(steps: str, ip: str, port: int) -> None:
            Adds game service data to the list of game services data.
        create_test_runner(steps: str, ip: str, port: int) -> GameService:
            Creates a game service instance with the specified steps, IP, and port.
        _build_test_runner(test_runner, ip, port) -> GameService:
            Abstract method to build a game service instance. Must be implemented by subclasses.
        test_all() -> None:
            Runs all the tests in the game environment.
        delete_test_runners() -> None:
            Deletes all game service instances.
        run_test(steps: str, active_processes) -> None:
            Runs a test with the given steps.
        run_test_render(steps: str, active_processes) -> None:
            Runs a test in render mode with the given steps.
    """

    def __init__(self, comm_service,
                 feature_strategy: FeatureStrategy,
                 mode: str = TEST_MODE, timesteps=None, iterations=None, do_logs: bool = False,
                 logging_level=logging.NOTSET):
        self._comm_service = comm_service
        self._scenario_datas: Dict[Scenario, ScenarioData] = {}
        self._mode = mode
        self._timesteps = timesteps
        self._iterations = iterations
        self._feature_strategy: FeatureStrategy = feature_strategy
        self._assertion_queue = multiprocess.Queue()
        self._do_logs = do_logs
        self._logging_level = logging_level
        self._delta_time = 0

    def get_free_port(self, scenario) -> int:
        # Get the port for a given feature and scenario
        if scenario not in self._scenario_datas:
            return 5001 + len(self._scenario_datas)
        else:
            return self._scenario_datas[scenario].port

    def add_test_runner_data(self, scenario: Scenario, ip: str, port: int):
        # Add a game service data to the list of game services data
        self._scenario_datas[scenario] = ScenarioData(ip=ip, port=port)

    def create_test_runner(self, scenario: Scenario, assertion_queue: multiprocess.Queue,
                           registry_queue: multiprocess.Queue
                           ) -> TestRunner:
        test_runner = self._feature_strategy.build_test_runner(mode=self._mode,
                                                               timesteps=self._timesteps,
                                                               iterations=self._iterations,
                                                               scenario=scenario,
                                                               test_queue=assertion_queue,
                                                               registry_queue=registry_queue,
                                                               comm_service=CommunicationServiceSocket(
                                                                   host="127.0.0.1"))
        # scenario_data.test_runner = test_runner

        return test_runner

    def _init_logging(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)

    def test_all(self, path) -> None:
        test_time_start = time.time()

        # Retrieve features and scenarios
        self._feature_strategy.retrieve_feature(path)
        features = self._feature_strategy.features

        # Check if all tests are finished
        active_processes = multiprocess.Value('i', 0)

        # For all scenarios in each feature, we run the test
        for feature in features:
            self._run_feature(feature, active_processes)

        # Wait for all tests to be finished
        while active_processes.value > 0:
            pass

        # Close all processes
        for feature in features:
            for process in feature.processes:
                process.kill()

        # self.trainer_manager.disconnect_trainer(scenario.feature.name, scenario.name) TODO : see if we need to disconnect

        test_time_end = time.time()
        self._delta_time = round(test_time_end - test_time_start, 3)

        if self._mode == TEST_MODE or self._mode == RENDER_MODE:
            self._assert()
        else:
            print(f"{bcolors.OKGREEN}Training finished in {self._delta_time}s.{bcolors.ENDC}")

    def _assert(self):
        # Make assertions

        results: List[AssertionReport] = []
        successes = 0
        tests_passed_names = ''
        error_logs = ''

        # Gather all assertion reports
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

    @abstractmethod
    def _run_feature(self, feature, active_processes):
        raise NotImplementedError
