Xumes
=====

Xumes is a game testing tool designed to be used on top of games without the need to modify the game sources. It provides a framework for observing and interacting with game elements, training models, and conducting tests. For the moment, only the Godot framework has an implemented module for interacting with Xumes. So for the moment, the documentation will be focused on the implementation with Godot.

Please check the `documentation <https://xumes.readthedocs.io/en/latest/>`_ for more information.

Framework
---------

The framework is based on the BDD methodology, that means that two types of files are needed to conduct tests. Those files are the `feature` files and the `steps` files.

The following diagram illustrates the architecture of the framework:

.. image:: ./docs/source/_static/architecture.png
   :alt: framework schema

Installation
------------

.. code-block:: bash

    pip install xumes

Using with Godot
----------------

To use Xumes with Godot, you need to compile Godot from sources. Follow the instructions in the `Godot documentation <https://docs.godotengine.org/en/stable/development/compiling/index.html>`_.

Clone the following repository instead of the official one:

.. code-block:: bash

    git clone https://github.com/mastainvin/godot.git

.. note::

    Don't forget to checkout to the `xumes` branch before building `Godot`.

To start the `Godot` editor, run the following command:

.. code-block:: bash

    ./bin/godot.x11.tools.64 --editor --path <path_to_godot_project>

Quick start
-----------

Once `Xumes` and `Godot` are installed, you can test your installation with the Flappy Bird example. First, clone the repository:

.. code-block:: bash

    git clone https://github.com/mastainvin/Xumes-Examples.git

Then, navigate to the `FlappyBird` directory:

.. code-block:: bash

    cd Xumes-Examples/Godot/flappy_bird/

Run the tests with the following command:

.. code-block:: bash

    python -m xumes test ./Tests/PipeSizeTest/features -h 10 -i 100

.. warning::

    Always use `python -m xumes` to run the tests. This ensures the use of `Xumes` as a module and the ability to import other modules in the project.

This command will run the tests found in the `features` directory in headless mode (without rendering the game), with a frame rate limit of 10 FPS and 100 iterations.

You should see the following output:

.. code-block:: text

                   TEST REPORT

    9 tests passed on a total of 9 in 00:01:16.
    Tests passed:
        - PipeSize/Testing the pipe size [2] - (i=0.5, j=1, k=2)
        - PipeSize/Testing the pipe size easy [1] - (i=0.5, j=0.5, k=2)
        - PipeSize/Testing the pipe size easy [2] - (i=1, j=1, k=2)
        - PipeSize/Testing the pipe size hard [1] - (i=1, j=0, k=2)
        - PipeSize/Testing the pipe size [1] - (i=0.5, j=0, k=2)
        - PipeSize/Testing the pipe size easy [0] - (i=0, j=0, k=2)
        - PipeSize/Testing the pipe size hard [0] - (i=0, j=1, k=2)
        - PipeSize/Testing the pipe size [0] - (i=0, j=0.5, k=2)
        - PipeSize/Testing the pipe size [3] - (i=1, j=0.5, k=2)

`Here <https://www.youtube.com/watch?v=awXkgS3Pc8s>`_ is the video of Godot first build and test execution.
