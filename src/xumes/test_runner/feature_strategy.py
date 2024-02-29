import importlib.util
import json
import multiprocess
import os
from abc import ABC, abstractmethod
from typing import List

from xumes.core.modes import TEST_MODE, RENDER_MODE
from xumes.test_runner.assertion import AssertionEqual
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
                         communication_service: ICommunicationServiceGame = None, mode: str = TEST_MODE, ):
                super().__init__(communication_service)
                self._feature = feature_name
                self._scenario = scenario_name
                self._mode = mode
                self._number_of_steps = 0
                self._number_max_of_steps = number_max_of_steps
                self._number_of_tests = 1
                self._number_max_of_tests = number_max_of_tests

                self._assertion_bucket = AssertionBucket(test_name=f"{self._feature}/{self._scenario}",
                                                         queue=test_queue)

            def run(self, port: int):
                super().run(port)
                self.push_args({
                    "when": {
                        "first_pipe": 1,
                        "second_pipe": 0
                    }})
                self.given()
                self.when()

            def _test_finished(self) -> bool:
                return self._number_of_tests >= self._number_max_of_tests

            def episode_finished(self) -> bool:
                # when an episode is finished, we collect the assertions
                finished = self._test_finished()
                self._number_of_tests += 1
                if self._mode == TEST_MODE:
                    if finished:
                        self._do_assert()
                        exit(0)

                    else:
                        try:
                            assertions_dicts = self.then()
                            self._assertion_bucket.assert_from_dict(assertions_dicts)
                        except KeyError:
                            pass

                return True

            def _do_assert(self) -> None:
                assertions_dicts = self.then()
                self._assertion_bucket.assert_from_dict(assertions_dicts)

                self._assertion_bucket.assertion_mode()
                self._assertion_bucket.assert_from_dict(assertions_dicts)

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
