from unittest import TestCase

from xumes.trainer.entity_manager import EntityObject, AutoEntityManager, choose_delegate, \
    EntityIntAdapter


class TestEntityObject(TestCase):

    def test_get_attr(self):
        s = EntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b.c, 2)

    def test_set_attr(self):
        s = EntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        s.a = 2
        s.b.c = 3
        self.assertEqual(s.a, 2)
        self.assertEqual(s.b.c, 3)

    def test_set_attr2(self):
        s = EntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        s.a = 2
        s.b = 3
        self.assertEqual(s.a, 2)
        self.assertEqual(s.b, 3)

    def test_bool(self):
        s = EntityObject.build({"a": True, "b": {"c": False, "__type__": "Test2"}, "__type__": "Test"})
        self.assertTrue(s.a)
        self.assertFalse(s.b.c)

    def test_int(self):
        s = EntityObject.build({"a": 1, "b": {"c": 2, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b.c, 2)

    def test_float(self):
        s = EntityObject.build({"a": 1.1, "b": {"c": 2.2, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1.1)
        self.assertEqual(s.b.c, 2.2)

    def test_complex(self):
        s = EntityObject.build({"a": 1j, "b": {"c": 2j, "__type__": "Test2"}, "__type__": "Test"})
        self.assertEqual(s.a, 1j)
        self.assertEqual(s.b.c, 2j)

    def test_list(self):
        s = EntityObject.build({"a": 1, "b": [1, 2, 3], "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, [1, 2, 3])

    def test_tuple(self):
        s = EntityObject.build({"a": 1, "b": (1, 2, 3), "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, (1, 2, 3))

    def test_str(self):
        s = EntityObject.build({"a": 1, "b": "abc", "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, "abc")

    def test_set(self):
        s = EntityObject.build({"a": 1, "b": {1, 2, 3}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, {1, 2, 3})

    def test_dict(self):
        s = EntityObject.build({"a": 1, "b": {"a": 1, "b": 2}, "__type__": "Test"})
        self.assertEqual(s.a, 1)
        self.assertEqual(s.b, {"a": 1, "b": 2})

    def test_no_object_int(self):
        s = EntityIntAdapter.build(1)
        self.assertEqual(s, 1)



