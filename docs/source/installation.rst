Installation
============

To use Xumes, first install it using pip:

.. code:: bash

   $ pip install -i https://test.pypi.org/simple/ xumes

It’s possible that certain dependencies will not be found on
test.pypi.org so you may have to install them yourself.

Install dependencies with pip:

.. code:: bash

   $ pip install "gymnasium>=0.28.1" "pygame>=2.4.0" "numpy>=1.24.3" "pyzmq>=25.1.0" "flask>=2.3.2" "requests>=2.30.0" "click>=8.1.3" "statsmodels>=0.14.0" "gherkin-official>=24.1.0" "multiprocess>=0.70.14" "sphinx-rtd-theme>=1.2.2"
   $ pip install "sb3_contrib>=2.0.0a1" --upgrade
   $ pip install "stable_baselines3>=2.0.0a1" --upgrade
