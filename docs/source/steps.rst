Steps files
===========

The steps files are responsible for implementing the tests that will be
executed by the framework. They are written in Gherkin, a language that
allows you to write tests in a human-readable format. The framework will
execute these tests by interacting with the game.


Example of a steps file:

.. code:: python

    @config
    def config(context):
        context.driver.set_scene("res://Tests/PipeSizeTest/PipeSizeTest.tscn")


    @given("first pipe at {i:f} and second pipe at {j:f}")
    def step_impl(context, i, j):
        context.driver.set_pipes_position(i, j)


    @when("bird flies")
    def step_impl(context):
        return Fly()


    @then("bird should have passed {i:d} pipes")
    def step_impl(context, i):
        context.assert_true(context.score >= i)



Each step file while require to implement the following methods using
python decorators:


.. method:: @config

   :type: Method
   :description: This method will be executed before the tests. It will set up the game instance.

.. important::

    In `Godot` you have to call the method `set_scene` and pass the path to the scene you want to test.

.. method:: @given(step_description)

   :param str step_description: The description of the given step.
   :type: Method
   :description: This method will be executed before each test. It is responsible for setting up the game state before the test starts.

.. method:: @when(step_description)

   :param str step_description: The description of the when step.
   :type: Method
   :description: The method will be executed before every test. It return a `Behavior` object that will make the actions in the game.

.. method:: @then(step_description)

   :param str step_description: The description of the then step.
   :type: Method
   :description: This method will be executed after the game loop. It is responsible for asserting the expected game state after the test is finished.


.. note:: The ``given``, ``when`` and ``then`` decorators can handle
   arguments.


Get the game state
------------------


The game state is represented by the ``test_context`` object. This object is include as the first argument of the methods decorated by ``given``, ``when`` and ``then``.
For instance, if you want to get the player health, you can do it like this:

.. code:: python

   player_health = test_context.player.health



Call game methods (in `@config` and `@given`)
---------------------------------------------

You can call game methods in the `@config` and `@given` methods. For instance, if you want to set the player health to 100, you can do it like this:

.. code:: python

   test_context.set_player_health(100)


.. note::

    In `Godot` those methods need to be exposed in the script of the `FeatureNode` root.



Assertions
----------

The ``@then`` decorator is used to define the conditions under which a
test is successful. As you can see on the schema, it will be executed
every time a game is terminated. You have a list of ``assertion``
functions that you can use to define your conditions.

.. code:: python

   @then("The player killed the monster")
   def test_impl(test_context):
       test_context.assert_true(test_context.monster.is_dead)

Assertion functions
~~~~~~~~~~~~~~~~~~~

.. method:: assert_true(condition)

   :param condition: The condition to assert.
   :description: Asserts that ``condition`` is ``True``.

.. method:: assert_false(condition)

   :param condition: The condition to assert.
   :description: Asserts that ``condition`` is ``False``.

.. method:: assert_equal(actual, expected)

   :param actual: The actual value.
   :param expected: The expected value.
   :description: Asserts that ``actual`` is equal to ``expected``.

.. method:: assert_not_equal(actual, expected)

   :param actual: The actual value.
   :param expected: The expected value.
   :description: Asserts that ``actual`` is not equal to ``expected``.

.. method:: assert_greater(actual, expected)

   :param actual: The actual value.
   :param expected: The expected value.
   :description: Asserts that ``actual`` is greater than ``expected``.

.. method:: assert_greater_equal(actual, expected)

   :param actual: The actual value.
   :param expected: The expected value.
   :description: Asserts that ``actual`` is greater than or equal to ``expected``.

.. method:: assert_less(actual, expected)

   :param actual: The actual value.
   :param expected: The expected value.
   :description: Asserts that ``actual`` is less than ``expected``.

.. method:: assert_less_equal(actual, expected)

   :param actual: The actual value.
   :param expected: The expected value.
   :description: Asserts that ``actual`` is less than or equal to ``expected``.

.. method:: assert_between(actual, min, max)

    :param actual: The actual value.
    :param min: The minimum value.
    :param max: The maximum value.
    :description: Asserts that ``actual`` is between ``min`` and ``max``.

.. method:: assert_not_between(actual, min, max)

    :param actual: The actual value.
    :param min: The minimum value.
    :param max: The maximum value.
    :description: Asserts that ``actual`` is not between ``min`` and ``max``.


Example:

.. code:: python

   test_context.assert_false(test_context.monster.is_dead)
   test_context.assert_not_between(test_context.player.health, 0, 100)