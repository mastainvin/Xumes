import importlib.util
import json
import sys

import multiprocess
import os
from abc import ABC, abstractmethod
from typing import List

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.core.modes import TEST_MODE
from xumes.core.registry import create_registry_content, exec_registry_function, create_registry
from xumes.test_runner.assertion_bucket import AssertionBucket
from xumes.test_runner.i_communication_service import ICommunicationService
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
        self.processes = []


config = create_registry()
given = create_registry_content()
when = create_registry_content()
then = create_registry_content()

config_registry = config.all
given_registry = given.all
when_registry = when.all
then_registry = then.all


class FeatureStrategy(ABC):
    """
    FeatureStrategy is a class that implements the strategy pattern to define a way to get
    all features.
    """

    def __init__(self, alpha: float = 0.001, steps_path: str = "./"):
        self.features: List[Feature] = []
        self._steps_files: List[str] = []

        self.given = given
        self.when = when
        self.then = then
        self.config = config

        self._alpha = alpha
        self._load_tests(steps_path)

    def _load_tests(self, path: str = "./"):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        sys.path.insert(0, parent_dir)

        for file in os.listdir(path):
            if file.endswith(".py"):
                module_path = os.path.join(path, file)
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

                self._steps_files.append(file[:-3])

    def build_test_runner(self, timesteps: int = None, iterations: int = None,
                          mode: str = TEST_MODE, scenario: Scenario = None, test_queue: multiprocess.Queue = None,
                          comm_service: ICommunicationService = None, registry_queue: multiprocess.Queue = None):
        # Get steps
        steps = scenario.steps
        feature_name = scenario.feature.name
        scenario_name = scenario.name

        config_r, given_r, when_r, then_r = registry_queue.get()

        class ConcreteTestRunner(TestRunner):
            def __init__(self, number_max_of_steps: int = None, number_max_of_tests: int = None,
                         communication_service: ICommunicationService = None, mode: str = TEST_MODE, ):
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

            def config(self):
                config_r[steps](self)
                return self.driver()

            def given(self):
                exec_registry_function(registry=given_r[steps], game_context=self, scenario_name=scenario_name)

            def when(self):
                return exec_registry_function(registry=when_r[steps], game_context=self, scenario_name=scenario_name)

            def then(self):
                return exec_registry_function(registry=then_r[steps], game_context=self, scenario_name=scenario_name)

            def assert_true(self, condition: bool) -> None:
                self._assertion_bucket.assert_true(data=condition)

            def assert_false(self, condition: bool) -> None:
                self._assertion_bucket.assert_false(data=condition)

            def assert_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_equal(data=actual, expected=expected)

            def assert_not_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_not_equal(data=actual, expected=expected)

            def assert_greater(self, actual, expected) -> None:
                self._assertion_bucket.assert_greater_than(data=actual, expected=expected)

            def assert_greater_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_greater_than_or_equal(data=actual, expected=expected)

            def assert_less(self, actual, expected) -> None:
                self._assertion_bucket.assert_less_than(data=actual, expected=expected)

            def assert_less_equal(self, actual, expected) -> None:
                self._assertion_bucket.assert_less_than_or_equal(data=actual, expected=expected)

            def assert_between(self, actual, expected_min, expected_max) -> None:
                self._assertion_bucket.assert_between(data=actual, expected_min=expected_min, expected_max=expected_max)

            def assert_not_between(self, actual, expected_min, expected_max) -> None:
                self._assertion_bucket.assert_not_between(data=actual, expected_min=expected_min,
                                                          expected_max=expected_max)

            def episode_finished(self) -> bool:
                # when an episode is finished, we collect the assertions
                if self._mode == TEST_MODE:
                    if self._number_of_tests >= self._number_max_of_tests:
                        self._do_assert()
                        raise RunningEndsError
                    else:
                        try:
                            self.then()
                            self._assertion_bucket.reset_iterator()
                        except KeyError:
                            pass
                    self._number_of_tests += 1

                return True

            def _do_assert(self) -> None:
                self._assertion_bucket.assertion_mode()
                self.then()
                self._assertion_bucket.send_results()
                self._assertion_bucket.clear()
                self._assertion_bucket.collect_mode()

        return ConcreteTestRunner(timesteps, iterations, comm_service, mode)

    @abstractmethod
    def retrieve_feature(self, path: str):
        """
        Get all features.
        """
        raise NotImplementedError


class DummyFeatureStrategy(FeatureStrategy):
    def retrieve_feature(self, path: str):
        pass
