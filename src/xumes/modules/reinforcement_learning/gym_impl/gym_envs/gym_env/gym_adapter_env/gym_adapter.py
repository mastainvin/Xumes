from __future__ import annotations

from typing import SupportsFloat, Any, Tuple, Dict

import gymnasium as gym
from gymnasium import Space
from gymnasium.core import RenderFrame, ActType, ObsType

from xumes.modules.reinforcement_learning.agent_trainer import AgentTrainer


class GymAdapter(gym.Env):

    def __init__(self,
                 training_service: AgentTrainer,
                 observation_space: Space[ObsType],
                 action_space: Space[ActType],
                 ):
        self._trainer = training_service
        self.observation_space = observation_space
        self.action_space = action_space
        self._first_reset = True

    def reset(
            self,
            *,
            seed: int | None = None,
            options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        self._trainer.do_reset()
        if self._first_reset:
            self._first_reset = False
        else:
            self._trainer.episode_finished()
        return self._trainer.get_obs(), {}

    def step(self, action: ActType) -> Tuple[ObsType, SupportsFloat, bool, bool, Dict[str, Any]]:
        obs = self._trainer.push_actions_and_get_obs(action)
        reward = self._trainer.get_reward()
        terminated = self._trainer.get_terminated()
        return obs, reward, terminated, False, {}

    def render(self) -> RenderFrame | list[RenderFrame] | None:
        return None
