Trainer files
=============

In our architecture, a trainer has the goal to create a model for a particular feature.
So you will need to create a trainer for each feature you want to train. The file name must be the same as the feature name.
For example, if you want to train the `fight` feature, you will need to create a `fight.py` file.

Each trainer file while require to implement the following methods using python decorators:

.. method:: @config

    :type: Method
    :description: This method will configure the trainer. You can define the algorithm, the number of steps, the number of iterations, etc. And also define what you need to train your model.

.. method:: @observation

    :type: Method
    :description: This method will return the observation of the game state and extract the features.

.. method:: @action

    :type: Method
    :description: This method will convert the output of the model to a game action.

.. method:: @terminated

    :type: Method
    :description: This method will convert the observation of the game state to a boolean that indicates if the game is terminated. You can also reset every variable you need.

.. method:: @reward

    :type: Method
    :description: This method will convert the observation of the game state to a reward.



Here's an example of implementation:

.. code:: python

    @config
    def train_impl(train_context):
        # Define useful values you need to train your model
        train_context.points = 0

        # Define what the model needs
        train_context.observation_space = spaces.Dict({
            "speedup": spaces.Box(-float('inf'), 300, shape=(1,), dtype=float),
            "lidar": spaces.Box(0, LIDAR_MAX_DIST, shape=(7,), dtype=int),
        })
        train_context.action_space = spaces.Discrete(2)
        train_context.max_episode_length = 2000
        train_context.total_timesteps = int(2e4)
        train_context.algorithm_type = "MultiInputPolicy"
        train_context.algorithm = stable_baselines3.PPO

    @observation
    def train_impl(train_context):
        return {"entity": np.array([train_context.entity.attr1])}

    @action
    def train_impl(train_context, actions):
        if actions == 0:
            return ["space"]
        return ["nothing"]

    @terminated
    def train_impl(train_context):
        t = train_context.game.lose or train_context.game.win
        if t: # Reset what you want
            train_context.points = 0

        return t

    @reward
    def train_impl(self):
        return 1 if self.game.win else 0

.. important:: We are using `StableBaselines3` to train the models. Check the `stablebaselines` `documentation <https://stable-baselines3.readthedocs.io/en/master/>`_ for more information.
