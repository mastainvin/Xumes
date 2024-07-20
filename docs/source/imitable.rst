
Imitable Interface
==================

`Agent` can implement the `Imitable` interface to allow to use an imitation learning algorithm to learn from human expert demonstrations.

The `Imitable` interface has the following method:

- `imitate(self) -> Imitator`

Imitator Class
--------------

You have to create an Imitator and define the following method:

- `convert_action(self, input: keys) -> np.ndarray` : Convert the input keys to an action.

The input keys are the keys pressed by the human expert. We use the pygame key constants to represent the keys.

Example
~~~~~~~


.. code:: python

    class FlyImitator(Imitator):

        def convert_input(self, keys) -> np.ndarray:
            if keys[pygame.K_SPACE]:
                return np.array([1])
            return np.array([0])


You then can use the `Imitator` in your agent by implementing the `imitate` method.

.. code:: python

    class FlyAgent(Agent, Imitable):

        def imitate(self) -> Imitator:
            return FlyImitator(algorithm=BC(20),
                               threshold=2,
                               collected_data_path="./Tests/PipeSizeTest/models/fly")


Collecting Data
---------------

You can use the following command to start collecting data:

.. code:: bash

   python -m xumes collect <features_path> -i <number_of_examples_per_scenario>

Then a window will open and you can start playing the game.

- You can pause the game by pressing "esc" and resume by pressing "esc" again.
- After each episode, you can validate the episode by pressing "return" to save the episode or "backspace" to discard it.

.. important::

    Focus on the pygame window to capture the keys pressed. (not the game window)


Training
--------

After the data collection, you can train the model using the 'train' command with '--imitate' flag.

.. code:: bash

   python -m xumes train <features_path> --imitate -h 10

After the training, you can use the trained model to train the agent.