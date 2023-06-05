from __future__ import annotations

from typing import SupportsFloat, Any, Tuple, Dict

import gymnasium as gym
from gymnasium import Space
from gymnasium.core import RenderFrame, ActType, ObsType

from framework.training_service_module.trainer import _Trainer


class GymAdapter(gym.Env):

    def __init__(self,
                 trainer: _Trainer,
                 observation_space: Space[ObsType],
                 action_space: Space[ActType]
                 ):
        self._trainer = trainer
        self.observation_space = observation_space
        self.action_space = action_space

    def reset(
            self,
            *,
            seed: int | None = None,
            options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        self._trainer.random_reset()
        return self._trainer.get_obs(), {}

    def step(self, action: ActType) -> Tuple[ObsType, SupportsFloat, bool, bool, Dict[str, Any]]:
        self._trainer.push_action(action)
        obs = self._trainer.get_obs()
        reward = self._trainer.reward()
        done = self._trainer.terminated()
        return obs, reward, done, False, {}

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        return None
