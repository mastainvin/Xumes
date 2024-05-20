import importlib
import os
from abc import abstractmethod

from xumes.test_runner.test_runner import TestRunner
from xumes.behavior.behavior import Behavior


class IBehaviorFactory:

    @abstractmethod
    def create_behavior(self, test_runner: TestRunner, feature: str, scenario: str, behavior: Behavior):
        pass


class TrainerFactory(IBehaviorFactory):

    @abstractmethod
    def create_behavior(self, test_runner: TestRunner, feature: str, scenario: str, behavior: Behavior):
        pass


class SBTrainerFactory(TrainerFactory):

    def create_behavior(self, test_runner: TestRunner, feature: str, scenario: str, behavior: Behavior):
        module = importlib.import_module(f"xumes.trainer.implementations.rl_impl.{feature}.{scenario}")
        class_ = getattr(module, behavior)
        return class_(test_runner)
