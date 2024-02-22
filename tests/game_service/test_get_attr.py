import unittest

from xumes.test_runner.errors.state_conversion_error import StateConversionError
from xumes.test_runner.state_observable import get_object_from_attributes, State


class TestGetattr(unittest.TestCase):

    def test_str(self):
        class A:
            def __init__(self, a):
                self.a = a

        a = A(1)
        self.assertEqual({"__type__": "A", "a": 1}, get_object_from_attributes(a, "a"))

        class A:
            def __init__(self, a):
                self.a = a
                self.b = [1, 2, 3]

        a = A(1)
        self.assertEqual({"__type__": "A", "b": [1, 2, 3]}, get_object_from_attributes(a, "b"))

    def test_list_str(self):
        class A:
            def __init__(self, a):
                self.a = a
                self.b = [1, 2, 3]

        a = A(1)
        self.assertEqual({"a": 1, "b": [1, 2, 3], "__type__": "A"}, get_object_from_attributes(a, ["a", "b"]))

    def test_bool(self):
        self.assertEqual(True, get_object_from_attributes(True))

    def test_int(self):
        self.assertEqual(1, get_object_from_attributes(1))

    def test_float(self):
        self.assertEqual(1.0, get_object_from_attributes(1.0))

    def test_complex(self):
        self.assertEqual(1j, get_object_from_attributes(1j))

    def test_list(self):
        self.assertEqual([1, 2], get_object_from_attributes([1, 2]))
        self.assertEqual([], get_object_from_attributes([]))
        self.assertEqual(["a", "b"], get_object_from_attributes(["a", "b"]))

    def test_tuple(self):
        self.assertEqual((1, 2), get_object_from_attributes((1, 2)))
        self.assertEqual((), get_object_from_attributes(()))
        self.assertEqual(("a", "b"), get_object_from_attributes(("a", "b")))

    def test_range(self):
        self.assertEqual(range(1, 2), get_object_from_attributes(range(1, 2)))
        self.assertEqual(range(1), get_object_from_attributes(range(1)))
        self.assertEqual(range(1, 2, 3), get_object_from_attributes(range(1, 2, 3)))

    def test_bytes(self):
        self.assertEqual(b"a", get_object_from_attributes(b"a"))

    def test_bytes_array(self):
        self.assertEqual(bytearray(b"a"), get_object_from_attributes(bytearray(b"a")))

    def test_memory_view(self):
        self.assertEqual(memoryview(b"a"), get_object_from_attributes(memoryview(b"a")))

    def test_set(self):
        self.assertEqual({1, 2}, get_object_from_attributes({1, 2}))
        self.assertEqual(set(), get_object_from_attributes(set()))

    def test_frozen_set(self):
        self.assertEqual(frozenset({1, 2}), get_object_from_attributes(frozenset({1, 2})))
        self.assertEqual(frozenset(), get_object_from_attributes(frozenset()))

    def test_dict(self):
        self.assertEqual({"a": 1}, get_object_from_attributes({"a": 1}))
        self.assertEqual({}, get_object_from_attributes({}))

    def test_state_attribute_one_attr(self):
        class A:
            def __init__(self, av):
                self.a = av

        state_attribute = State("a")
        a = A(1)
        self.assertEqual({"a": 1, "__type__": "A"}, get_object_from_attributes(a, state_attribute))

    def test_state_attr_not_exist(self):
        class A:
            def __init__(self, av):
                self.a = av

        state_attribute = State("b")
        a = A(1)
        self.assertEqual({"__type__": "A", "b": None}, get_object_from_attributes(a, state_attribute))

    def test_state_attribute_not_exist_in_list_attr(self):
        class A:
            def __init__(self, av):
                self.a = av

        state_attribute = [State("a"), State("b")]
        a = A(1)
        self.assertEqual({"a": 1, "b": None, "__type__": "A"}, get_object_from_attributes(a, state_attribute))

    def test_state_attribute_attr_in_attr(self):
        class A:
            def __init__(self, av):
                self.a = av

        class B:
            def __init__(self, bv):
                self.b = A(bv)

        state_attribute2 = State("b", [
            State("a")
        ])
        b = B(1)

        self.assertEqual({"b": {"a": 1, "__type__": "A"}, "__type__": "B"},
                         get_object_from_attributes(b, state_attribute2))

    def test_state_attribute_attr_with_diff_attr(self):
        class A:
            def __init__(self, av):
                self.a = av

        class B:
            def __init__(self, bv):
                self.b = A(bv)
                self.li = [1, 2]

        state_attribute = [
            State("b", [
                State("a")
            ]),
            State("li")
        ]

        b = B(1)
        self.assertEqual({"b": {"a": 1, "__type__": "A"}, "li": [1, 2], "__type__": "B"},
                         get_object_from_attributes(b, state_attribute))

    def test_state_attribute_attr_with_list_attr(self):
        class A:
            def __init__(self, av):
                self.a = av

        class B:
            def __init__(self):
                self.li = [A(1), A(2)]

        b = B()

        state_attribute = State("li", [
            State("a")
        ])

        self.assertEqual({"li": [{"a": 1, "__type__": "A"}, {"a": 2, "__type__": "A"}], "__type__": "B"},
                         get_object_from_attributes(b, state_attribute))

    def test_state_with_func_on_list1(self):

        class A:
            def __init__(self, av):
                self.a = [av] * av

        def func_raise(a):
            s = 0
            for i in range(len(a)):
                s += a[i]
            return s

        state_attribute = State("a", func=func_raise)

        self.assertEqual({'__type__': 'A', 'a': 4}, get_object_from_attributes(A(2), state_attribute))

    def test_state_with_func_on_list2(self):
        class A:
            def __init__(self, av):
                self.a = [av] * av

        class B:
            def __init__(self):
                self.li = [A(2), A(5)]

        b = B()

        state_attribute = State("li", State("a"))

        self.assertEqual({"li": [{"a": [2] * 2, "__type__": "A"}, {"a": [5] * 5, "__type__": "A"}], "__type__": "B"},
                         get_object_from_attributes(b, state_attribute))

        def sum_li(li):
            s = []
            for i in li:
                s.append(sum(i["a"]))
            return s

        state_attribute2 = State("li", State("a"), func=sum_li)

        self.assertEqual({"li": [4, 25], "__type__": "B"}, get_object_from_attributes(b, state_attribute2))

    def test_state_with_func_on_list3(self):

        li = [1, 2, 3, 4, 5]

        def func_sum(li):
            s = 0
            for i in li:
                s += i
            return s

        state_attribute = State(func=func_sum)

        self.assertEqual(15, get_object_from_attributes(li, state_attribute))

    def test_state_with_func_on_list4_error(self):
        li = [1, 2, 3, 4, 5]

        def func_sum_raise(li):
            s = 0
            for i in range(20):
                s += li[i]
            return s

        state_attribute = State(func=func_sum_raise)
        self.assertEqual(None, get_object_from_attributes(li, state_attribute))

    def test_state_with_func_on_tuple1(self):
        class A:
            def __init__(self, av):
                self.a = (av,) * av

        class B:
            def __init__(self):
                self.li = (A(2), A(5))

        b = B()

        state_attribute = State("li", State("a"))

        self.assertEqual({"li": ({"a": (2,) * 2, "__type__": "A"}, {"a": (5,) * 5, "__type__": "A"}), "__type__": "B"},
                         get_object_from_attributes(b, state_attribute))

        def sum_li(li):
            s = []
            for i in li:
                s.append(sum(i["a"]))
            return s

        state_attribute2 = State("li", State("a"), func=sum_li)

        self.assertEqual({"li": [4, 25], "__type__": "B"}, get_object_from_attributes(b, state_attribute2))

    def test_state_with_func_on_tuple2(self):
        a = (1, 2, 3, 4, 5)

        state_attribute = State(func=lambda x: sum(x))

        self.assertEqual(15, get_object_from_attributes(a, state_attribute))

    def test_state_with_func_on_tuple3_error(self):
        a = (1, 2, 3, 4, 5)

        state_attribute = State(func=lambda x: sum(x) + x[5])

        self.assertEqual(None, get_object_from_attributes(a, state_attribute))

    def test_state_with_func_on_dict1(self):
        class A:
            def __init__(self, av):
                self.a = {"a": av}

        class B:
            def __init__(self):
                self.li = {"a": A(2), "b": A(5)}

        b = B()

        state_attribute = State("li", State("a"))

        self.assertEqual({'__type__': 'B',
                          'li': {'a': {'__type__': 'A', 'a': {'a': 2}},
                                 'b': {'__type__': 'A', 'a': {'a': 5}}}},
                         get_object_from_attributes(b, state_attribute))

        def sum_li(li):
            for k in li:
                li[k] = sum(li[k]["a"].values())
            return li

        state_attribute2 = State("li", State("a"), func=sum_li)

        self.assertEqual({'__type__': 'B', 'li': {'a': 2, 'b': 5}}, get_object_from_attributes(b, state_attribute2))

    def test_state_with_func_on_dict2(self):
        a = {"a": 1, "b": 2, "c": 3}

        state_attribute = State(func=lambda x: sum(x.values()))

        self.assertEqual(6, get_object_from_attributes(a, state_attribute))

    def test_state_with_func_on_dict3_error(self):
        a = {"a": 1, "b": 2, "c": 3}

        def func_error(x):
            return x["d"]

        state_attribute = State(func=func_error)

        self.assertEqual(None, get_object_from_attributes(a, state_attribute))

if __name__ == '__main__':
    unittest.main()
