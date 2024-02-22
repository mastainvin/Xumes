import types
from unittest import TestCase
from unittest.mock import Mock

from xumes.test_runner.state_observable import ComposedGameStateObservable, State, InheritedGameStateObservable


class TestGameStateObservable(TestCase):

    # Test for build-in types
    def test_int(self):
        s = ComposedGameStateObservable(1, name="s")
        self.assertEqual(1, s.state().state)

    def test_float(self):
        s = ComposedGameStateObservable(1.0, name="s")
        self.assertEqual(1.0, s.state().state)

    def test_complex(self):
        s = ComposedGameStateObservable(1j, name="s")
        self.assertEqual(1j, s.state().state)

    def test_bool(self):
        s = ComposedGameStateObservable(True, name="s")
        self.assertEqual(True, s.state().state)

    def test_str(self):
        s = ComposedGameStateObservable("a", name="s")
        self.assertEqual("a", s.state().state)

    def test_list(self):
        s = ComposedGameStateObservable([1, 2], name="s")
        self.assertEqual([1, 2], s.state().state)

    def test_tuple(self):
        s = ComposedGameStateObservable((1, 2), name="s")
        self.assertEqual((1, 2), s.state().state)

    def test_dict(self):
        s = ComposedGameStateObservable({"a": 1}, name="s")
        self.assertEqual({"a": 1}, s.state().state)

    def test_set(self):
        s = ComposedGameStateObservable({1, 2}, name="s")
        self.assertEqual({1, 2}, s.state().state)

    def test_frozenset(self):
        s = ComposedGameStateObservable(frozenset({1, 2}), name="s")
        self.assertEqual(frozenset({1, 2}), s.state().state)

    # Test for custom types

    def test_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = ComposedGameStateObservable([A(1), A(2)], name="s", state=["a"])
        self.assertEqual([{"a": 1, "__type__": "A"}, {"a": 2, "__type__": "A"}], s.state().state)

    def test_tuple_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = ComposedGameStateObservable((A(1), A(2)), name="s", state=["a"])
        self.assertEqual(({"a": 1, "__type__": "A"}, {"a": 2, "__type__": "A"}), s.state().state)

    def test_dict_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = ComposedGameStateObservable({"a": A(1), "b": A(2)}, name="s", state=["a"])
        self.assertEqual({"a": {"a": 1, "__type__": "A"}, "b": {"a": 2, "__type__": "A"}}, s.state().state)

    def test_obj_with_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = ComposedGameStateObservable(A([B(1), B(2)]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_dict_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = ComposedGameStateObservable(A({"a": B(1), "b": B(2)}), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({'__type__': 'A',
                          'a': {'a': {'__type__': 'B', 'b': 1}, 'b': {'__type__': 'B', 'b': 2}}},
                         s.state().state)

    def test_obj_with_tuple_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = ComposedGameStateObservable(A((B(1), B(2))), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": ({"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}), "__type__": "A"},
                         s.state().state)

    def test_obj_with_attr_change(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = ComposedGameStateObservable(A(1), name="s", state=State(
            "a",
        ))
        self.assertEqual({"a": 1, "__type__": "A"}, s.state().state)
        s.a = 2
        self.assertEqual({"a": 2, "__type__": "A"}, s.state().state)

    def test_obj_with_attr_change_with_list(self):
        class A:
            def __init__(self, a):
                self.a = a

        s = ComposedGameStateObservable(A([1, 2]), name="s", state=State(
            "a",
        ))
        self.assertEqual({"a": [1, 2], "__type__": "A"}, s.state().state)
        s.a = [3, 4]
        self.assertEqual({"a": [3, 4], "__type__": "A"}, s.state().state)

    def test_obj_with_attr_change_with_list_of_obj(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = ComposedGameStateObservable(A([B(1), B(2)]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)
        s.a = [B(3), B(4)]
        self.assertEqual({"a": [{"b": 3, "__type__": "B"}, {"b": 4, "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_attr_change_with_list_of_obj_with_attr_change(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = ComposedGameStateObservable(A([B(1), B(2)]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": 1, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)
        s.a[0].b = 3
        self.assertEqual({"a": [{"b": 3, "__type__": "B"}, {"b": 2, "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_attr_change_with_list_of_obj_with_attr_change_with_list(self):
        class A:
            def __init__(self, a):
                self.a = a

        class B:
            def __init__(self, b):
                self.b = b

        s = ComposedGameStateObservable(A([B([1, 2]), B([3, 4])]), name="s", state=State(
            "a",
            State("b")
        ))
        self.assertEqual({"a": [{"b": [1, 2], "__type__": "B"}, {"b": [3, 4], "__type__": "B"}], "__type__": "A"},
                         s.state().state)
        s.a[0].b = [5, 6]
        self.assertEqual({"a": [{"b": [5, 6], "__type__": "B"}, {"b": [3, 4], "__type__": "B"}], "__type__": "A"},
                         s.state().state)

    def test_obj_with_list_of_obj_func(self):
        class A:
            def __init__(self, b_list):
                self.b_list = b_list

            def update(self):
                for b in self.b_list:
                    b.update_state()

        class B:
            def __init__(self, b):
                self.b = b

            def update(self):
                self.b += 1

        s = ComposedGameStateObservable(A([B(1), B(2)]), "a", state=State("b_list", State("b", methods_to_observe=["update"]),
                                                                          func=lambda x: [b["b"] for b in x]))
        self.assertEqual({"b_list": [1, 2], "__type__": "A"}, s.state().state)
        s2 = ComposedGameStateObservable(A([B(1), B(2)]), "a",
                                         state=State("b_list", func=lambda x: [b.b for b in x], methods_to_observe=["update"]))
        self.assertEqual({"b_list": [1, 2], "__type__": "A"}, s2.state().state)

    def test_obj_with_list_of_obj_func_inside_func(self):
        class A:
            def __init__(self, b_list):
                self.b_list = b_list

        class B:
            def __init__(self, c_list):
                self.c_list = c_list

        class C:
            def __init__(self, c):
                self.c = c

        s = ComposedGameStateObservable(A([B([C(1), C(2)]), B([C(3)])]), "a",
                                        state=State("b_list", State("c_list", State("c", methods_to_observe=["update"]),
                                                            ),
                                            func=lambda x: [[c["c"] for c in b["c_list"]] for b in x]))
        self.assertEqual({'__type__': 'A', 'b_list': [[1, 2], [3]]}, s.state().state)

        s2 = ComposedGameStateObservable(A([B([C(1), C(2)]), B([C(3)])]), "a",
                                         state=State("b_list", State("c_list", methods_to_observe=["update"],
                                                             func=lambda x: [c.c for c in x]),
                                             func=lambda x: [b["c_list"] for b in x]))
        self.assertEqual({'__type__': 'A', 'b_list': [[1, 2], [3]]}, s2.state().state)

        s3 = ComposedGameStateObservable(A([B([C(1), C(2)]), B([C(3)])]), "a",
                                         state=State("b_list",
                                             func=lambda x: [[c.c for c in b.c_list] for b in x]))
        self.assertEqual({'__type__': 'A', 'b_list': [[1, 2], [3]]}, s3.state().state)

    def test_shortest_state_trivial(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, b):
                self.b = b

        class C:
            def __init__(self, c):
                self.c = c

        a = A(B(1), C(2))

        s = ComposedGameStateObservable(a, name="s", state=[State("b"), State("c")])
        f = s._find_state([State("b")])
        self.assertEqual([State("b")], f)

    def test_shortest_state_same_branch(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("d"), State("e")])
        self.assertEqual([State("b", [State("d"), State("e")])], f)

    def test_shortest_state_same_branch_all_branch(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("b", ["d", "e"])])
        self.assertEqual([State("b", [State("d"), State("e")])], f)

    def test_shortest_state_all_tree(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("b", ["d", "e"]), State("c")])
        self.assertEqual([State("b", ["d", "e"]), State("c")], f)

    def test_shortest_state_one_leef(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("e")])
        self.assertEqual([State("b", ["e"])], f)

    def test_shortest_state_leef_not_deep(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", "e"]), State("c")])
        f = s._find_state([State("c")])
        self.assertEqual([State("c")], f)

    def test_shortest_state_two_branch(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]), State("c")])
        f = s._find_state([State("f")])
        self.assertEqual([State("b", State("e", State("f")))], f)

    def test_shortest_state_two_branch_split_on_second_layer(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]), State("c")])
        f = s._find_state([State("e", State("f"))])
        self.assertEqual([State("b", State("e", State("f")))], f)

    def test_shortest_state_two_branch_limited_search(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]),
                                                            State("c", ["d", State("e", State("f"))])])
        f = s._find_state([State("d")])
        self.assertEqual([State("b", ["d"]), State("c", ["d"])], f)

    def test_shortest_state_results_in_two_nodes(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s", state=[State("b", ["d", State("e", State("f"))]),
                                                            State("c", ["d", State("e", State("f"))])])
        f = s._find_state([State("e", State("f"))])
        self.assertEqual([State("b", State("e", State("f"))), State("c", State("e", State("f")))], f)

    def test_shortest_state_results_in_two_node_different_shapes(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s",
                                        state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        f = s._find_state([State("d")])
        self.assertEqual([State("b", "d"), State("c", State("e", State("d")))], f)

    def test_shortest_state_two_results_not_at_the_same_depth(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s",
                                        state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        f = s._find_state([State("e", State("d"))])
        self.assertEqual([State("c", State("e", State("d")))], f)

    def test_shortest_state_one_result_deep(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s",
                                        state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        f = s._find_state([State("f")])
        self.assertEqual([State("b", State("e", State("f")))], f)

    def test_shortest_state_error(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s",
                                        state=[State("b", ["d", State("e", State("f"))]), State("c", [State("e", State("d"))])])
        self.assertRaises(ValueError, s._find_state, [State("h")])

    def test_shortest_state_error2(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        a = A(1, 2)
        s = ComposedGameStateObservable(a, name="s",
                                        state=None)
        self.assertRaises(ValueError, s._find_state, [State("h")])

    def test_shortest_state_error3(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        a = A(1, 2)
        s = ComposedGameStateObservable(a, name="s",
                                        state=["b", State("c", attributes=None)])

        self.assertRaises(ValueError, s._find_state, [State("h")])

    def test_shortest_state_no_ends(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        a = A(1, 2)
        s = ComposedGameStateObservable(a, name="s",
                                        state=["b", State("c", attributes=None)])

        self.assertEquals(s._state, s._find_state([]))

    def test_game_state_observable_methods_to_observe(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e

        class C:
            def __init__(self, c):
                self.c = c

        class D:
            def __init__(self, d):
                self.d = d

        class E:
            def __init__(self, e):
                self.e = e

        a = A(B(D(1), E(2)), C(3))

        s = ComposedGameStateObservable(a, name="s",
                                        state=[State("b", ["d", State("e", State("f"), methods_to_observe="test2")]), State("c",
                                                                                                                    [
                                                                                                                        State(
                                                                                                                            "e",
                                                                                                                            State(
                                                                                                                                "d",
                                                                                                                                methods_to_observe="test1"),
                                                                                                                            methods_to_observe="test2")])])
        self.assertEqual(
            {"test1": [State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])],
             "test2": [State("b", [State("e", State("f"), methods_to_observe="test2")]),
                       State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])]},
            s._methods_to_observe)

    def test_game_state_observable_methods_to_observe(self):
        class A:
            def __init__(self, b, c):
                self.b = b
                self.c = c
                self.d = 5

        class B:
            def __init__(self, d, e):
                self.d = d
                self.e = e
                self.f = 6

        class C:
            def __init__(self, c):
                self.c = c
                self.d = 7

        class D:
            def __init__(self, d):
                self.d = d
                self.e = 8

        class E:
            def __init__(self, e):
                self.e = e
                self.f = 9

        a = A(B(D(1), E(2)), C(3))
        s = ComposedGameStateObservable(a, name="s",
                                        state=[State("b", ["d", State("e", State("f"), methods_to_observe="test2")]), State("c",
                                                                                                                    [
                                                                                                                        State(
                                                                                                                            "e",
                                                                                                                            State(
                                                                                                                                "d",
                                                                                                                                methods_to_observe="test1"),
                                                                                                                            methods_to_observe="test2")])])
        self.assertEqual(
            {"test1": [State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])],
             "test2": [State("b", [State("e", State("f"), methods_to_observe="test2")]),
                       State("c", [State("e", State("d", methods_to_observe="test1"), methods_to_observe="test2")])]},
            s._methods_to_observe)
