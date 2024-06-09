import numpy as np
from scipy.stats import ttest_1samp
from statsmodels.stats.proportion import proportions_ztest


def check_equal_values(sample, pop_mean):
    if all(value == pop_mean for value in sample):
        return True
    else:
        return False


def check_all_equal_values(sample):
    if len(set(sample)) == 1:
        return True
    else:
        return False


def hypothesis_test(sample, pop_mean, alpha):
    # Case if all values are equals
    if check_equal_values(sample, pop_mean):  # if all values are equals to pop_mean
        return None, None, None, None, False
    elif check_all_equal_values(sample):  # if all values are equals
        return None, None, None, None, True

    # Case if all values are not equals

    # Compute Student's t-test
    t_statistic, p_value_t = ttest_1samp(sample, pop_mean)

    # Compute Proportions z-test we need to add 0.00000000001 to avoid division by zero
    count = sum([1 for value in sample if value == pop_mean]) + 0.00000000001
    nobs = len(sample) + 0.00000000001
    _, p_value_prop = proportions_ztest(count, nobs, pop_mean)

    # Compute combined p-value
    p_value_combined = min(p_value_t, p_value_prop) * 2

    # Check if the difference is significant
    if p_value_combined < alpha:
        significant_difference = True
    else:
        significant_difference = False

    return t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference


class IAssertionStrategy:
    """
    Implements the Strategy design pattern to define the interface for assertions
    """

    def test(self, data) -> bool:
        raise NotImplementedError


class Assertion(IAssertionStrategy):
    """
    Abstract class for assertions
    Implements the test method of the IAssertionStrategy interface
    and compute the hypothesis test for the given data
    """

    def __init__(self, value=None):
        self._value = value
        if value is not None:
            self._type = type(value)
        else:
            self._type = None

    def test(self, data) -> bool:
        if self._type is None:
            raise NotImplementedError("Assertion type is not defined")
        if len(data) == 0:
            raise ValueError("Data is empty")
        if not isinstance(data[0], self._type):
            raise TypeError("Data type is not equal to assertion type")

        return False


class AssertionStatistical(Assertion):

    def __init__(self, value=None, alpha=0.001):
        super().__init__(value)
        self._alpha = alpha


class AssertionEqualStatistical(AssertionStatistical):
    """
    Overloads the test method of the Assertion class to test if the mean of the data is equal to the given value
    """

    def test(self, data) -> bool:
        super().test(data)

        value = self._value
        if self._type != float and self._type != int:
            data = np.array([1 if x == self._value else -1 for x in data])
            value = 1

        t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data, value,
                                                                                                         self._alpha)

        return not significant_difference


class AssertionBetweenStatistical(AssertionStatistical):
    """
    Overloads the test method of the Assertion class to test if the mean of the data is between the given values
    """

    def __init__(self, min_value, max_value, alpha=0.001):
        super().__init__(alpha=alpha)

        if min_value > max_value:
            min_value, max_value = max_value, min_value
        elif min_value == max_value:
            raise ValueError("min_value and max_value cannot be equal")

        if type(min_value) != type(max_value):
            raise TypeError("min_value and max_value must have the same type")

        self._min_value = min_value
        self._max_value = max_value
        self._type = type(min_value)

    def test(self, data) -> bool:
        super().test(data)

        data = np.array([1 if self._min_value <= x <= self._max_value else -1 for x in data])
        value = 1

        t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                         value,
                                                                                                         self._alpha)

        if p_value_combined:
            return p_value_combined > self._alpha

        return not significant_difference


class AssertionLessThanStatistical(AssertionStatistical):
    """
    Overloads the test method of the Assertion class to test if the mean of the data is less than the given value
    """

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x < self._value else -1 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)

            if p_value_combined and t_statistic:
                return p_value_combined / 2 < self._alpha and t_statistic < 0
            else:
                return np.mean(data) < self._value


class AssertionLessThanOrEqualStatistical(AssertionStatistical):
    """
    Overloads the test method of the Assertion class to test if the mean of the data is less than or equal to the given value
    """

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x <= self._value else -1 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)
            if t_statistic:
                return t_statistic < 0
            else:
                return np.mean(data) <= self._value


class AssertionGreaterThanStatistical(AssertionStatistical):
    """
    Overloads the test method of the Assertion class to test if the mean of the data is greater than the given value
    """

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x > self._value else 0 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)

            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)

            if p_value_combined and t_statistic:
                return p_value_combined / 2 < self._alpha and t_statistic > 0
            else:
                return np.mean(data) > self._value


class AssertionGreaterThanOrEqualStatistical(AssertionStatistical):
    """
    Overloads the test method of the Assertion class to test if the mean of the data is greater than or equal to the given value
    """

    def test(self, data) -> bool:
        super().test(data)

        if self._type != float and self._type != int:
            data = np.array([1 if x >= self._value else -1 for x in data])
            value = 1

            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             value,
                                                                                                             self._alpha)
            return not significant_difference

        else:
            t_statistic, p_value_t, p_value_prop, p_value_combined, significant_difference = hypothesis_test(data,
                                                                                                             self._value,
                                                                                                             self._alpha)
            if t_statistic:
                return t_statistic > 0
            else:
                return np.mean(data) >= self._value


class AssertionEqual(Assertion):

    def test(self, data) -> bool:
        super().test(data)
        return any([value == self._value for value in data])


class AssertionBetween(Assertion):

    def __int__(self, min_value, max_value):
        super().__init__()
        if min_value > max_value:
            min_value, max_value = max_value, min_value
        elif min_value == max_value:
            raise ValueError("min_value and max_value cannot be equal")

        if type(min_value) != type(max_value):
            raise TypeError("min_value and max_value must have the same type")

        self._min_value = min_value
        self._max_value = max_value
        self._type = type(min_value)

    def test(self, data) -> bool:
        super().test(data)
        return any([self._min_value <= value <= self._max_value for value in data])


class AssertionLessThan(Assertion):

    def test(self, data) -> bool:
        super().test(data)
        return any([value < self._value for value in data])


class AssertionLessThanOrEqual(Assertion):

    def test(self, data) -> bool:
        super().test(data)
        return any([value <= self._value for value in data])


class AssertionGreaterThan(Assertion):

    def test(self, data) -> bool:
        super().test(data)
        return any([value > self._value for value in data])


class AssertionGreaterThanOrEqual(Assertion):

    def test(self, data) -> bool:
        super().test(data)
        return any([value >= self._value for value in data])
