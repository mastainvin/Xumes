import importlib.util
import json
import multiprocess
import os
from abc import ABC, abstractmethod
from typing import List

from xumes.core.modes import TEST_MODE, RENDER_MODE
from xumes.test_runner.assertion_bucket import AssertionBucket
from xumes.test_runner.i_communication_service_game import ICommunicationServiceGame
from xumes.test_runner.test_runner import TestRunner


class Scenario:

    def __init__(self, name: str = None, steps: str = None, feature=None):
        self.name = name
        self.steps: str = steps
        self.feature: Feature = feature


class Feature:

    def __init__(self, scenarios=None, name: str = None):
        if scenarios is None:
            scenarios = []
        self.scenarios: List[Scenario] = scenarios
        self.name = name


class FeatureStrategy(ABC):
    """
    FeatureStrategy is a class that implements the strategy pattern to define a way to get
    all features.
    """

    def __init__(self, alpha: float = 0.001):
        self.features: List[Feature] = []
        self._steps_files: List[str] = []

        self._alpha = alpha

    def build_test_runner(self, timesteps: int = None, iterations: int = None,
                          mode: str = TEST_MODE, scenario: Scenario = None, test_queue: multiprocess.Queue = None,
                          comm_service: ICommunicationServiceGame = None):
        # Get steps
        feature_name = scenario.feature.name
        scenario_name = scenario.name

        class ConcreteTestRunner(TestRunner):
            def __init__(self, number_max_of_steps: int = None, number_max_of_tests: int = None,
                         communication_service: ICommunicationServiceGame = None):
                super().__init__(communication_service)
                self._feature = feature_name
                self._scenario = scenario_name
                self._mode = mode
                self._number_of_steps = 0
                self._number_max_of_steps = number_max_of_steps
                self._number_of_tests = 0
                self._number_max_of_tests = number_max_of_tests

                self._assertion_bucket = AssertionBucket(test_name=f"{self._feature}/{self._scenario}",
                                                         queue=test_queue)
                # exec given
                self.given()
                # exec when
                self.when()

            def _continue_test(self) -> bool:
                return (self._number_max_of_steps is None or self._number_of_steps < self._number_max_of_steps) and (
                        self._number_max_of_tests is None or self._number_of_tests < self._number_max_of_tests)

            def _make_loop(self) -> bool:
                # Loop content method return False if the test is finished

                # Check if the test is finished
                finished = not self._continue_test()
                self._number_of_steps += 1
                if finished:
                    # If the test is finished, we send to the training manager that the test is finished
                    # self._assertion_bucket.collect_mode()
                    # self._assertion_bucket.do_collect()
                    try:
                        self.is_finished = True
                    finally:
                        return False

                return True

            def run_test(self) -> None:
                while True:
                    if not self._make_loop():
                        break
                self._do_assert_and_log()

            def _do_assert_and_log(self) -> None:
                if self._mode == TEST_MODE or self._mode == RENDER_MODE:
                    # If the test is finished, we assert the test
                    self._assertion_bucket.assertion_mode()

                    # if
                    # exec_registry_function(registry=then_r[steps], game_context=self, scenario_name=scenario_name)

                    self._assertion_bucket.send_results()
                    self._assertion_bucket.clear()
                    self._assertion_bucket.collect_mode()

            def reset(self) -> None:
                if self._mode == TEST_MODE or self._mode == RENDER_MODE:
                    # then
                    self._assertion_bucket.reset_iterator()
                # when
                self.when()
                self._number_of_tests += 1

        return ConcreteTestRunner(timesteps, iterations, comm_service)

    @abstractmethod
    def retrieve_feature(self, path: str):
        """
        Get all features.
        """
        raise NotImplementedError
