Installation
============

To use Xumes, first install it using pip:

.. code-block:: bash

    pip install xumes

Using Godot
-----------

To use Xumes with Godot, you need to compile Godot from sources. Follow the instructions in the `Godot documentation <https://docs.godotengine.org/en/stable/development/compiling/index.html>`_.

Clone the following repository instead of the official one:

.. code-block:: bash

    git clone https://github.com/mastainvin/godot.git

.. note::

    Don't forget to checkout to the `xumes` branch before build `Godot`.


To start the `Godot` editor, run the following command:

.. code-block:: bash

    ./bin/godot.x11.tools.64 --editor --path <path_to_godot_project>