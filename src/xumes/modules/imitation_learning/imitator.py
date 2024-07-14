import pickle
from typing import List, Callable, Any

import numpy as np

from abc import ABC, abstractmethod

from imitation.data.types import Trajectory, DictObs

from xumes import Agent, Input
from xumes.modules.imitation_learning.imitation_learning_algorithm import ImitationLearningAlgorithm
from xumes.modules.reinforcement_learning.stable_baselines_trainer import StableBaselinesTrainer
from xumes.modules.reinforcement_learning.vec_stable_baselines_trainer import VecStableBaselinesTrainer
from xumes.test_automation.behavior import Behavior


class Imitator(Behavior, ABC):
    """
    Base class for behavior imitation.
    """

    def __init__(self,
                 algorithm: ImitationLearningAlgorithm,
                 threshold: float = 0,
                 collected_data_path: str = None,
                 n_epochs: int = 20):
        """
        Base class for behavior imitation.
        Args:
            algorithm (ImitationLearningAlgorithm): The imitation learning algorithm.
            threshold (float): The threshold for the imitation learning algorithm.
            collected_data_path (str): The path to the collected data.
            n_epochs (int): The number of epochs.
        """

        super().__init__()
        self._agent = None
        self._algorithm = algorithm
        self._made = False
        self._threshold = threshold
        self._n_epochs = n_epochs
        self._collected_data_path = collected_data_path if collected_data_path else "collected_data.pkl"
        self._vec_sb_trainers = VecStableBaselinesTrainer()

        self._agent = None  # Use for collecting data

    def make(self):
        if self._made:
            return
        self._made = True
        self._vec_sb_trainers.make()

    def make_algo(self):
        self._vec_sb_trainers.make_algo()

    def add_trainer(self, trainer: StableBaselinesTrainer):
        self._vec_sb_trainers.add_trainer(trainer)

    def set_agent(self, agent: Agent):
        self._agent = agent

    @property
    def agent(self):
        return self._agent

    def execute(self, feature, scenario):
        self.make()
        self.make_algo()

        venv = self._vec_sb_trainers.venv
        rng = np.random.default_rng(42)
        trajectories = self._load_trajectories()
        policy = self._vec_sb_trainers.policy

        self._algorithm.execute(venv, policy, rng, trajectories, "cpu")

        policy.save(self._agent.get_path() + "/bc_policy.zip")

    def _load_trajectories(self) -> List[Trajectory]:
        """
        Load the trajectories from the collected data.
        Returns: The list of trajectories.
        """

        with open(self._collected_data_path + "/collected_data.pkl", "rb") as f:
            collected_data = pickle.load(f)

        # Convert data to Trajectories
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
    def convert_input(self, keys) -> np.ndarray:
        """
        Convert Pygame input to the appropriate action.
        """
        pass

    def input_to_action(self, inputs: np.ndarray) -> List[Input]:
        """
        Convert input to action.
        """
        return self._agent.actions(inputs)

    def terminated(self) -> bool:
        return self._agent.terminated()

    @property
    def path(self):
        return self._collected_data_path

    @property
    def threshold(self):
        return self._threshold

    def free(self):
        self._vec_sb_trainers.free()


class LambdaImitator(Imitator):
    def __init__(self, algorithm: ImitationLearningAlgorithm, convert_input: Callable[
        [Any], np.ndarray], threshold: float = 0,
                 collected_data_path: str = None):
        super().__init__(algorithm=algorithm, threshold=threshold, collected_data_path=collected_data_path)
        self._convert_input = convert_input

    def convert_input(self, keys):
        return self._convert_input(keys)
