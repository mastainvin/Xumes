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
from xumes.test_runner.test_runner import TestRunner

from xumes.trainer.entity_manager import EntityManager
from xumes.trainer.training_service import MarkovTrainingService

OBST = TypeVar("OBST")


class StableBaselinesTrainer(MarkovTrainingService, ABC):

    def __init__(self,
                 entity_manager: EntityManager,
                 test_runner: TestRunner,
                 observation_space=None,
                 action_space=None,
                 max_episode_length: int = 1000,
                 total_timesteps: int = 1000000,
                 algorithm_type: str = "MultiInputPolicy",
                 algorithm=stable_baselines3.PPO,
                 ):
        super().__init__(entity_manager, test_runner)
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

    def train(self, save_path: str = None, eval_freq: int = 10000, logs_path: Optional[str] = None,
              logs_name: Optional[str] = None, previous_model_path: Optional[str] = None):
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

    def load(self, path: str):
        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1).load(path, env=self.env)

    def play(self, timesteps: Optional[int] = None):
        obs, _ = self.env.reset()

        def step():
            nonlocal obs
            action, _states = self.model.predict(obs, deterministic=True)
            try:
                obs, reward, terminated, done, info = self.env.step(action)
                if done or terminated:
                    self.env.reset(options={"not_random": True})
            except RunningEndsError:
                logging.info(f"Received stop signal. Closing environment.")

        if not timesteps:
            while True:
                step()
        else:
            for _ in range(timesteps):
                step()
