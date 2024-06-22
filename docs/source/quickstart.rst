Quickstart
==========

Once `Xumes` and `Godot` are installed, you can test your installation with the Flappy Bird example. First, clone the repository:

.. code-block:: bash

    git clone https://github.com/mastainvin/Xumes-Examples.git

Then, navigate to the `FlappyBird` directory:

.. code-block:: bash

    cd Xumes-Examples/Godot/flappy_bird/

Run the tests with the following command:

.. code-block:: bash

    python -m xumes test --features_path=./Tests/PipeSizeTest/features --steps_path=./Tests/PipeSizeTest/features/steps -h 10 -i 100 -v

.. warning::

    Always use `python -m xumes` to run the tests. This ensures the use `Xumes` as a module and be able to import other modules in the project.

This command will run the tests found in the `features` directory in headless mode (without rendering the game), with a frame rate limit of 10 FPS and 100 iterations. The `-v` flag enables vectorized mode.

You should see the following output:

.. code:: text

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



`Here <https://www.youtube.com/watch?v=awXkgS3Pc8s>`_ is the video of godot first build and test execution:

.. youtube::
    awXkgS3Pc8s
    width=100%
