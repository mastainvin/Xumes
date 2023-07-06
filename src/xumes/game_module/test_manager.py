import importlib.util
import multiprocessing
import os
from abc import abstractmethod
from typing import List, Dict

from xumes.core.colors import bcolors
from xumes.core.modes import TEST_MODE, TRAIN_MODE
from xumes.game_module import GameService, PygameEventFactory, CommunicationServiceGameMq
from xumes.game_module.assertion_bucket import AssertionReport
from xumes.game_module.feature_strategy import FeatureStrategy, Scenario
from xumes.game_module.i_communication_service_test_manager import ICommunicationServiceTestManager


class ScenarioData:

    def __init__(self, game_service: GameService = None, process: multiprocessing.Process = None, ip: str = None, port: int = None):
        self.game_service = game_service
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
        add_game_service_data(steps: str, ip: str, port: int) -> None:
            Adds game service data to the list of game services data.
        create_game_service(steps: str, ip: str, port: int) -> GameService:
            Creates a game service instance with the specified steps, IP, and port.
        _build_game_service(test_runner, ip, port) -> GameService:
            Abstract method to build a game service instance. Must be implemented by subclasses.
        test_all() -> None:
            Runs all the tests in the game environment.
        delete_game_services() -> None:
            Deletes all game service instances.
        run_test(steps: str, active_processes) -> None:
            Runs a test with the given steps.
        run_test_render(steps: str, active_processes) -> None:
            Runs a test in render mode with the given steps.
    """

    def __init__(self, communication_service: ICommunicationServiceTestManager, feature_strategy: FeatureStrategy,
                 mode: str = TEST_MODE, timesteps=None, iterations=None):

        self._load_tests()
        self._communication_service = communication_service
        self._scenario_datas: Dict[Scenario, ScenarioData] = {}
        self._mode = mode
        self._timesteps = timesteps
        self._iterations = iterations
        self._feature_strategy: FeatureStrategy = feature_strategy
        self._assertion_queue = multiprocessing.Queue()

    @staticmethod
    def _load_tests():
        for file in os.listdir("./tests"):
            if file.endswith(".py"):
                module_name = file[:-3]
                module_path = os.path.join("./tests", file)
                module = compile(open(module_path).read(), module_path, 'exec')
                exec(module, globals(), locals())
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

    def get_free_port(self, scenario) -> int:
        # Get the port for a given feature and scenario
        if scenario not in self._scenario_datas:
            return 5001 + len(self._scenario_datas)
        else:
            return self._scenario_datas[scenario].port

    def add_game_service_data(self, scenario: Scenario, ip: str, port: int):
        # Add a game service data to the list of game services data
        self._scenario_datas[scenario] = ScenarioData(ip=ip, port=port)

    def create_game_service(self, scenario: Scenario, scenario_data: ScenarioData) -> GameService:
        game_service = self._build_game_service(
            self._feature_strategy.build_test_runner(mode=self._mode, timesteps=self._timesteps,
                                                     iterations=self._iterations, scenario=scenario,
                                                     test_queue=self._assertion_queue), scenario_data.ip, scenario_data.port, )
        scenario_data.game_service = game_service
        return game_service

    @abstractmethod
    def _build_game_service(self, test_runner, ip, port) -> GameService:
        raise NotImplementedError

    def test_all(self) -> None:
        # Retrieve features and scenarios
        self._feature_strategy.retrieve_feature()
        features = self._feature_strategy.features

        # For all scenarios, we run the test
        for feature in features:
            # Check if all tests are finished
            active_processes = multiprocessing.Value('i', 0)

            for scenario in feature.scenarios:

                self._communication_service.connect_trainer(self, scenario)

                if self._mode == TEST_MODE or self._mode == TRAIN_MODE:  # no render
                    process = multiprocessing.Process(target=self.run_test, args=(scenario, active_processes,))
                else:  # render
                    process = multiprocessing.Process(target=self.run_test_render,
                                                      args=(scenario, active_processes,))
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

        if self._mode == TEST_MODE:
            self._assert()

    def _assert(self):

        results: List[AssertionReport] = []
        successes = 0
        error_logs = ''

        while not self._assertion_queue.empty():
            assertion_report = self._assertion_queue.get()
            results.append(assertion_report)
            if assertion_report.passed:
                successes += 1
            else:
                error_logs += assertion_report.error_logs

        # log results
        nb_test = len(results)
        header = f"{bcolors.BOLD}{bcolors.UNDERLINE}{'':15}TEST REPORT{'':15}{bcolors.ENDC}\n"
        details = f"{successes} tests passed on a total of {nb_test}.\n" + error_logs
        if successes < nb_test:
            print(f"{bcolors.FAIL}{header}")
            print(f"{bcolors.FAIL}{details}")
        else:
            print(f"{bcolors.OKGREEN}{header}")
            print(f"{bcolors.OKGREEN}{details}")

    def _delete_game_services(self) -> None:
        self._scenario_datas.clear()

    def run_test(self, scenario: Scenario, active_processes) -> None:
        game_service = self.create_game_service(scenario, self._scenario_datas[scenario])
        game_service.run()

        with active_processes.get_lock():
            active_processes.value -= 1

        game_service.stop()

    def run_test_render(self, scenario: Scenario, active_processes) -> None:
        game_service = self.create_game_service(scenario, self._scenario_datas[scenario])
        game_service.run_render()

        with active_processes.get_lock():
            active_processes.value -= 1

        game_service.stop()


class PygameTestManager(TestManager):

    def _build_game_service(self, test_runner, ip, port) -> GameService:
        game_service = GameService(test_runner=test_runner,
                                   event_factory=PygameEventFactory(),
                                   communication_service=CommunicationServiceGameMq(ip=ip, port=port))
        return game_service
