import importlib.util
import sys

import os
from abc import ABC, abstractmethod
from typing import List

from xumes.test_automation.registries import given, when, then


class Scenario:

    def __init__(self, name: str = None, steps: str = None, feature=None, tags=None):
        self.name = name
        self.steps: str = steps
        self.feature: Feature = feature

        if tags is None:
            tags = []
        self.tags = tags


class Feature:

    def __init__(self, scenarios=None, name: str = None):
        if scenarios is None:
            scenarios = []
        self.scenarios: List[Scenario] = scenarios
        self.name = name
        self.processes = []


class FeatureStrategy(ABC):
    """
    FeatureStrategy is a class that implements the strategy pattern to define a way to get
    all features.
    """

    def __init__(self, alpha: float = 0.001, steps_path: str = None, features_path: str = None):
        self.features: List[Feature] = []
        self._steps_files: List[str] = []

        self._alpha = alpha

        if not features_path:
            features_path = "./"

        self._features_path = features_path

        if not steps_path:
            steps_path = os.path.join(self._features_path, "steps")

        if not os.path.exists(steps_path):
            raise FileNotFoundError(f"Path {steps_path} does not exists.")

        self._load_tests(steps_path)

        self.given = given
        self.when = when
        self.then = then

    def _load_tests(self, path: str = "./"):
        current_dir = os.path.dirname(os.path.abspath(__file__))

        parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
        sys.path.insert(0, parent_dir)

        for file in os.listdir(path):
            if file.endswith(".py"):
                module_path = os.path.join(path, file)
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

                self._steps_files.append(file[:-3])

    @abstractmethod
    def retrieve_features(self):
        """
        Get all features.
        """
        raise NotImplementedError


class DummyFeatureStrategy(FeatureStrategy):
    def retrieve_features(self):
        pass
