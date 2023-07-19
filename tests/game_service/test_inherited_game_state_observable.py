from typing import List
from unittest import TestCase
from unittest.mock import Mock, MagicMock

from xumes.game_module import State
from xumes.game_module.test_runner import TestRunner


class TestInheritedGameStateObservable(TestCase):

    def setUp(self):
        observer = Mock()

        class ConcreteTestRunner(TestRunner):
            def run_test(self) -> None:
                pass

            def run_test_render(self) -> None:
                pass

            def random_reset(self) -> None:
                pass

            def reset(self) -> None:
                pass

            def delete_screen(self) -> None:
                pass

        self.test_runner = ConcreteTestRunner(observer=observer)

    def tearDown(self):
        del self.test_runner

    def test_create(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a", methods_to_observe=["update"]))
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 4)
        self.assertEqual(a.a, 1)

    def test_create_with_args(self):
        class A:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a"), 0)
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_with_kwargs(self):
        class A:

            def __init__(self, a=0, b=0):
                self.a = a
                self.b = b

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a"), a=0, b=0)
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create1(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        a = self.test_runner.create(A, "a", State("a", methods_to_observe=["update"]))
        a.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 4)
        self.assertEqual(a.a, 1)

    def test_create_obj_in_obj(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        class B:

            def __init__(self):
                self.a = A()

            def update_a(self):
                self.a.update_a()

        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]))
        b.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)
        self.assertEqual(b.a.a, 1)

    def test_create_list_of_obj_in_obj(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        class B:

            def __init__(self):
                self.a = [A(), A()]

            def update_a(self):
                for a in self.a:
                    a.update_a()

        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]))
        b.update_a()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)
        self.assertEqual(b.a[0].a, 1)

    def test_create_list_of_obj_in_obj_with_list_of_methods(self):
        class A:

            def __init__(self):
                self.a = 0

            def update_a(self):
                self.update()

            def update(self):
                self.a += 1

        class B:

            def __init__(self):
                self.a = [A(), A()]

            def update(self):
                self.update_a()

            def update_a(self):
                for a in self.a:
                    a.update_a()

        b = self.test_runner.create(B, "b", State("a", State("a", methods_to_observe=["update_a"])))
        b.update()
        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)
        self.assertEqual(b.a[0].a, 1)

    def test_create_two_observable(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update_a(self):
                self.update()

            def update(self):
                self.value += 1

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("value", methods_to_observe=["update"]), value=0)
        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]), a=a)

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 7)

    def test_create_two_observable_no_methods(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update_a(self):
                self.update()

            def update(self):
                self.value += 1

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("value"), value=0)
        b = self.test_runner.create(B, "b", State("a"), a=a)

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 5)

    def test_create_observable_with_list_of_observable(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update_a(self):
                self.update()

            def update(self):
                self.value += 1

        class B:

            def __init__(self, a_list):
                self.a_list = a_list

            def update_a(self):
                for a in self.a_list:
                    a.update()

        a = self.test_runner.create(A, "a", State("value", methods_to_observe=["update"]), value=0)
        b = self.test_runner.create(B, "b", State("a_list", methods_to_observe=["update_a"]), a_list=[a, a])

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 9)

    def test_create_two_observable_each_contain_each_other(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update_a(self):
                self.update()

            def update(self):
                pass

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("b", methods_to_observe=["update"]), b=0)
        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]), a=a)
        a.b = b

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 7)

    def test_create_two_observable_each_contain_each_other_no_methods(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update_a(self):
                self.update()

            def update(self):
                pass

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update()

        a = self.test_runner.create(A, "a", State("b"), b=0)
        b = self.test_runner.create(B, "b", State("a"), a=a)
        a.b = b

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 5)

    def test_create_two_observable_each_contain_each_other_with_list_of_methods(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update_a(self):
                self.update()

            def update(self):
                pass

        class B:

            def __init__(self, a):
                self.a = a

            def update_a(self):
                self.a.update_a()

        a = self.test_runner.create(A, "a", State("b", methods_to_observe=["update", "update_a"]), b=0)
        b = self.test_runner.create(B, "b", State("a", methods_to_observe=["update_a"]), a=a)
        a.b = b

        b.update_a()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 8)

    def test_create_observable_with_a_deep_call_tree(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update(self):
                self.b.update()

        class B:

            def __init__(self, c):
                self.c = c

            def update_c(self):
                self.c.update()

            def update(self):
                self.update_c()

        class C:

            def __init__(self, d):
                self.d = d

            def update_d(self):
                self.d.update()

            def update(self):
                self.update_d()

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        d = self.test_runner.create(D, "d", State("v"), v=1)
        a = A(B(C(d)))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_observable_with_a_deep_state_tree(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update(self):
                self.b.update()

        class B:

            def __init__(self, c):
                self.c = c

            def update_c(self):
                self.c.update()

            def update(self):
                self.update_c()

        class C:

            def __init__(self, d):
                self.d = d

            def update_d(self):
                self.d.update()

            def update(self):
                self.update_d()

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        a = self.test_runner.create(A, "a", State("b", State("c", State("d", methods_to_observe="update"))),
                                    b=B(c=C(d=D(1))))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_observable_with_a_deep_state_tree2(self):
        class A:

            def __init__(self, b):
                self.b = b

            def update(self):
                self.b.update()

        class B:

            def __init__(self, c):
                self.c = c

            def update_c(self):
                self.c.update()

            def update(self):
                self.update_c()

        class C:

            def __init__(self, d):
                self.d = d

            def update_d(self):
                self.d.update()

            def update(self):
                self.update_d()

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        a = self.test_runner.create(A, "a", State("b", State("c", State("d", State("v", methods_to_observe="update")))),
                                    b=B(c=C(d=D(1))))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_observable_with_a_large_state_tree(self):
        class A:

            def __init__(self, b, c, d):
                self.b = b
                self.c = c
                self.d = d

            def update(self):
                self.b.update()
                self.c.update()
                self.d.update()

        class B:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class C:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        a = self.test_runner.create(A, "a", [State("b"), State("c"), State("d")], b=B(1), c=C(1), d=D(1))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 4)

    def test_create_observable_with_a_large_state_tree_with_method(self):
        class A:

            def __init__(self, b, c, d):
                self.b = b
                self.c = c
                self.d = d

            def update(self):
                self.b.update()
                self.c.update()
                self.d.update()

        class B:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class C:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        a = self.test_runner.create(A, "a",
                                    [State("b", methods_to_observe="update"), State("c", methods_to_observe="update"),
                                     State("d", methods_to_observe="update")], b=B(1),
                                    c=C(1), d=D(1))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 5)

    def test_create_observable_with_a_large_state_tree_with_method2(self):
        class A:

            def __init__(self, b, c, d):
                self.b = b
                self.c = c
                self.d = d

            def update(self):
                self.b.update()
                self.c.update()
                self.d.update()

        class B:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class C:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        a = self.test_runner.create(A, "a", [State("b"), State("c"), State("d", methods_to_observe="update")], b=B(1),
                                    c=C(1), d=D(1))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 5)

    def test_create_observable_with_a_large_state_tree_with_method3(self):
        class A:

            def __init__(self, b, c, d):
                self.b = b
                self.c = c
                self.d = d

            def update(self):
                self.update_b()
                self.update_c()
                self.update_d()

            def update_b(self):
                self.b.update()

            def update_c(self):
                self.c.update()

            def update_d(self):
                self.d.update()

        class B:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class C:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        class D:

            def __init__(self, v):
                self.v = v

            def update(self):
                self.v += 1

        a = self.test_runner.create(A, "a", [State("b", methods_to_observe="update_b"),
                                             State("c", methods_to_observe="update_c"),
                                             State("d", methods_to_observe="update_d")], b=B(1),
                                    c=C(1), d=D(1))
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 7)

    def test_create_an_observable_with_conflicts_get_and_set_attr(self):
        class A:

            def __init__(self, value):
                self.value = value

            def update(self):
                self.value += 1

            def __getattr__(self, item):
                return getattr(self.value, item)

            def __setattr__(self, key, value):
                if key == "value":
                    self.__dict__[key] = value
                else:
                    setattr(self.value, key, value)

            def __getattribute__(self, item):
                if item == "value":
                    return self.__dict__[item]
                else:
                    return getattr(self.value, item)

        a = self.test_runner.create(A, "a", [State("value")], value=1)
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_an_observable_with_conflicts_slots_(self):
        class A:
            __slots__ = ["value"]

            def __init__(self, value):
                self.value = value

            def update(self):
                self.value += 1

        a = self.test_runner.create(A, "a", [State("value")], value=1)
        a.update()

        self.assertEqual(self.test_runner._observer.update_state.call_count, 3)

    def test_create_an_observable_list(self):

        li = self.test_runner.create(list, "li", [State("items", methods_to_observe="append")], [1, 2, 3])

        li.append(4)

        self.assertEqual(self.test_runner._observer.update_state.call_count, 2)

    def test_create_an_observable_list2(self):

        li = self.test_runner.create(list, "li", [State("items", methods_to_observe="__setitem__")], [1, 2, 3])

        li.__setitem__(0, 4)

        self.assertEqual(self.test_runner._observer.update_state.call_count, 2)

    def test_create_an_observable_list3(self):

        li = self.test_runner.create(list, "li", [State("items", methods_to_observe="__setitem__")], [1, 2, 3])

        li[0] = 4

        self.assertEqual(self.test_runner._observer.update_state.call_count, 1)

    def test_create_observable_setitem(self):

        class A:
            def __init__(self, value):
                self.value = value

            def __setitem__(self, key, value):
                self.value[key] = value

        a = self.test_runner.create(A, "a", [State("value", methods_to_observe="__setitem__")], value={})
        a["key"] = 1

        self.assertEqual(self.test_runner._observer.update_state.call_count, 2)

    def test_create_an_observable_dict(self):

        d = self.test_runner.create(dict, "obj", [State("items", methods_to_observe="__setitem__")], {"value": 1})

        d.__setitem__("value", 2)

        self.assertEqual(self.test_runner._observer.update_state.call_count, 2)
