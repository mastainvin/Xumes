import time

import multiprocess
from typing import List, Dict

from jsonpickle.compat import iterator

from xumes.assertions.assertion import IAssertionStrategy
from xumes.assertions.assertion_factory import AssertionFactory
from xumes.assertions.assertion_result import AssertionResult


class AssertionReport:

    def __init__(self, passed: bool, error_logs: str, test_name: str, class_name: str, time: str):
        self.passed = passed
        self.error_logs = error_logs
        self.test_name = test_name
        self.class_name = class_name
        self.time = time

    def __getstate__(self):
        return self.passed, self.error_logs, self.test_name, self.class_name, self.time

    def __setstate__(self, state):
        self.passed, self.error_logs, self.test_name, self.class_name, self.time = state


class AssertionBucket:
    """
    A class that asserts values immediately upon adding them.
    Each assertion is evaluated as it is added, and the overall result is an 'or' combination of all assertions.
    """
    def __init__(self, test_name, class_name, queue: multiprocess.Queue, assertion_factory=AssertionFactory()):
        super().__init__()
        self._results: List = []
        self._test_name = test_name
        self._class_name = class_name
        self._queue = queue
        self._assertion_factory: AssertionFactory = assertion_factory
        self.iterator = 0

    def _assert_and_store(self, data, expected, assertion_strategy: IAssertionStrategy, opposite=False):
        r = assertion_strategy.test([data])
        if opposite:
            r = not r

        if self.iterator < len(self._results):
            assertion_result = self._results[self.iterator]
            assertion_result.actual.append(data)
            assertion_result.passed = r
        else:
            assertion_result = AssertionResult(
                fail_message=f"Test {self._test_name} FAILED" if not r else f"Test {self._test_name} PASSED",
                passed=r,
                actual=[data],
                expected=expected
            )
            self._results.append(assertion_result)

        self.iterator += 1

    def assert_true(self, data):
        self._assert_and_store(data=data, expected=True, assertion_strategy=self._assertion_factory.assertion_equal(True))

    def assert_false(self, data):
        self._assert_and_store(data=data, expected=False, assertion_strategy=self._assertion_factory.assertion_equal(False))

    def assert_equal(self, data, expected):
        self._assert_and_store(data=data, expected=expected, assertion_strategy=self._assertion_factory.assertion_equal(expected))

    def assert_not_equal(self, data, expected):
        self._assert_and_store(data=data, expected=expected, assertion_strategy=self._assertion_factory.assertion_equal(expected), opposite=True)

    def assert_greater_than(self, data, expected):
        self._assert_and_store(data=data, expected=expected, assertion_strategy=self._assertion_factory.assertion_greater_than(expected))

    def assert_greater_than_or_equal(self, data, expected):
        self._assert_and_store(data=data, expected=expected, assertion_strategy=self._assertion_factory.assertion_greater_than_or_equal(expected))

    def assert_less_than(self, data, expected):
        self._assert_and_store(data=data, expected=expected, assertion_strategy=self._assertion_factory.assertion_less_than(expected))

    def assert_less_than_or_equal(self, data, expected):
        self._assert_and_store(data=data, expected=expected, assertion_strategy=self._assertion_factory.assertion_less_than_or_equal(expected))

    def assert_between(self, data, expected_min, expected_max):
        self._assert_and_store(data, expected=(expected_min, expected_max), assertion_strategy=self._assertion_factory.assertion_between(expected_min, expected_max))

    def assert_not_between(self, data, expected_min, expected_max):
        self._assert_and_store(data=data, expected=(expected_min, expected_max), assertion_strategy=self._assertion_factory.assertion_between(expected_min, expected_max), opposite=True)

    def send_results(self, test_time: float):
        error_logs = ""
        passed = True

        for assertion_result in self._results:
            if not assertion_result.passed:
                error_logs += f"\n{assertion_result.fail_message:50}\n" \
                              f"{'Actual':10}: {assertion_result.actual} \n" \
                              f"{'Expected':10}: {assertion_result.expected}\n"
                passed = False

        assertion_report = AssertionReport(passed=passed,
                                           error_logs=error_logs,
                                           test_name=self._test_name,
                                           class_name=self._class_name,
                                           time=str(test_time)
                                           )

        self._queue.put(assertion_report)
        time.sleep(0.5)

    def clear(self):
        self._results.clear()

    def to_next_episode(self) -> bool:
        self.iterator = 0
        return self.passed()

    def passed(self):
        for assertion_result in self._results:
            if not assertion_result.passed:
                return False
        return True


class AssertionBucketTrain(AssertionBucket):

    def _assert_and_store(self, data, expected, assertion_strategy: IAssertionStrategy, opposite=False):
        r = assertion_strategy.test([data])
        if opposite:
            r = not r

        if self.iterator < len(self._results):
            self._results[self.iterator] = r
        else:
            self._results.append(r)

        self.iterator  += 1


    def passed(self):
        return all(self._results)