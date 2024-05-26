from xumes.test_runner.assertion import IAssertionStrategy, AssertionEqualStatistical, AssertionBetweenStatistical, \
    AssertionLessThanStatistical, AssertionLessThanOrEqualStatistical, AssertionGreaterThanStatistical, \
    AssertionGreaterThanOrEqualStatistical, AssertionGreaterThanOrEqual, AssertionGreaterThan, AssertionLessThanOrEqual, \
    AssertionLessThan, AssertionBetween, AssertionEqual


class IAssertionFactory:

    def assertion_equal(self, value) -> IAssertionStrategy:
        raise NotImplementedError

    def assertion_between(self, min_value, max_value) -> IAssertionStrategy:
        raise NotImplementedError

    def assertion_less_than(self, value) -> IAssertionStrategy:
        raise NotImplementedError

    def assertion_less_than_or_equal(self, value) -> IAssertionStrategy:
        raise NotImplementedError

    def assertion_greater_than(self, value) -> IAssertionStrategy:
        raise NotImplementedError

    def assertion_greater_than_or_equal(self, value) -> IAssertionStrategy:
        raise NotImplementedError


class AssertionFactoryStatistical(IAssertionFactory):

    def __init__(self, alpha=0.001):
        self._alpha = alpha

    def assertion_equal(self, value) -> IAssertionStrategy:
        return AssertionEqualStatistical(value, alpha=self._alpha)

    def assertion_between(self, min_value, max_value) -> IAssertionStrategy:
        return AssertionBetweenStatistical(min_value, max_value, alpha=self._alpha)

    def assertion_less_than(self, value) -> IAssertionStrategy:
        return AssertionLessThanStatistical(value, alpha=self._alpha)

    def assertion_less_than_or_equal(self, value) -> IAssertionStrategy:
        return AssertionLessThanOrEqualStatistical(value, alpha=self._alpha)

    def assertion_greater_than(self, value) -> IAssertionStrategy:
        return AssertionGreaterThanStatistical(value, alpha=self._alpha)

    def assertion_greater_than_or_equal(self, value) -> IAssertionStrategy:
        return AssertionGreaterThanOrEqualStatistical(value, alpha=self._alpha)


class AssertionFactory(IAssertionFactory):

    def assertion_equal(self, value) -> IAssertionStrategy:
        return AssertionEqual(value)

    def assertion_between(self, min_value, max_value) -> IAssertionStrategy:
        return AssertionBetween(min_value, max_value)

    def assertion_less_than(self, value) -> IAssertionStrategy:
        return AssertionLessThan(value)

    def assertion_less_than_or_equal(self, value) -> IAssertionStrategy:
        return AssertionLessThanOrEqual(value)

    def assertion_greater_than(self, value) -> IAssertionStrategy:
        return AssertionGreaterThan(value)

    def assertion_greater_than_or_equal(self, value) -> IAssertionStrategy:
        return AssertionGreaterThanOrEqual(value)
