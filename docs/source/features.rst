Feature files
=============

We are using the `Gherkin language <https://cucumber.io/docs/gherkin/reference/>`_ to describe the features.

To get started, create a ``features`` directory in the test directory and write your feature files (``.feature`` files) in the ``features`` directory.

The difference with normal BDD usage is in the sense of the keywords:

- ``Given`` is used to set up the game.
- ``When`` return a `Behavior` object that will be used to test the game.
- ``Then`` is used to make assertions after the agent's play.

Here is an example of a feature file:

.. code-block:: gherkin

    Feature: Flappy Bird Game

        @easy
        Scenario Outline: Testing the pipe size easy
            Given first pipe at <i> and second pipe at <j>
            When bird flies
            Then bird should have passed <k> pipes

            Examples:
                | i   | j   | k |
                | 0   | 0   | 2 |
                | 0.5 | 0.5 | 2 |
                | 1   | 1   | 2 |


.. note:: You can check in the documentation of the `Gherkin language <https://cucumber.io/docs/gherkin/reference/>`_  or in the `behave documentation <https://behave.readthedocs.io/>`_ for more information.