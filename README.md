# Xumes

<table style="width: 100%;">
   <tr style="border: none">
      <td style="border: none; width: 75%; vertical-align: top;">
         <p>Xumes is a game testing tool designed to be used on top of games without the need to modify the game sources. It provides a framework for observing and interacting with game elements, training models, and conducting tests. For the moment, only the Godot framework has an implemented module for interacting with Xumes. So for the moment, the documentation will be focused on the implementation with Godot.</p>
         <p>Please check the <a href="https://xumes.readthedocs.io/en/latest/">documentation</a> for more information.</p>
      </td>
      <td style="border: none; width: 5%;"></td>
      <td style="border: none; width: 20%; vertical-align: top;">
         <img src="/docs/source/_static/fb.gif" alt="Test Animation" style="display: block; max-width: 100%;">
      </td>
   </tr>
</table>

## Framework

The framework is based on the BDD methodology, that's means that two type of files are needed to be write for conducting tests. Those file are the `feature` files and the `steps` files.

The following diagram illustrates the architecture of the framework:

![framework schema](/docs/source/_static/architecture.png)

## Installation

```bash
pip install xumes
```


## Using with Godot

To use Xumes with Godot, you need to compile Godot from sources. Follow the instructions in the `Godot documentation <https://docs.godotengine.org/en/stable/development/compiling/index.html>`_.

Clone the following repository instead of the official one:

```bash
git clone https://github.com/mastainvin/godot.git
```

> Don't forget to checkout to the `xumes` branch before build `Godot`.


To start the `Godot` editor, run the following command:

```bash
 ./bin/godot.x11.tools.64 --editor --path <path_to_godot_project>
```


## Quick start

Once `Xumes` and `Godot` are installed, you can test your installation with the Flappy Bird example. First, clone the repository:

```bash
git clone https://github.com/mastainvin/Xumes-Examples.git
```

Then, navigate to the `FlappyBird` directory:

```bash
cd Xumes-Examples/Godot/flappy_bird/
```

Run the tests with the following command:

```bash
python -m xumes test ./Tests/PipeSizeTest/features -h 10 -i 100
```

> ⚠️ Always use `python -m xumes` to run the tests. This ensures the use `Xumes` as a module and be able to import other modules in the project.

This command will run the tests found in the `features` directory in headless mode (without rendering the game), with a frame rate limit of 10 FPS and 100 iterations.

You should see the following output:


```text
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
```

[Here](https://www.youtube.com/watch?v=awXkgS3Pc8s) is the video of godot first build and test execution.

