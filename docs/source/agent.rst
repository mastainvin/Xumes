Agent Class
===========

The ``Agent`` class extends the ``Behavior`` class and represents a machine learning agent that interacts with the game. It implements a reinforcement learning approach for predicting actions.

.. autoclass:: xumes.Agent
    :members: observation,reward,terminated,actions

Exemple
-------

Here is an example from the ``FlappyBird`` game, where the agent is a bird that learns to fly by jumping over obstacles.

.. code-block:: python

    class Fly(Agent):

        def __init__(self, model_path: str = None):
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
                save_path=model_path if model_path is not None else "./Tests/PipeSizeTest/models/fly",
                eval_freq=10000,
            )

            self.points = 0

        def observation(self):
            velocity = self.context.Game.Bird.velocity
            return {"velocity": np.array(velocity, dtype=float),
                    "X": np.array([self.context.X], dtype=float),
                    "Y": np.array([self.context.Y], dtype=float),
                    "Y1": np.array([self.context.Y1], dtype=float)}

        def reward(self):
            if self.context.score > self.points:
                self.points = self.context.score
                return 1

            if self.context.dead or self.context.Game.Bird.position[1] < 0:
                return -1
            return 0

        def terminated(self):
            terminated = self.context.dead != 0 or self.context.score >= 2 or self.context.Game.Bird.position[1] < 0
            if terminated:
                self.points = 0
            return terminated

        def actions(self, raw_actions):
            if raw_actions == 1:
                return [GodotAction("jump")]
            return []


.. note:: As you can see I defined a attribute `points` to store the current score of the agent. In the ``terminated`` method, I reset the points to 0 when the episode is terminated.




