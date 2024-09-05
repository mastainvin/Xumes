import logging
from abc import ABC
from typing import final, TypeVar, Optional, Type

import gymnasium
import stable_baselines3
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

# noinspection PyUnresolvedReferences
import xumes
from stable_baselines3.common.policies import ActorCriticPolicy
from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.modules.reinforcement_learning.agent_trainer import AgentTrainer

OBST = TypeVar("OBST")


class StableBaselinesTrainer(AgentTrainer, ABC):

    def __init__(self,
                 agent,
                 observation_space=None,
                 action_space=None,
                 max_episode_length: int = 1000,
                 total_timesteps: int = 1000000,
                 algorithm_type: str = "MultiInputPolicy",
                 algorithm: Type[ActorCriticPolicy] = stable_baselines3.PPO,
                 policy_kwargs: Optional[dict] = None,
                 ):
        super().__init__(agent)
        if observation_space is not None and action_space is not None:
            self.env = Monitor(gymnasium.make(
                id="xumes-v0",
                max_episode_steps=max_episode_length,
                training_service=self,
                observation_space=observation_space,
                action_space=action_space,
            ), filename=None, allow_early_resets=True)
        self.policy_class = algorithm
        self.algorithm_type = algorithm_type
        self.total_timesteps = total_timesteps

        # self.model = None

        self.observation_space = observation_space
        self.action_space = action_space
        self.max_episode_length = max_episode_length

        self.made = False

        self.policy = None

        self.policy_kwargs = policy_kwargs

    @final
    def make(self):
        if self.observation_space is None or self.action_space is None:
            raise Exception("Observation space and action space must be set before calling make")
        self.env = Monitor(gymnasium.make(
            id="xumes-v0",
            max_episode_steps=self.max_episode_length,
            training_service=self,
            observation_space=self.observation_space,
            action_space=self.action_space,
        ), filename=None, allow_early_resets=True)
        self.made = True

    def train(self, save_path: str = None, eval_freq: int = 1000, logs_path: Optional[str] = None,
              logs_name: Optional[str] = None, previous_model_path: Optional[str] = None):

        if not self.made:
            self.make()

        eval_callback = None
        if save_path:
            eval_callback = EvalCallback(self.env, best_model_save_path=save_path,
                                         log_path=save_path, eval_freq=eval_freq,
                                         deterministic=True, render=False)

        self.make_algo(logs_path)

        if previous_model_path:
            self.policy = self.policy.load(previous_model_path)

        self.policy = self.policy.learn(
            self.total_timesteps,
            callback=eval_callback,
            tb_log_name=logs_name,
        )

        self.finished()

    def save(self, path: str):
        self.policy.save(path)

    def free(self):
        if self.env is not None:
            self.env.close()
        self.policy = None

    def load(self, path: str):
        if not self.made:
            self.make()

        self.make_algo()

        self.policy = self.policy.load(path, env=self.env)

    def make_algo(self, logs_path: Optional[str] = None):
        if not self.made:
            self.make()

        self.policy = self.policy_class(self.algorithm_type, self.env, verbose=1, tensorboard_log=logs_path, policy_kwargs=self.policy_kwargs)

    def get_env(self):
        return self.env

    def get_policy(self):
        return self.policy

    def play(self, time_steps: Optional[int] = None):

        if not self.made:
            self.make()

        obs, _ = self.env.reset()

        running = True

        def step():
            nonlocal obs
            nonlocal running

            action, _states = self.policy.predict(obs, deterministic=True)
            try:
                obs, reward, terminated, done, info = self.env.step(action)
                if done or terminated:
                    self.env.reset()
            except RunningEndsError:
                logging.info(f"Received stop signal. Closing environment.")
                self.env.close()
                running = False
            except Exception as e:
                logging.error(f"Error in step: {e}")
                self.env.close()
                running = False

        if not time_steps:
            while running:
                step()
        else:
            for _ in range(time_steps):
                step()

    def finished(self):
        self.policy.test_runner().finished()

    def predict(self, obs: OBST):
        """
        Predicts the action to take given the observation.
        Method used only when using the model in non-training model, inside a scripted bot.
        """
        return self.policy.predict(obs)[0]
