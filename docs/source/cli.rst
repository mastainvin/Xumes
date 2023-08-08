CLI
===

Testers
-------

Once you have implemented your `.features` file and your `steps` files, you can start the tester.

To launch the tester, run the following command:

.. code-block:: bash

    $ python -m xumes tester [options]

Options
~~~~~~~

.. option:: --test

   Use this flag to enable the test mode. You need to specify the number of steps and/or the number of iterations to perform.

.. option:: --train

    To use the train mode. The number of steps will be decided by the trainers.

.. option:: --timesteps <steps>, -ts <steps>

   [when testing] The number of steps to perform.

.. option:: --iterations <num>, -i <num>

   [when testing] The number of iterations to perform (Number of games played).

.. option:: --path <folder>

   The path to the folder where the tests are located.

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

.. option:: --ip <ip> [Optional]

   The IP of the training server (default=localhost).

.. option:: --port <ip> [Optional]

   The port of the training server (default=5000).

.. option:: --debug [Optional]

   Enable debug messages display.

.. option:: --info [Optional]

   Enable info messages display.

.. option:: --render [Optional]

   Enable game rendering.

The tester will run the tests and display the results.

Trainers
--------

Once you have implemented your trainers files, you can start the trainer.

To launch the trainer, run the following command:

.. code-block:: bash

    $ python -m xumes trainer [options]

Options
~~~~~~~

.. option:: --train

   Use this flag to enable the train mode. The number of steps will be determined by the trainers inside the python file.

.. option:: --test

   Use this flag to enable the test mode. The number of steps is determined by the tester.

.. option:: --path <folder>

   The path to the folder where the trainers are located.

.. option:: --tensorboard -tb [Optional]

   Save logs to the ``_logs`` folder to be used with TensorBoard.

.. option:: --model [Optional]

   The path to the previously trained model if you want to train from a model.

.. option:: --mode [Optional]

   Mode of training. (scenario=one model per scenario, feature=one model per feature) [default=feature].

.. option:: --debug [Optional]

   Enable debug messages display.

.. option:: --info [Optional]

   Enable info messages display.

.. option:: --port [Optional]

   The port of the training server.

The trainer will run the agents and save the models in the ``models`` folder.
