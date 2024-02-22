from unittest import TestCase

from xumes.test_runner.state_observable import State


class TestState(TestCase):

    def test_create(self):
        state = State("a")
        self.assertEqual("a", state.name)

    def test_create_with_attr_str(self):
        state = State("a", "b")
        self.assertEqual("a", state.name)
        self.assertEqual(State("b"), state.attributes)

    def test_create_with_attr_list(self):
        state = State("a", ["b", "c"])
        self.assertEqual("a", state.name)
        self.assertEqual([State("b"), State("c")], state.attributes)

    def test_create_with_state(self):
        state = State("a", State("b"))
        self.assertEqual("a", state.name)
        self.assertEqual(State("b"), state.attributes)

    def test_not_equal_name(self):
        state = State("a")
        state2 = State("b")
        self.assertNotEqual(state, state2)

    def test_not_equal_attributes(self):
        state = State("a", "b")
        state2 = State("a", "c")
        state3 = State("a", ["b", "c"])
        state4 = State("a", ["b", "d"])
        state5 = State("a", ["b", "c", "d"])
        state6 = State("a")
        self.assertNotEqual(state, state2)
        self.assertNotEqual(state, state3)
        self.assertNotEqual(state3, state4)
        self.assertNotEqual(state3, state5)
        self.assertNotEqual(state, state6)
        self.assertNotEqual(state6, state3)

    def test_not_equal_func(self):
        state = State("a", func=lambda x: x[0])
        state2 = State("a", func=lambda x: len(x))
        self.assertNotEqual(state, state2)

    def test_create_with_func1(self):
        state = State("a", func=lambda x: x[0])
        self.assertEqual("a", state.name)
        self.assertEqual((lambda x: x[0]).__code__.co_code, state.func.__code__.co_code)

    def test_create_with_func2(self):
        state = State("a", "b", func=lambda x: x[0])
        self.assertEqual("a", state.name)
        self.assertEqual(State("b"), state.attributes)
        self.assertEqual((lambda x: x[0]).__code__.co_code, state.func.__code__.co_code)

    def test_create_with_attr_with_func1(self):
        state = State("a", State("b", func=lambda x: x[0]))
        self.assertEqual("a", state.name)
        self.assertEqual("b", state.attributes.name)
        self.assertEqual((lambda x: x[0]).__code__.co_code, state.attributes.func.__code__.co_code)

    def test_create_with_attr_with_func2(self):
        state = State("a", State("b", func=lambda x: sum(x)))
        self.assertEqual("a", state.name)
        self.assertEqual("b", state.attributes.name)
        self.assertEqual((lambda x: sum(x)).__code__.co_code, state.attributes.func.__code__.co_code)

    def test_create_with_attr_with_func3(self):
        state = State("a", State("b", func=lambda x: sum(x)), func=lambda x: x[0])
        self.assertEqual("a", state.name)
        self.assertEqual("b", state.attributes.name)
        self.assertEqual((lambda x: sum(x)).__code__.co_code, state.attributes.func.__code__.co_code)
        self.assertEqual((lambda x: x[0]).__code__.co_code, state.func.__code__.co_code)
