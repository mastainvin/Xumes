from unittest import TestCase

from xumes.training_module.entity_manager import EntityBoolAdapter, EntityIntAdapter, EntityFloatAdapter, \
    EntityComplexAdapter, EntityStrAdapter, \
    EntityListAdapter, EntityTupleAdapter, EntitySetAdapter, EntityDictAdapter, EntityObject


class TestEntity(TestCase):
    def test_bool(self):
        b = EntityBoolAdapter(True)
        c = EntityBoolAdapter(False)
        self.assertTrue(b)
        self.assertFalse(c)
        b = b.update_state(False)
        c = c.update_state(True)
        self.assertFalse(b)
        self.assertTrue(c)

    def test_int(self):
        a = EntityIntAdapter(1)
        a = a.update_state(2)
        a += 1
        self.assertEqual(a, 3)

    def test_float(self):
        a = EntityFloatAdapter(1.0)
        a = a.update_state(2.0)
        a += 1.0
        self.assertEqual(a, 3.0)

    def test_complex(self):
        a = EntityComplexAdapter(1 + 1j)
        a = a.update_state(2 + 2j)
        a += 1+1j
        self.assertEqual(a, 3+3j)

    def test_str(self):
        a = EntityStrAdapter("a")
        a = a.update_state("b")
        a += "c"
        self.assertEqual(a, "bc")

    def test_list(self):
        li = EntityListAdapter([1, 2, 3])
        li.append(4)
        self.assertEqual([1, 2, 3, 4], li)
        li = li.update_state([1, 2, 3, 4, 5])
        self.assertEqual([1, 2, 3, 4, 5], li)

    def test_tuple(self):
        t = EntityTupleAdapter((1, 2, 3))
        t = t.update_state((1, 2, 3, 4))
        self.assertEqual((1, 2, 3, 4), t)

    def test_set(self):
        s = EntitySetAdapter({1, 2, 3})
        s = s.update_state({1, 2, 3, 4})
        self.assertEqual({1, 2, 3, 4}, s)

    def test_dict(self):
        d = EntityDictAdapter({1: 1, 2: 2, 3: 3})
        d = d.update_state({1: 1, 2: 2, 3: 3, 4: 4})
        self.assertEqual({1: 1, 2: 2, 3: 3, 4: 4}, d)

    def test_list_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        li = EntityListAdapter([o])
        li = li.update_state([o, o])
        self.assertEqual([o, o], li)

    def test_tuple_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        t = EntityTupleAdapter((0,))
        t = t.update_state((o, o))
        self.assertEqual((o, o), t)

    def test_set_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        o2 = EntityObject({"a": 2, "__type__": "Test"})
        s = EntitySetAdapter({o})
        s = s.update_state({o, o2})
        self.assertEqual({o, o2}, s)
        self.assertNotEqual({o}, s)

    def test_dict_object(self):
        o = EntityObject({"a": 1, "__type__": "Test"})
        o2 = EntityObject({"a": 2, "__type__": "Test"})
        d = EntityDictAdapter({1: o})
        d = d.update_state({1: o, 2: o2})
        self.assertEqual({1: o, 2: o2}, d)
        self.assertNotEqual({1: o}, d)