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

   Tags to filter the scenarios. See the `Tags Expression` section for more information.

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

   Tags to filter the scenarios. See the `Tags Expression` section for more information.

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

   Tags to filter the scenarios. See the `Tags Expression` section for more information.

.. option:: --fps <value> [Optional]

   Limit of FPS.

.. option:: --headless [Optional]

   Run the game in headless mode.

.. option:: --tensorboard, -tb [Optional]

   Save logs to the ``logs`` folder to be used with TensorBoard.

.. option:: --imitate

   Imitate the expert.

Collect
-------

This command collects the data from the game.

Synopsis
~~~~~~~~

.. code-block:: bash

    xumes collect [OPTIONS]

Options
~~~~~~~

.. option:: --clean [Optional]

   Clean the data before collecting. If not specified, the data will be appended.

.. option:: --iterations <num>, -i <num>

   [when collecting] The number of iterations to perform (Number of games played).

.. option:: --features <name>, -f <name> [Optional]

   List of features you want to collect, separated by commas. All if not specified.

.. option:: --scenarios <name>, -s <name> [Optional]

   List of scenarios you want to collect, separated by commas. All if not specified.

.. option:: --tags <name> [Optional]

   Tags to filter the scenarios. See the `Tags Expression` section for more information.

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

.. option:: --h <value> [Optional]

   Limit of FPS and headless mode.




List
----

This command lists all the features of the test.

Synopsis
~~~~~~~~

.. code-block:: bash

    xumes list [OPTIONS]

Options
~~~~~~~

.. option:: --features_path <folder> [Optional]

   The path to the folder where the features are located.

.. option:: --steps_path <folder> [Optional]

   The path to the folder where the steps are located.

.. option:: --features <name>, -f <name> [Optional]

   List of features you want to list, separated by commas. All if not specified.

.. option:: --scenarios <name>, -s <name> [Optional]

   List of scenarios you want to list, separated by commas. All if not specified.

.. option:: --tags <name> [Optional]

   Tags to filter the scenarios. See the `Tags Expression` section for more information.

Description
~~~~~~~~~~~

The ``list`` command is used to list all the features of the test. It takes several optional parameters including ``features``, ``scenarios``, and ``tags``. The ``features``, ``scenarios``, and ``tags`` parameters are used to specify which features and scenarios to list and to tag the features. The ``features_path`` and ``steps_path`` parameters are used to specify the paths to the features and steps folders.

Examples
~~~~~~~~

.. code-block:: bash

    xumes list --features_path ./features --steps_path ./steps --features feature1,feature2 --scenarios scenario1,scenario2 --tags 'tag1 and tag2'

This command will list all the features specified in the ``features`` and ``scenarios`` options that are tagged with the tags specified in the ``tags`` option. The features and scenarios are located in the folders specified by the ``features_path`` and ``steps_path`` options.


.. code-block:: bash

    +------------------------------------------------------+--------------+-------------+
    | Feature/Scenario                                     | Steps file   | Tags        |
    +======================================================+==============+=============+
    | Feature: PipeSize2                                   |              |             |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size easy [0] - (i=0, j=0, k=2)     | PipeSize.py  | easy, smoke |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size easy [1] - (i=0.5, j=0.5, k=2) | PipeSize.py  | easy, smoke |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size easy [2] - (i=1, j=1, k=2)     | PipeSize.py  | easy, smoke |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size hard [0] - (i=0, j=1, k=2)     | PipeSize.py  | hard        |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size hard [1] - (i=1, j=0, k=2)     | PipeSize.py  | hard        |
    +------------------------------------------------------+--------------+-------------+
    | Feature: PipeSize                                    |              |             |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size easy [0] - (i=0, j=0, k=2)     | PipeSize.py  | easy, smoke |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size easy [1] - (i=0.5, j=0.5, k=2) | PipeSize.py  | easy, smoke |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size easy [2] - (i=1, j=1, k=2)     | PipeSize.py  | easy, smoke |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size hard [0] - (i=0, j=1, k=2)     | PipeSize.py  | hard        |
    +------------------------------------------------------+--------------+-------------+
    | Testing the pipe size hard [1] - (i=1, j=0, k=2)     | PipeSize.py  | hard        |
    +------------------------------------------------------+--------------+-------------+


Tags Expression
----------------

This feature allows you to filter scenarios based on tags expressions. The `--tags` parameter supports boolean logic expressions with `and`, `or`, and `not` operators, as well as wildcard matching.

Syntax
~~~~~~

- `tag1 and tag2`: Select scenarios that have both `tag1` and `tag2`.
- `tag1 or tag2`: Select scenarios that have either `tag1` or `tag2`.
- `not tag1`: Select scenarios that do not have `tag1`.
- `tag1 and (tag2 or tag3)`: Select scenarios that have `tag1` and either `tag2` or `tag3`.
- `not (tag1 or tag2)`: Select scenarios that do not have `tag1` or `tag2`.

Wildcards
~~~~~~~~~

- `tag.*`: Select scenarios with tags that start with `tag`.
- `.*tag`: Select scenarios with tags that end with `tag`.
- `*tag*`: Select scenarios with tags that contain `tag`.

Examples
~~~~~~~~

.. code-block:: bash

    xumes list --tags "easy and not smoke"