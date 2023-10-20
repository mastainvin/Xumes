import time

import multiprocess
from typing import List

from xumes.game_module.assertion import IAssertionStrategy
from xumes.game_module.assertion_factory import AssertionFactory
from xumes.game_module.assertion_result import AssertionResult


class AssertionReport:

    def __init__(self, passed: bool, error_logs: str, test_name: str):
        self.passed = passed
        self.error_logs = error_logs
        self.test_name = test_name

    def __getstate__(self):
        return self.passed, self.error_logs, self.test_name

    def __setstate__(self, state):
        self.passed, self.error_logs, self.test_name = state


class AssertionBucketState:

    def __init__(self, assertion_bucket):
        self._assertion_bucket = assertion_bucket

    def action(self, *args, **kwargs):
        raise NotImplementedError


class CollectState(AssertionBucketState):

    def action(self, *args, **kwargs):
        if 'data' in kwargs:
            self._assertion_bucket.do_collect(kwargs['data'])
        else:
            raise ValueError("Missing data argument")


class AssertState(AssertionBucketState):

    def action(self, *args, **kwargs):
        if 'expected' in kwargs and 'assertion_strategy' in kwargs and 'opposite' in kwargs:
            self._assertion_bucket.do_assert(kwargs['expected'], kwargs['assertion_strategy'], kwargs['opposite'])
        elif 'expected' in kwargs and 'assertion_strategy' in kwargs:
            self._assertion_bucket.do_assert(kwargs['expected'], kwargs['assertion_strategy'])
        else:
            raise ValueError("Missing expected or assertion_strategy argument")


class AssertionBucket:
    """
    A class that holds a list of lists of values to assert.
    Each list of values is a test case.
    We then iterate over each test case and assert the values.
    """
    ASSERT_MODE = "assert"
    COLLECT_MODE = "collect"

    def __init__(self, test_name, queue: multiprocess.Queue, assertion_factory=AssertionFactory()):
        super().__init__()
        self._data = []
        self._results: List[AssertionResult] = []
        self._iterator = 0
        self._test_name = test_name
        self._collect_state = CollectState(self)
        self._assert_state = AssertState(self)
        self._state = self._collect_state
        self._queue = queue
        self._passed = True
        self._assertion_factory: AssertionFactory = assertion_factory

    def reset_iterator(self):
        self._iterator = 0

    def collect_mode(self):
        self._state = self._collect_state

    def assertion_mode(self):
        self._state = self._assert_state

    def _collect_or_assert(self, data, expected, assertion_strategy: IAssertionStrategy, opposite=False):
        self._state.action(data=data, expected=expected, assertion_strategy=assertion_strategy, opposite=opposite)

    def assert_true(self, data):
        self._state.action(data=data, expected=True, assertion_strategy=self._assertion_factory.assertion_equal(True),
                           opposite=False)

    def assert_false(self, data):
        self._state.action(data=data, expected=False, assertion_strategy=self._assertion_factory.assertion_equal(False),
                           opposite=False)

    def assert_equal(self, data, expected):
        self._state.action(data=data, expected=expected,
                           assertion_strategy=self._assertion_factory.assertion_equal(expected))

    def assert_not_equal(self, data, expected):
        self._state.action(data=data, expected=expected,
                           assertion_strategy=self._assertion_factory.assertion_equal(expected), opposite=True)

    def assert_greater_than(self, data, expected):
        self._state.action(data=data, expected=expected,
                           assertion_strategy=self._assertion_factory.assertion_greater_than(expected))

    def assert_greater_than_or_equal(self, data, expected):
        self._state.action(data=data, expected=expected,
                           assertion_strategy=self._assertion_factory.assertion_greater_than_or_equal(expected))

    def assert_less_than(self, data, expected):
        self._state.action(data=data, expected=expected,
                           assertion_strategy=self._assertion_factory.assertion_less_than(expected))

    def assert_less_than_or_equal(self, data, expected):
        self._state.action(data=data, expected=expected,
                           assertion_strategy=self._assertion_factory.assertion_less_than_or_equal(expected))

    def assert_between(self, data, expected_min, expected_max):
        self._state.action(data, expected=(expected_min, expected_max),
                           assertion_strategy=self._assertion_factory.assertion_between(expected_min,
                                                                                        expected_max))

    def assert_not_between(self, data, expected_min, expected_max):
        self._state.action(data=data, expected=(expected_min, expected_max),
                           assertion_strategy=self._assertion_factory.assertion_between(expected_min,
                                                                                        expected_max),
                           opposite=True)

    def do_collect(self, other):
        if self._iterator < len(self._data):
            self._data[self._iterator].append(other)
        else:
            self._data.append([other])
        self._iterator += 1

    def do_assert(self, expected, assertion_strategy: IAssertionStrategy, opposite=False):
        # Get the actual value and assert it
        actual = self._data[self._iterator]
        r = assertion_strategy.test(actual)
        if opposite:  # If we want to assert the opposite
            r = not r
        if not r:
            self._passed = False
        self._results.append(AssertionResult(
            fail_message=f"Test {self._test_name} FAILED on {self._iterator + 1}th assertion",
            passed=r,
            actual=actual,
            expected=expected
        ))
        self._iterator += 1

    def send_results(self):
        error_logs = ""
        for assertion_result in self._results:
            if not assertion_result.passed:
                error_logs += f"\n{assertion_result.fail_message:50}\n" \
                              f"{'Actual':10}: {assertion_result.actual} \n" \
                              f"{'Expected':10}: {assertion_result.expected}\n"

        self._queue.put(AssertionReport(passed=self._passed,
                                        error_logs=error_logs,
                                        test_name=self._test_name
                                        ))
        time.sleep(0.5)

    def clear(self):
        self._data.clear()
        self._results.clear()
        self._iterator = 0
