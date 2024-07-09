import pickle
from types import FunctionType
from typing import List, Type, Callable, Any, Optional

import gymnasium as gym
import numpy as np
import torch
from imitation.algorithms import bc

from imitation.algorithms.base import BaseImitationAlgorithm
from abc import ABC, abstractmethod

from imitation.data.types import Trajectory, DictObs
from xumes import Agent, Input
from xumes.test_automation.behavior import Behavior


class Imitator(Behavior, ABC):
    def __init__(self, agent: Agent, algorithm: Type[BaseImitationAlgorithm], threshold: float = 0,
                 collected_data_path: str = None, n_epochs: int = 20):
        super().__init__()
        self._agent = agent
        self._algorithm = algorithm
        self._made = False
        self._threshold = threshold
        self._n_epochs = n_epochs
        self._collected_data_path = collected_data_path if collected_data_path else "collected_data.pkl"

    def make(self):
        if self._made:
            return
        self._made = True
        self._agent.set_mode(self._mode)
        self._agent.set_test_runner(self.test_runner)
        self._agent.get_trainer().make_algo()

    def execute(self, feature, scenario):
        self.make()
        self._env = self._agent.get_trainer().get_env()
        rng = np.random.default_rng(42)

        trajectories = self._load_trajectories()

        policy = self._agent.get_trainer().get_policy()

        bc_trainer = bc.BC(
            observation_space=self._env.observation_space,
            action_space=self._env.action_space,
            policy=policy.policy,
            rng=rng,
            demonstrations=trajectories,
            device="cpu",
        )
        bc_trainer.train(n_epochs=self._n_epochs)

        policy.save(self._agent.get_path() + "/bc_policy.zip")

    def _load_trajectories(self):
        with open(self._collected_data_path + "/collected_data.pkl", "rb") as f:
            collected_data = pickle.load(f)

        # Convertir les données collectées en Trajectory
        trajectories = []
        for episode in collected_data:
            observations = []
            actions = []
            rewards = []
            dones = []
            new_observation = None
            for obs, action, reward, new_observation, done in episode:
                observations.append(obs)
                actions.append(action)
                rewards.append(reward)
                dones.append(done)

            observations.append(new_observation)
            trajectories.append(Trajectory(
                obs=DictObs({key: np.array([obs[key] for obs in observations]) for key in observations[0].keys()}),
                acts=np.array(actions),
                infos=None,
                terminal=dones[-1],
            ))

        return trajectories

    @abstractmethod
    def convert_input(self, key) -> np.ndarray:
        """
        Convert Pygame input to the appropriate action.
        """
        pass

    def input_to_action(self, inputs: np.ndarray) -> List[Input]:
        """
        Convert input to action.
        """
        return self._agent.actions(inputs)

    @property
    def agent(self):
        return self._agent

    def terminated(self) -> bool:
        return self._agent.terminated()

    @property
    def path(self):
        return self._collected_data_path

    @property
    def threshold(self):
        return self._threshold


class LambdaImitator(Imitator):
    def __init__(self, agent: Agent, algorithm: Type[BaseImitationAlgorithm], convert_input: Callable[
        [Any], np.ndarray], threshold: float = 0,
                 collected_data_path: str = None):
        super().__init__(agent, algorithm, threshold, collected_data_path)
        self._convert_input = convert_input

    def convert_input(self, keys):
        return self._convert_input(keys)
