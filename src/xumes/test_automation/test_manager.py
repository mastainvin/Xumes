import logging
import textwrap
import time
import traceback
from abc import abstractmethod

import multiprocess
from typing import List, Dict, Tuple

from tabulate import tabulate
import xml.etree.ElementTree as et

from xumes.core.colors import bcolors
from xumes.core.modes import TEST_MODE, RENDER_MODE
from xumes.assertions.assertion_bucket import AssertionReport
from xumes.test_automation.episode_control import DefaultEpisodeControlFactory
from xumes.test_automation.feature_strategy import FeatureStrategy, Scenario
from xumes.communication.i_com_game_engine import IComGameEngine
from xumes.test_automation.registries import config_registry, given_registry, \
    when_registry, then_registry

from xumes.communication.implementations.socket_impl.com_game_instance_socket import ComGameInstanceSocket

from xumes.test_automation.game_instance_service import GameInstanceService
from xumes.test_automation.test_runner import TestRunner


class ScenarioData:

    def __init__(self, test_runner: GameInstanceService = None, process: multiprocess.Process = None, ip: str = None,
                 port: int = None, pid: int = None):
        self.test_runner = test_runner
        self.process = process
        self.ip = ip
        self.port = port
        self.pid = pid


class TestManager:
    """
    A class that manages the execution of tests in a game environment.

    The TestManager class is responsible for loading and running tests in a game environment. It provides functionality
    for creating game services, running tests, and managing communication with the training manager.
    """

    def __init__(self, comm_service: IComGameEngine,
                 feature_strategy: FeatureStrategy,
                 mode: str = TEST_MODE, timesteps=None, iterations=None, do_logs: bool = False,
                 logging_level=logging.NOTSET, fps_limit=-1, render=False,
                 episode_control_factory=DefaultEpisodeControlFactory()
                 ):
        self._comm_service: IComGameEngine = comm_service
        self._scenario_datas: Dict[Scenario, ScenarioData] = {}
        self._mode = mode
        self._timesteps = timesteps
        self._iterations = iterations
        self._feature_strategy: FeatureStrategy = feature_strategy
        self._assertion_queue = multiprocess.Queue()
        self.do_logs = do_logs
        self._logging_level = logging_level
        self._delta_time = 0
        self._fps_limit = fps_limit
        self._render = render
        self._features = []
        self._episode_control_factory = episode_control_factory

    def add_test_runner_data(self, scenario: Scenario, ip: str, port: int):
        # Add a game service data to the list of game services data
        self._scenario_datas[scenario] = ScenarioData(ip=ip, port=port)

    def _init_logging(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)

    def test_all(self, path) -> None:
        try:
            test_time_start = time.time()

            # Retrieve features and scenarios
            self._feature_strategy.retrieve_features()
            self._features = self._feature_strategy.features

            # Check if all tests are finished
            active_processes = multiprocess.Value('i', 0)

            # For all scenarios in each feature, we run the test
            for feature in self._features:
                logging.info(f"{bcolors.OKBLUE + bcolors.BOLD}Feature: {feature.name}{bcolors.ENDC}")

                # Run the feature (exec all scenarios)
                self._run_feature(feature, active_processes)

                # Wait for all tests to be finished
                while active_processes.value > 0:
                    time.sleep(1)

                # Stop all scenarios
                feature_scenarios_data = []
                for scenario in feature.scenarios:
                    feature_scenarios_data.append(self._scenario_datas[scenario])
                    self._scenario_datas.pop(scenario)

                self._comm_service.stop_scenarios([scenario_data.pid for scenario_data in feature_scenarios_data])

                for process in feature.processes:
                    process.join()
                    process.terminate()

            test_time_end = time.time()
            self._delta_time = round(test_time_end - test_time_start, 3)

            if self._mode == TEST_MODE or self._mode == RENDER_MODE:
                self._assert()
            else:
                converted_time = time.strftime("%H:%M:%S", time.gmtime(self._delta_time))
                print(f"{bcolors.OKGREEN}Training finished in {converted_time}s.{bcolors.ENDC}")

        except KeyboardInterrupt as e:
            logging.info(f"{bcolors.FAIL}Xumes interrupted by user.{bcolors.ENDC}")
        except Exception as e:
            logging.error(f"{bcolors.FAIL}Error occurs while testing: {e}{bcolors.ENDC}")
            logging.error(traceback.format_exc())
        finally:
            # Close all game processes
            self._comm_service.stop_scenarios([scenario_data.pid for scenario_data in self._scenario_datas.values()])

            # Close all processes
            for feature in self._features:
                for process in feature.processes:
                    process.join()
                    process.terminate()

    def list_features(self, path):
        try:
            # Retrieve features and scenarios
            self._feature_strategy.retrieve_features()
            self._features = self._feature_strategy.features
            width = 80

            # Create a list of rows for the table
            table_data = []
            for feature in self._features:
                header = f"{bcolors.OKBLUE + bcolors.BOLD}Feature: {feature.name}{bcolors.ENDC}"
                table_data.append([header, "", ""])
                for scenario in feature.scenarios:
                    tags = ', '.join(scenario.tags)
                    wrapped_tags = textwrap.fill(tags, width=50, subsequent_indent=' ' * 8)
                    table_data.append([f"  {scenario.name}", f"{scenario.steps}.py", wrapped_tags])

            # Define table headers
            headers = [bcolors.UNDERLINE + bcolors.BOLD + "Feature/Scenario" + bcolors.ENDC,
                       bcolors.UNDERLINE + bcolors.BOLD + "Steps file" + bcolors.ENDC,
                       bcolors.UNDERLINE + bcolors.BOLD + "Tags" + bcolors.ENDC]

            # Print the table
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        except Exception as e:
            logging.error(f"{bcolors.FAIL}Error occurs while listing features: {e}{bcolors.ENDC}")

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
        converted_time = time.strftime("%H:%M:%S", time.gmtime(self._delta_time))

        # Create XML structure
        testsuite = et.Element('testsuite', {
            'name': 'TestSuite',
            'tests': str(nb_test),
            'failures': str(nb_test - successes),
            'errors': '0',
            'skipped': '0',
            'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()),
            'time': str(self._delta_time)
        })

        for result in results:
            testcase = et.SubElement(testsuite, 'testcase', {
                'classname': result.class_name,
                'name': result.test_name,
                'time': result.time
            })
            if not result.passed:
                failure = et.SubElement(testcase, 'failure', {
                    'message': result.error_logs,
                    'type': 'AssertionError'
                })
                failure.text = result.error_logs

        # Write XML to file
        xml_file = "test-results.xml"
        tree = et.ElementTree(testsuite)
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

        # Print the formatted report to the console
        self._print_formatted_report(xml_file)

    def _print_formatted_report(self, xml_file):
        tree = et.parse(xml_file)
        root = tree.getroot()

        header = f"{bcolors.BOLD}{bcolors.UNDERLINE}TEST REPORT{bcolors.ENDC}\n"
        summary = (
            f"Total Tests: {bcolors.BOLD}{root.attrib['tests']}{bcolors.ENDC}\n"
            f"Failures: {bcolors.BOLD}{bcolors.FAIL}{root.attrib['failures']}{bcolors.ENDC}\n"
            f"Errors: {bcolors.BOLD}{bcolors.FAIL}{root.attrib['errors']}{bcolors.ENDC}\n"
            f"Skipped: {bcolors.BOLD}{root.attrib['skipped']}{bcolors.ENDC}\n"
            f"Time: {bcolors.BOLD}{root.attrib['time']}{bcolors.ENDC}\n"
        )

        border = f"{bcolors.GREY}{'=' * 50}{bcolors.ENDC}"
        print(f"{bcolors.HEADER}{header}{bcolors.ENDC}")
        print(f"{border}")
        print(f"{bcolors.OKBLUE}{summary}{bcolors.ENDC}")
        print(f"{border}\n")

        for testcase in root.findall('testcase'):
            classname = testcase.attrib['classname']
            name = testcase.attrib['name']
            time = testcase.attrib['time']
            failure = testcase.find('failure')
            status = "PASSED"
            message = ""
            if failure is not None:
                status = "FAILED"
                message = failure.attrib['message']

            status_icon = "✅" if status == "PASSED" else "❌"
            status_color = bcolors.OKGREEN if status == "PASSED" else bcolors.FAIL
            print(f"{status_color}{status_icon} Test Case: {name}{bcolors.ENDC}")
            print(f"  Class: {classname}")
            print(f"  Time: {time}")
            print(f"  Status: {status_color}{status}{bcolors.ENDC}")
            if message:
                print(f"  Message: {message}")
            print(f"{bcolors.GREY}{'-' * 50}{bcolors.ENDC}")

    def _run_feature(self, feature, active_processes):

        scenarios_methods: List[Dict] = []

        for scenario in feature.scenarios:
            self.add_test_runner_data(scenario=scenario, ip="127.0.0.1", port=0)

            registry_queue = multiprocess.Queue()
            registry_queue.put((config_registry, given_registry, when_registry, then_registry))

            test_runner = TestRunner(GameInstanceService(ComGameInstanceSocket(host="127.0.0.1")),
                                     self._timesteps, self._iterations, self._mode, scenario.feature.name,
                                     scenario.name,
                                     self._assertion_queue, scenario.steps, registry_queue,
                                     self._episode_control_factory.create(self._timesteps, self._iterations),
                                     )

            self._scenario_datas[scenario].test_runner = test_runner

            methods = test_runner.config()

            scenarios_methods.append({
                "name": scenario.name,
                "methods": methods,
                "fps_limit": self._fps_limit,
                "render": self._render
            })

        # Make call to api to start the game instances
        ports_pids: Dict[scenario, Tuple[int, int]] = self._comm_service.start_scenarios(scenarios_methods,
                                                                                         feature.scenarios,
                                                                                         self._fps_limit, self._render)

        for scenario in ports_pids:
            self._scenario_datas[scenario].port = ports_pids[scenario][0]
            self._scenario_datas[scenario].pid = ports_pids[scenario][1]
            self._scenario_datas[scenario].test_runner.run(ports_pids[scenario][0])

        self._run_scenarios(feature=feature, scenario_datas=self._scenario_datas, active_processes=active_processes)

    @abstractmethod
    def _run_scenarios(self, feature, scenario_datas, active_processes):
        raise NotImplementedError


class DummyTestManager(TestManager):
    def _run_scenarios(self, feature, scenario_datas, active_processes):
        pass
