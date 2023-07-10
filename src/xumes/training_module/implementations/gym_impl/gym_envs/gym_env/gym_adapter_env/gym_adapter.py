from __future__ import annotations

import random
from typing import SupportsFloat, Any, Tuple, Dict

import gymnasium as gym
from gymnasium import Space
from gymnasium.core import RenderFrame, ActType, ObsType

from xumes.training_module.training_service import MarkovTrainingService


class GymAdapter(gym.Env):

    def __init__(self,
                 training_service: MarkovTrainingService,
                 observation_space: Space[ObsType],
                 action_space: Space[ActType],
                 random_reset_rate: float = 1.0,
                 ):
        self._training_service = training_service
        self.observation_space = observation_space
        self.action_space = action_space
        self.random_reset_rate = random_reset_rate

    def reset(
            self,
            *,
            seed: int | None = None,
            options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        if (options and "not_random" in options and options["not_random"]) or random.random() < 1 - self.random_reset_rate:
            self._training_service.reset()
        else:
            self._training_service.random_reset()
        return self._training_service.get_obs(), {}

    def step(self, action: ActType) -> Tuple[ObsType, SupportsFloat, bool, bool, Dict[str, Any]]:
        self._training_service.push_raw_actions(action)
        obs = self._training_service.get_obs()
        reward = self._training_service.reward()
        terminated = self._training_service.terminated()
        return obs, reward, terminated, False, {}

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        return None
