from xumes.assertions.assertion_bucket import AssertionBucket
from xumes.entity.entity_manager import EntityRegistry
from xumes.test_automation.driver import Driver


class TestContext:
    """
    Class responsible for providing the test context to the test scripts.
    The test context provides limited access to the test automation framework.
    Access:
        - Entities: Access to the entities registered in the entity registry.
        - Driver: Access to the driver. (call game methods, etc.)
        - Assertions: Access to the assertion methods.
    """

    def __init__(self, entity_registry: EntityRegistry, driver: Driver, assertion_bucket: AssertionBucket):
        self._entity_registry = entity_registry
        self.driver = driver
        self._assertion_bucket = assertion_bucket

    def __getattr__(self, item):
        return self._entity_registry.get(item)

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
