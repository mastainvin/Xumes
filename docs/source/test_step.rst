TestStep
========

The `TestStep` class is an abstract base class that provides an abstraction layer for interacting with the game instance. Each step must implement specific methods to define its actions, determine whether it is complete, and reset its state.

.. autoclass:: xumes.TestStep
    :members: step, is_complete, reset

Default implementations
-----------------------

Xumes provides default implementations of `TestStep`.

.. autoclass:: xumes.SequentialStep

.. autoclass:: xumes.DelayStep

.. autoclass:: xumes.CombinedStep

.. autoclass:: xumes.WaitStep

.. autoclass:: xumes.WaitUntilStep

.. autoclass:: xumes.RepeatStep

.. autoclass:: xumes.RepeatUntilStep

.. autoclass:: xumes.LogStep
