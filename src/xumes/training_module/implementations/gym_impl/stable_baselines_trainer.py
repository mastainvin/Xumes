from abc import abstractmethod
from typing import final, TypeVar, List

import gymnasium as gym
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.monitor import Monitor

import xumes

from xumes.training_module.entity_manager import EntityManager
from xumes.training_module.i_communication_service_training import ICommunicationServiceTraining
from xumes.training_module.training_service import MarkovTrainingService

OBST = TypeVar("OBST")


class StableBaselinesTrainer(MarkovTrainingService):

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service: ICommunicationServiceTraining,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm,
                 random_reset_rate: float = 1.0
                 ):
        super().__init__(entity_manager, communication_service)
        self.env = Monitor(gym.make(
            id="xumes-v0",
            max_episode_steps=max_episode_length,
            training_service=self,
            observation_space=observation_space,
            action_space=action_space,
            random_reset_rate=random_reset_rate
        ), filename=None, allow_early_resets=True)
        self.algorithm = algorithm
        self.algorithm_type = algorithm_type
        self.total_timesteps = total_timesteps
        self.model = None

    @final
    def train(self, save_path: str = None, eval_freq: int = 10000, log_path: str = None, test_name: str = None):
        eval_callback = None
        if save_path:
            eval_callback = EvalCallback(self.env, best_model_save_path=save_path,
                                         log_path=save_path, eval_freq=eval_freq,
                                         deterministic=True, render=False)

        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1, tensorboard_log=log_path).learn(
            self.total_timesteps,
            callback=eval_callback,
            tb_log_name=test_name
        )

    @final
    def save(self, path: str):
        self.model.save(path)

    @final
    def load(self, path: str):
        self.model = self.algorithm(self.algorithm_type, self.env, verbose=1).load(path)

    @final
    def play(self, timesteps: int):
        obs, info = self.env.reset()
        for _ in range(timesteps):
            action, _states = self.model.predict(obs, deterministic=True)
            obs, reward, terminated, done, info = self.env.step(action)
            if done or terminated:
                self.env.reset(options={"not_random": True})

    @final
    def reward(self):
        return self.convert_reward()

    @final
    def terminated(self):
        return self.convert_terminated() or self._entity_manager.game_state == "reset" or self._entity_manager.game_state == "random_reset"

    @final
    def push_raw_actions(self, actions):
        self.push_actions(actions=self.convert_actions(actions))

    @final
    def get_obs(self) -> OBST:
        self.retrieve_state()
        return self.convert_obs()

    @abstractmethod
    def convert_obs(self) -> OBST:  # TODO Change pass to raise NotImplementedError
        pass

    @abstractmethod
    def convert_reward(self) -> float:
        pass

    @abstractmethod
    def convert_terminated(self) -> bool:
        pass

    @abstractmethod
    def convert_actions(self, raws_actions) -> List[str]:
        pass
