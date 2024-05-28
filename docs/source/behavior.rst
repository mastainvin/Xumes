Agent Class
===========

The ``Agent`` class extends the ``Behavior`` class and represents a machine learning agent that interacts with the game. It implements a reinforcement learning approach for predicting actions.

Exemple
-------

Here is an example from the ``FlappyBird`` game, where the agent is a bird that learns to fly by jumping over obstacles.

.. code-block:: python

    class Fly(Agent):

        def __init__(self):
            super().__init__(
                observation_space=spaces.Dict({
                    "velocity": spaces.Box(-float('inf'), 300, shape=(2,), dtype=float),
                    "X": spaces.Box(-float('inf'), float('inf'), shape=(1,), dtype=float),
                    "Y": spaces.Box(-float('inf'), float('inf'), shape=(1,), dtype=float),
                    "Y1": spaces.Box(-float('inf'), float('inf'), shape=(1,), dtype=float),
                }),
                action_space=spaces.Discrete(2),
                max_episode_length=1000,
                total_timesteps=int(3_000_000),
                algorithm_type="MultiInputPolicy",
                algorithm=stable_baselines3.PPO,
                save_path="./models/fly",
                eval_freq=10000,
                )

            self.points = 0

        def observation(self):
            velocity = self.Game.Bird.velocity
            return {"velocity": np.array(velocity), "X": np.array(self.X), "Y": np.array(self.Y), "Y1": np.array(self.Y1)}

        def reward(self):
            if self.score > self.points:
                self.points = self.score
                return 1

            if self.dead or self.Game.Bird.position[1] < 0:
                return -1
            return 0

        def terminated(self):
            terminated = self.dead != 0 or self.score >= 2 or self.Game.Bird.position[1] < 0
            if terminated:
                self.points = 0
            return terminated

        def actions(self, raw_actions):
            if raw_actions == 1:
                return [{"type": "ACTION_EVENT", "action_name": "jump"}]
            return []


.. note:: As you can see I defined a attribute `points` to store the current score of the agent. In the ``terminated`` method, I reset the points to 0 when the episode is terminated.


Attributes
----------

- `_save_path` (str): The path to save the trained model.
- `_eval_freq` (int): The evaluation frequency during training.
- `_logs_path` (Optional[str]): The path to save training logs.
- `_logs_name` (Optional[str]): The name of the log files.
- `_previous_model_path` (Optional[str]): The path to a pre-trained model, if available.

and `stable_baselines3` attributes:

- `observation_space` (gym.spaces.Space): The observation space.
- `action_space` (gym.spaces.Space): The action space.
- `max_episode_length` (int): The maximum length of an episode.
- `total_timesteps` (int): The total number of timesteps.
- `algorithm_type` str: The algorithm type.
- `algorithm` stable_baselines3.base.BaseAlgorithm: The algorithm instance.
- `save_path` (str): The path to save the trained
- `eval_freq` (int): The evaluation frequency during training.

Abstract Methods
----------------

These methods must be implemented by any class that inherits from `Agent`.

.. automethod:: Agent.observation
    :noindex:

.. automethod:: Agent.reward
    :noindex:

.. automethod:: Agent.terminated
    :noindex:

.. automethod:: Agent.actions
    :noindex:

Abstract Methods Details
------------------------

.. _Agent.observation:

observation(self) -> OBST
    Abstract method to obtain observations from the environment.

    :return: The observations from the environment.
    :rtype: OBST

.. _Agent.reward:

reward(self) -> float
    Abstract method to obtain the agent's current reward.

    :return: The current reward.
    :rtype: float

.. _Agent.terminated:

terminated(self) -> bool
    Abstract method to check if the episode is terminated.

    :return: True if the episode is terminated, otherwise False.
    :rtype: bool

.. _Agent.actions:

actions(self, raws_actions) -> List
    Abstract method to obtain the list of possible actions for the agent.

    :param raws_actions: The raw actions to process.
    :type raws_actions: any
    :return: The list of possible actions.
    :rtype: List
