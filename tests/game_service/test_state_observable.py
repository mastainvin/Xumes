from unittest import TestCase
from unittest.mock import Mock, patch

from xumes.test_runner.state_observable import StateObservable, State


class TestStateObservable(TestCase):

    @patch.multiple(StateObservable, __abstractmethods__=set())
    def setUp(self) -> None:
        self.observer1 = Mock()
        self.observer2 = Mock()

        self.object = Mock()
        self.obs_name = Mock()
        self.obs = StateObservable(self.object, observers=[self.observer1], name=self.obs_name)
        self.obs2_name = Mock()
        self.obs2 = StateObservable(observable_object=None, observers=[self.observer1], name=self.obs2_name)

        self.obs3_name = Mock()
        self.obs3 = StateObservable(observable_object=self.object, observers=[], name=self.obs3_name)

    def test_attach(self):
        # Normal use
        self.obs.attach(self.observer2)
        self.assertEqual(set(self.obs.observers), {self.observer1, self.observer2})
        self.obs2.attach(self.observer2)
        self.assertEqual(set(self.obs2.observers), {self.observer1, self.observer2})
        # Add two times the same observer
        self.obs2.attach(self.observer2)
        self.assertEqual(set(self.obs2.observers), {self.observer1, self.observer2})
        # Attach a list of observers
        self.obs3.attach([self.observer1, self.observer2])
        self.assertEqual(set(self.obs3.observers), {self.observer1, self.observer2})

    def test_detach(self):
        # Normal use
        self.obs.attach(self.observer2)
        self.obs.detach(self.observer1)
        self.assertEqual(set(self.obs.observers), {self.observer2})
        self.obs2.attach(self.observer2)
        self.obs2.detach(self.observer1)
        self.assertEqual(set(self.obs2.observers), {self.observer2})

        # Detach an observer not attached
        try:
            self.obs3.detach(self.observer1)
        except RuntimeError:
            self.fail("self.obs3.detach(self.observer1) raised Exception unexpectedly!")
        self.assertEqual(set(self.obs3.observers), set())

        # Detach a list
        self.obs3.attach(self.observer1)
        self.obs3.attach(self.observer2)
        self.obs3.detach([self.observer1, self.observer2])
        self.assertEqual(set(self.obs3.observers), set())

    def test_detach_all(self):
        # Normal use
        self.obs.attach(self.observer2)
        self.obs.detach_all()
        self.assertEqual(set(self.obs.observers), set())

        self.obs2.attach(self.observer2)
        self.obs2.detach_all()
        self.assertEqual(set(self.obs2.observers), set())

        # Detach with no observers
        try:
            self.obs3.detach_all()
        except RuntimeError:
            self.fail("self.obs3.detach_all() raised Exception unexpectedly!")
        self.assertEqual(set(self.obs3.observers), set())

    def test_notify(self):
        # Normal use
        self.obs.notify()
        self.observer1.update_state.assert_called_once()

        self.obs2.attach(self.observer2)
        self.obs2.detach(self.observer1)
        self.obs2.notify()
        self.observer2.update_state.assert_called_once()

        # Notify with no observers
        try:
            self.obs3.notify()
        except RuntimeError:
            self.fail("self.obs3.notify() raised Exception unexpectedly!")

    def test_name(self):
        self.assertEqual(self.obs_name, self.obs.name)
        self.assertEqual(self.obs2_name, self.obs2.name)
        self.assertEqual(self.obs3_name, self.obs3.name)

    def test_observers(self):
        self.assertEqual(set(self.obs.observers), {self.observer1})
        self.assertEqual(set(self.obs2.observers), {self.observer1})
        self.assertEqual(set(self.obs3.observers), set())

    def test_object(self):
        self.assertEqual(self.obs.object, self.object)
        self.assertEqual(self.obs2.object, None)
        self.assertEqual(self.obs3.object, self.object)



