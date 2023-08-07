from unittest import TestCase

from xumes.game_module.assertion import AssertionEqual, AssertionBetween, AssertionLessThan, AssertionGreaterThan, \
    AssertionLessThanOrEqual, AssertionGreaterThanOrEqual


class TestIAssertionStrategy(TestCase):

    def test_equal_not_same_type(self):
        int_assertion = AssertionEqual(1)
        float_assertion = AssertionEqual(1.0)
        self.assertRaises(TypeError, int_assertion.test, ["1.0"])
        self.assertRaises(TypeError, float_assertion.test, [1])

    def test_equal_no_data(self):
        int_assertion = AssertionEqual(1)
        self.assertRaises(ValueError, int_assertion.test, [])

    def test_equal_int(self):
        int_assertion = AssertionEqual(1)
        data = [1] * 100
        self.assertTrue(int_assertion.test(data))
        data2 = [2] * 100
        self.assertFalse(int_assertion.test(data2))
        data3 = [1, 2] * 50
        self.assertFalse(int_assertion.test(data3))

        data4 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self.assertTrue(int_assertion.test(data4))

    def test_equal_float(self):
        float_assertion = AssertionEqual(1.0)
        data = [1.0] * 100
        self.assertTrue(float_assertion.test(data))
        data2 = [2.0] * 100
        self.assertFalse(float_assertion.test(data2))
        data3 = [1.0, 2.0] * 50
        self.assertFalse(float_assertion.test(data3))

        data4 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0000000000000001, 1.0, 1.0, 1.0, 2.0]
        self.assertTrue(float_assertion.test(data4))

    def test_equal_bool(self):
        bool_assertion = AssertionEqual(True)
        data = [True] * 100
        self.assertTrue(bool_assertion.test(data))
        data2 = [False] * 100
        self.assertFalse(bool_assertion.test(data2))
        data3 = [True, False] * 50
        self.assertFalse(bool_assertion.test(data3))
        data4 = [True] * 95 + [False] * 5
        self.assertTrue(bool_assertion.test(data4))

    def test_equal_str(self):
        str_assertion = AssertionEqual('abc')
        data = ['abc'] * 100
        self.assertTrue(str_assertion.test(data))
        data2 = ['def'] * 100
        self.assertFalse(str_assertion.test(data2))
        data3 = ['abc', 'def'] * 50
        self.assertFalse(str_assertion.test(data3))
        data4 = ['abc'] * 95 + ['def'] * 5
        self.assertTrue(str_assertion.test(data4))

    def test_equal_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __eq__(self, other):
                return self.a == other.a

        obj_assertion = AssertionEqual(A(1))
        data = [A(1)] * 100
        self.assertTrue(obj_assertion.test(data))
        data2 = [A(2)] * 100
        self.assertFalse(obj_assertion.test(data2))
        data3 = [A(1), A(2)] * 50
        self.assertFalse(obj_assertion.test(data3))
        data4 = [A(1)] * 95 + [A(2)] * 5
        self.assertTrue(obj_assertion.test(data4))

    def test_equal_list(self):
        list_assertion = AssertionEqual([1, 2])
        data = [[1, 2]] * 100
        self.assertTrue(list_assertion.test(data))
        data2 = [[2, 1]] * 100
        self.assertFalse(list_assertion.test(data2))
        data3 = [[1, 2], [2, 1]] * 50
        self.assertFalse(list_assertion.test(data3))
        data4 = [[1, 2]] * 95 + [[2, 1]] * 5
        self.assertTrue(list_assertion.test(data4))

    def test_equal_tuple(self):
        tuple_assertion = AssertionEqual((1, 2))
        data = [(1, 2)] * 100
        self.assertTrue(tuple_assertion.test(data))
        data2 = [(2, 1)] * 100
        self.assertFalse(tuple_assertion.test(data2))
        data3 = [(1, 2), (2, 1)] * 50
        self.assertFalse(tuple_assertion.test(data3))
        data4 = [(1, 2)] * 95 + [(2, 1)] * 5
        self.assertTrue(tuple_assertion.test(data4))

    def test_equal_set(self):
        set_assertion = AssertionEqual({1, 2})
        data = [{1, 2}] * 100
        self.assertTrue(set_assertion.test(data))
        data2 = [{3, 1}] * 100
        self.assertFalse(set_assertion.test(data2))
        data3 = [{1, 2}, {2, 1}] * 50
        self.assertTrue(set_assertion.test(data3))
        data3 = [{1, 2}, {3, 4}] * 50
        self.assertFalse(set_assertion.test(data3))
        data4 = [{1, 2}] * 95 + [{2, 1}] * 5
        self.assertTrue(set_assertion.test(data4))

    def test_equal_dict(self):
        dict_assertion = AssertionEqual({1: 2})
        data = [{1: 2}] * 100
        self.assertTrue(dict_assertion.test(data))
        data2 = [{1: 3}] * 100
        self.assertFalse(dict_assertion.test(data2))
        data3 = [{1: 2}, {1: 3}] * 50
        self.assertFalse(dict_assertion.test(data3))
        data4 = [{1: 2}] * 95 + [{1: 3}] * 5
        self.assertTrue(dict_assertion.test(data4))

    def test_equal_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __eq__(self, other):
                return self.a == other.a

        list_assertion = AssertionEqual([A(1), A(2)])
        data = [[A(1), A(2)]] * 100
        self.assertTrue(list_assertion.test(data))
        data2 = [[A(2), A(1)]] * 100
        self.assertFalse(list_assertion.test(data2))
        data3 = [[A(1), A(2)], [A(2), A(1)]] * 50
        self.assertFalse(list_assertion.test(data3))
        data4 = [[A(1), A(2)]] * 95 + [[A(2), A(1)]] * 5
        self.assertTrue(list_assertion.test(data4))

    def test_equal_list_of_list(self):
        list_assertion = AssertionEqual([[1, 2], [3, 4]])
        data = [[[1, 2], [3, 4]]] * 100
        self.assertTrue(list_assertion.test(data))
        data2 = [[[3, 4], [1, 2]]] * 100
        self.assertFalse(list_assertion.test(data2))
        data3 = [[[1, 2], [3, 4]], [[3, 4], [1, 2]]] * 50
        self.assertFalse(list_assertion.test(data3))
        data4 = [[[1, 2], [3, 4]]] * 95 + [[[3, 4], [1, 2]]] * 5
        self.assertTrue(list_assertion.test(data4))

    def test_equal_list_of_str(self):
        list_assertion = AssertionEqual(['a', 'b'])
        data = [['a', 'b']] * 100
        self.assertTrue(list_assertion.test(data))
        data2 = [['b', 'a']] * 100
        self.assertFalse(list_assertion.test(data2))
        data3 = [['a', 'b'], ['b', 'a']] * 50
        self.assertFalse(list_assertion.test(data3))
        data4 = [['a', 'b']] * 95 + [['b', 'a']] * 5
        self.assertTrue(list_assertion.test(data4))

    def test_equal_list_of_bool(self):
        list_assertion = AssertionEqual([True, False])
        data = [[True, False]] * 100
        self.assertTrue(list_assertion.test(data))
        data2 = [[False, True]] * 100
        self.assertFalse(list_assertion.test(data2))
        data3 = [[True, False], [False, True]] * 50
        self.assertFalse(list_assertion.test(data3))
        data4 = [[True, False]] * 95 + [[False, True]] * 5
        self.assertTrue(list_assertion.test(data4))

    def test_between_int(self):
        int_assertion = AssertionBetween(1, 2)
        data = [1] * 100
        self.assertTrue(int_assertion.test(data))
        data = [3] * 50
        self.assertFalse(int_assertion.test(data))
        data2 = [3, 2] * 50
        self.assertFalse(int_assertion.test(data2))
        date3 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self.assertTrue(int_assertion.test(date3))

    def test_between_float(self):
        float_assertion = AssertionBetween(1.0, 2.0)
        data = [1.0] * 100
        self.assertTrue(float_assertion.test(data))
        data = [3.0] * 50 + [2.0] * 50
        self.assertFalse(float_assertion.test(data))
        data2 = [1.5] * 100 + [1.75] * 100
        self.assertTrue(float_assertion.test(data2))

    def test_between_str(self):
        str_assertion = AssertionBetween('a', 'b')
        data = ['a'] * 100
        self.assertTrue(str_assertion.test(data))
        data = ['c'] * 50 + ['b'] * 50
        self.assertFalse(str_assertion.test(data))
        data2 = ['a', 'b'] * 50
        self.assertTrue(str_assertion.test(data2))

    def test_between_bool(self):
        bool_assertion = AssertionBetween(False, True)
        data = [True] * 100
        self.assertTrue(bool_assertion.test(data))
        data = [False] * 50 + [True] * 50
        self.assertTrue(bool_assertion.test(data))
        data2 = [True, False] * 50
        self.assertTrue(bool_assertion.test(data2))

    def test_between_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __eq__(self, other):
                return self.a == other.a

            def __lt__(self, other):
                return self.a < other.a

            def __gt__(self, other):
                return self.a > other.a

            def __le__(self, other):
                return self.a <= other.a

            def __ge__(self, other):
                return self.a >= other.a

        obj_assertion = AssertionBetween(A(1), A(2))
        data = [A(1)] * 100
        self.assertTrue(obj_assertion.test(data))
        data = [A(3)] * 50 + [A(2)] * 50
        self.assertFalse(obj_assertion.test(data))
        data2 = [A(1), A(2)] * 50
        self.assertTrue(obj_assertion.test(data2))

    def test_less_int(self):
        int_assertion = AssertionLessThan(1)
        data = [0] * 100
        self.assertTrue(int_assertion.test(data))
        data = [1] * 100
        self.assertFalse(int_assertion.test(data))
        data2 = [2] * 100 + [3] * 100
        self.assertFalse(int_assertion.test(data2))

    def test_less_float(self):
        float_assertion = AssertionLessThan(1.0)
        data = [0.0] * 100
        self.assertTrue(float_assertion.test(data))
        data = [1.0] * 100
        self.assertFalse(float_assertion.test(data))
        data2 = [1.0] * 100 + [0.5] * 100
        self.assertTrue(float_assertion.test(data2))
        data3 = [1.0] * 100 + [1.0000000000000001] * 100
        self.assertFalse(float_assertion.test(data3))
        data4 = [1.0 + 1.5] * 100
        self.assertFalse(float_assertion.test(data4))

    def test_less_str(self):
        str_assertion = AssertionLessThan('abc')
        data = ['a'] * 100
        self.assertTrue(str_assertion.test(data))
        data = ['abc'] * 100
        self.assertFalse(str_assertion.test(data))
        data2 = ['b'] * 100
        self.assertFalse(str_assertion.test(data2))

    def test_less_bool(self):
        bool_assertion = AssertionLessThan(True)
        data = [False] * 100
        self.assertTrue(bool_assertion.test(data))
        data = [True] * 100
        self.assertFalse(bool_assertion.test(data))
        data2 = [False] * 50 + [True] * 50
        self.assertFalse(bool_assertion.test(data2))
        data3 = [False] * 95 + [True] * 5
        self.assertTrue(bool_assertion.test(data3))

    def test_less_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __lt__(self, other):
                return self.a < other.a

        obj_assertion = AssertionLessThan(A(1))
        data = [A(0)] * 100
        self.assertTrue(obj_assertion.test(data))
        data = [A(1)] * 100
        self.assertFalse(obj_assertion.test(data))
        data2 = [A(0), A(1)] * 50
        self.assertFalse(obj_assertion.test(data2))
        data3 = [A(0)] * 95 + [A(1)] * 5
        self.assertTrue(obj_assertion.test(data3))

    def test_less_equal_int(self):
        int_assertion = AssertionLessThanOrEqual(1)
        data = [0] * 100
        self.assertTrue(int_assertion.test(data))
        data = [1] * 100 + [0] * 100
        self.assertTrue(int_assertion.test(data))
        data2 = [2] * 100 + [3] * 100
        self.assertFalse(int_assertion.test(data2))


    def test_less_equal_float(self):
        float_assertion = AssertionLessThanOrEqual(1.0)
        data = [0.5] * 100
        self.assertTrue(float_assertion.test(data))
        data = [1.0] * 100
        self.assertTrue(float_assertion.test(data))
        data2 = [1.5] * 100 + [2.5] * 100
        self.assertFalse(float_assertion.test(data2))

    def test_less_equal_str(self):
        str_assertion = AssertionLessThanOrEqual('abc')
        data = ['a'] * 100
        self.assertTrue(str_assertion.test(data))
        data = ['abc'] * 100
        self.assertTrue(str_assertion.test(data))
        data2 = ['b'] * 100
        self.assertFalse(str_assertion.test(data2))

    def test_less_equal_bool(self):
        bool_assertion = AssertionLessThanOrEqual(True)
        data = [False] * 100
        self.assertTrue(bool_assertion.test(data))
        data = [True] * 100
        self.assertTrue(bool_assertion.test(data))
        data2 = [False] * 50 + [True] * 50
        self.assertTrue(bool_assertion.test(data2))
        data3 = [False] * 95 + [True] * 5
        self.assertTrue(bool_assertion.test(data3))

    def test_less_equal_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __le__(self, other):
                return self.a <= other.a

        obj_assertion = AssertionLessThanOrEqual(A(1))
        data = [A(0)] * 100
        self.assertTrue(obj_assertion.test(data))
        data = [A(1)] * 100
        self.assertTrue(obj_assertion.test(data))
        data2 = [A(2), A(1)] * 50
        self.assertFalse(obj_assertion.test(data2))
        data3 = [A(0)] * 95 + [A(1)] * 5
        self.assertTrue(obj_assertion.test(data3))

    def test_greater_int(self):
        int_assertion = AssertionGreaterThan(1)
        data = [0] * 100
        self.assertFalse(int_assertion.test(data))
        data = [1] * 100 + [0] * 100
        self.assertFalse(int_assertion.test(data))
        data2 = [2] * 100 + [3] * 100
        self.assertTrue(int_assertion.test(data2))
        data3 = [352, 386, 387, 388, 386, 387, 385, 389, 385, 389, 389, 386, 387, 387]
        int_assertion2 = AssertionGreaterThan(384)
        self.assertTrue(int_assertion2.test(data3))


    def test_greater_float(self):
        float_assertion = AssertionGreaterThan(1.0)
        data = [0.5] * 100
        self.assertFalse(float_assertion.test(data))
        data = [1.0] * 100
        self.assertFalse(float_assertion.test(data))
        data2 = [1.5] * 100 + [2.5] * 100
        self.assertTrue(float_assertion.test(data2))
        data3 = [1.0] * 100 + [2.0] * 100
        self.assertTrue(float_assertion.test(data3))
        data4 = [1.0] * 100 + [1.0000000000000001] * 100
        self.assertFalse(float_assertion.test(data4))

    def test_greater_str(self):
        str_assertion = AssertionGreaterThan('abc')
        data = ['a'] * 100
        self.assertFalse(str_assertion.test(data))
        data = ['abc'] * 100
        self.assertFalse(str_assertion.test(data))
        data2 = ['b'] * 100
        self.assertTrue(str_assertion.test(data2))

    def test_greater_bool(self):
        bool_assertion = AssertionGreaterThan(True)
        data = [False] * 100
        self.assertFalse(bool_assertion.test(data))
        data = [True] * 100
        self.assertFalse(bool_assertion.test(data))
        data2 = [False] * 50 + [True] * 50
        self.assertFalse(bool_assertion.test(data2))
        data3 = [False] * 95 + [True] * 5
        self.assertFalse(bool_assertion.test(data3))

    def test_greater_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __gt__(self, other):
                return self.a > other.a

        obj_assertion = AssertionGreaterThan(A(1))
        data = [A(0)] * 100
        self.assertFalse(obj_assertion.test(data))
        data = [A(1)] * 100
        self.assertFalse(obj_assertion.test(data))
        data2 = [A(0), A(1)] * 50
        self.assertFalse(obj_assertion.test(data2))
        data3 = [A(0)] * 95 + [A(1)] * 5
        self.assertFalse(obj_assertion.test(data3))
        data4 = [A(2)] * 95 + [A(0)] * 5
        self.assertTrue(obj_assertion.test(data4))

    def test_greater_equal_int(self):
        int_assertion = AssertionGreaterThanOrEqual(1)
        data = [0] * 100
        self.assertFalse(int_assertion.test(data))
        data = [1] * 100 + [0] * 100
        self.assertFalse(int_assertion.test(data))
        data2 = [2] * 100 + [3] * 100
        self.assertTrue(int_assertion.test(data2))
        data3 = [352, 386, 387, 388, 386, 387, 385, 389, 385, 389, 389, 386, 387, 387]
        int_assertion2 = AssertionGreaterThanOrEqual(384)
        self.assertTrue(int_assertion2.test(data3))
        data = [1] * 100
        self.assertTrue(int_assertion.test(data))
        data4 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2]
        self.assertTrue(int_assertion.test(data4))

    def test_greater_equal_float(self):
        float_assertion = AssertionGreaterThanOrEqual(1.0)
        data = [0.5] * 100
        self.assertFalse(float_assertion.test(data))
        data = [1.0] * 100
        self.assertTrue(float_assertion.test(data))
        data2 = [1.5] * 100 + [2.5] * 100
        self.assertTrue(float_assertion.test(data2))
        data3 = [1.0] * 100 + [2.0] * 100
        self.assertTrue(float_assertion.test(data3))
        data4 = [1.0] * 100 + [1.0000000000000001] * 100
        self.assertTrue(float_assertion.test(data4))

    def test_greater_equal_str(self):
        str_assertion = AssertionGreaterThanOrEqual('abc')
        data = ['a'] * 100
        self.assertFalse(str_assertion.test(data))
        data = ['abc'] * 100
        self.assertTrue(str_assertion.test(data))
        data2 = ['b'] * 100
        self.assertTrue(str_assertion.test(data2))

    def test_greater_equal_bool(self):
        bool_assertion = AssertionGreaterThanOrEqual(True)
        data = [False] * 100
        self.assertFalse(bool_assertion.test(data))
        data = [True] * 100
        self.assertTrue(bool_assertion.test(data))
        data2 = [False] * 50 + [True] * 50
        self.assertFalse(bool_assertion.test(data2))
        data3 = [False] * 95 + [True] * 5
        self.assertFalse(bool_assertion.test(data3))

    def test_greater_equal_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

            def __ge__(self, other):
                return self.a >= other.a

        obj_assertion = AssertionGreaterThanOrEqual(A(1))
        data = [A(0)] * 100
        self.assertFalse(obj_assertion.test(data))
        data = [A(1)] * 100
        self.assertTrue(obj_assertion.test(data))
        data2 = [A(0), A(1)] * 50
        self.assertFalse(obj_assertion.test(data2))
        data3 = [A(0)] * 95 + [A(1)] * 5
        self.assertFalse(obj_assertion.test(data3))
        data4 = [A(2)] * 95 + [A(0)] * 5
        self.assertTrue(obj_assertion.test(data4))
