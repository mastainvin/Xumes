import logging
from abc import ABC
from typing import final, TypeVar, Optional

import gymnasium as gym
import stable_baselines3
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

# noinspection PyUnresolvedReferences
import xumes
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
                 algorithm=stable_baselines3.PPO,
                 ):
        super().__init__(agent)
        if observation_space is not None and action_space is not None:
            self.env = Monitor(gym.make(
                id="xumes-v0",
                max_episode_steps=max_episode_length,
                training_service=self,
                observation_space=observation_space,
                action_space=action_space,
            ), filename=None, allow_early_resets=True)
        self.algorithm = algorithm
        self.algorithm_type = algorithm_type
        self.total_timesteps = total_timesteps

        self.model = None

        self.observation_space = observation_space
        self.action_space = action_space
        self.max_episode_length = max_episode_length

        self.made = False

    @final
    def make(self):
        if self.observation_space is None or self.action_space is None:
            raise Exception("Observation space and action space must be set before calling make")
        self.env = Monitor(gym.make(
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

        if previous_model_path:
            self.model = self.algorithm(self.algorithm_type, self.env, verbose=1, tensorboard_log=logs_path).load(
                previous_model_path, env=self.env).learn(
                self.total_timesteps,
                callback=eval_callback,
                tb_log_name=logs_name,
            )
        else:
            self.model = self.algorithm(self.algorithm_type, self.env, verbose=1, tensorboard_log=logs_path).learn(
                self.total_timesteps,
                callback=eval_callback,
                tb_log_name=logs_name,
            )

        self.finished()

    def save(self, path: str):
        self.model.save(path)

    def free(self):
        if self.env is not None:
            self.env.close()
        self.model = None

    def load(self, path: str):
        if not self.made:
            self.make()

        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1).load(path, env=self.env)

    def play(self, timesteps: Optional[int] = None):

        if not self.made:
            self.make()

        obs, _ = self.env.reset()

        running = True

        def step():
            nonlocal obs
            action, _states = self.model.predict(obs, deterministic=True)
            try:
                obs, reward, terminated, done, info = self.env.step(action)
                if done or terminated:
                    self.env.reset()
            except RunningEndsError:
                logging.info(f"Received stop signal. Closing environment.")
                self.env.close()
                nonlocal running
                running = False

        if not timesteps:
            while running:
                step()
        else:
            for _ in range(timesteps):
                step()

    def finished(self):
        self.agent.game_service().finished()

    def predict(self, obs: OBST):
        """
        Predicts the action to take given the observation.
        Method used only when using the model in non-training model, inside a scripted bot.
        """
        return self.model.predict(obs)
