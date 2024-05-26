CLI
===

Play Mode
---------

This mode allows a human to manually test the game.

To launch the play mode, run the following command:

.. code-block:: bash

    xumes play [options]

Options
~~~~~~~

.. option:: --iterations <num>, -i <num>

   [when playing] The number of iterations to perform (Number of games played).

.. option:: --features <name>, -f <name> [Optional]

   List of features you want to play, separated by commas. All if not specified.

.. option:: --scenarios <name>, -s <name> [Optional]

   List of scenarios you want to play, separated by commas. All if not specified.

.. option:: --tags <name> [Optional]

   List of tags you want to play, separated by commas. All if not specified.

.. option:: --log

   Enable logging of the results.

.. option:: --debug [Optional]

   Enable debug messages display.

.. option:: --info [Optional]

   Enable info messages display.

.. option:: --features_path <folder> [Optional]

   The path to the folder where the features are located.

.. option:: --steps_path <folder> [Optional]

   The path to the folder where the steps are located.

Test Mode
---------

This mode allows you to automatically test the game.

To launch the test mode, run the following command:

.. code-block:: bash

    xumes test [options]

Options
~~~~~~~

.. option:: --vectorize, -v

   Vectorize the testing.

.. option:: --iterations <num>, -i <num>

   [when testing] The number of iterations to perform (Number of games played).

.. option:: --features <name>, -f <name> [Optional]

   List of features you want to test, separated by commas. All if not specified.

.. option:: --scenarios <name>, -s <name> [Optional]

   List of scenarios you want to test, separated by commas. All if not specified.

.. option:: --tags <name> [Optional]

   List of tags you want to test, separated by commas. All if not specified.

.. option:: --alpha <value>, -a <value>

   [when testing] The alpha value for the Student t-test.

.. option:: --log

   Enable logging of the results.

.. option:: --debug [Optional]

   Enable debug messages display.

.. option:: --info [Optional]

   Enable info messages display.

.. option:: --features_path <folder> [Optional]

   The path to the folder where the features are located.

.. option:: --steps_path <folder> [Optional]

   The path to the folder where the steps are located.

.. option:: --fps <value> [Optional]

   Limit of FPS.

.. option:: --headless [Optional]

   Run the game in headless mode.

.. option:: --render [Optional]

   Enable game rendering.

Train Mode
----------

This mode allows you to train an agent.

To launch the train mode, run the following command:

.. code-block:: bash

    xumes train [options]

Options
~~~~~~~

.. option:: --tensorboard, -tb [Optional]

   Save logs to the ``_logs`` folder to be used with TensorBoard.

.. option:: --vectorize, -v

   Vectorize the training.

.. option:: --debug [Optional]

   Enable debug messages display.

.. option:: --info [Optional]

   Enable info messages display.

.. option:: --features_path <folder> [Optional]

   The path to the folder where the features are located.

.. option:: --steps_path <folder> [Optional]

   The path to the folder where the steps are located.

.. option:: --model <path> [Optional]

   The path to the previously trained model if you want to train from a model.

.. option:: --features <name>, -f <name> [Optional]

   List of features you want to train, separated by commas. All if not specified.

.. option:: --scenarios <name>, -s <name> [Optional]

   List of scenarios you want to train, separated by commas. All if not specified.

.. option:: --tags <name> [Optional]

   List of tags you want to train, separated by commas. All if not specified.

.. option:: --fps <value> [Optional]

   Limit of FPS.

.. option:: --headless [Optional]

   Run the game in headless mode.
