Quickstart
==========

Once `Xumes` and `Godot` are installed, you can test your installation with the Flappy Bird example. First, clone the repository:

.. code-block:: bash

    git clone https://github.com/mastainvin/Xumes-Examples.git

Then, navigate to the `FlappyBird` directory:

.. code-block:: bash

    cd Xumes-Examples/Godot/flappy_bird/Tests/PipeSizeTest

Run the tests with the following command:

.. code-block:: bash

    xumes test --features_path=./features --steps_path=./features/steps -h 10 -i 100 -v

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
