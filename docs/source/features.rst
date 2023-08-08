Feature files
=============

We are using the `Gherkin language <https://cucumber.io/docs/gherkin/reference/>`_ to describe the features.

To get started, create a ``features`` directory in the test directory and write your feature files (``.feature`` files) in the ``features`` directory.

The difference with normal BDD usage is in the sense of the keywords:

- ``Given`` is used to set up the game.
- ``When`` is used to set up the testing situation.
- ``Then`` is used to make assertions after the agent's play.

Here is an example of a feature file:

.. code-block:: gherkin

   Feature: Testing the jump

     Scenario: Top and bottom
       Given A game with a player
       And A pipe generator
       When The first pipe is at 50 % and the next pipe is at 100 %
       Then The player should have passed 2 pipes
       And The player should have passed at least 1 pipe

     Scenario: Bottom and top
       Given A game with a player
       And A pipe generator
       When The first pipe is at 100 % and the next pipe is at 50 %
       Then The player should have passed 2 pipes
       And The player should have passed at least 1 pipe


.. important:: As you can see, the ``And`` keyword is used to chain the steps, which means it has the same function as the keyword just before it.
