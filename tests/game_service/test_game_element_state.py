from unittest import TestCase

from xumes.game_module.game_element_state import GameElementState


class TestObject:

    def __init__(self):
        self.val1 = 1
        self.val2 = "val2"


class TestGameElementState(TestCase):

    def test_state(self):
        obj = TestObject()
        obj2 = TestObject()
        ges = GameElementState(obj)
        self.assertEqual(ges.state, obj)
        self.assertNotEqual(ges.state, obj2)
