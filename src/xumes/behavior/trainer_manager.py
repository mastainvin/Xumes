import importlib.util
import importlib.util
import logging
import multiprocess
import os

from abc import abstractmethod
from typing import List, Dict

from xumes.core.modes import TEST_MODE, TRAIN_MODE
from xumes.core.registry import create_registry
from xumes.test_runner.test_runner import TestRunner
from xumes.behavior.entity_manager import AutoEntityManager
from xumes.behavior.i_trainer import ITrainer
from xumes.modules.reinforcement_learning.stable_baselines_trainer import OBST, StableBaselinesTrainer
from xumes.modules.reinforcement_learning.vec_stable_baselines_trainer import VecStableBaselinesTrainer
from xumes.behavior.implementations.json_impl.json_game_element_state_converter import JsonGameElementStateConverter

observation = create_registry()
action = create_registry()
reward = create_registry()
terminated = create_registry()
config = create_registry()

observation_registry = observation.all
action_registry = action.all
reward_registry = reward.all
terminated_registry = terminated.all
config_registry = config.all


class TrainerManager:
    """
    Base class for behavior managers.

    Args:
        mode (str, optional): The mode of the behavior manager. Defaults to TEST_MODE.
        port (int, optional): The port number for the communication service. Defaults to 5000.
    """

    def __init__(self, mode: str = TEST_MODE,
                 port: int = 5000, do_logs: bool = False, model_path: str = None, logging_level=logging.NOTSET, trainers_path=None):
        self._load_trainers(trainers_path)
        self._trainer_processes: Dict[str, multiprocess.Process] = {}
        self._mode = mode
        self._port = port
        self._do_logs = do_logs
        self._previous_model_path = model_path
        self._logging_level = logging_level

    # noinspection DuplicatedCode
    @staticmethod
    def _load_trainers(path: str = "./"):
        for file in os.listdir(path):
            if file.endswith(".py"):
                module_path = os.path.join(path, file)
                module_path = os.path.abspath(module_path)
                module_name = os.path.basename(module_path)[:-3]

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module_dep = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module_dep)

    def run(self):
        if self._mode == TRAIN_MODE:
            self.train()
        elif self._mode == TEST_MODE:
            self.play()

    def _init_logger(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)

    # connect_trainer, disconnect_trainer, create_and_train, create_and_play
    # shall not be abstract methods, but because of the registry queue they are
    #  for the moment. TODO find a pattern to avoid this

    @abstractmethod
    def connect_trainer(self, test_runner: TestRunner, feature: str, scenario: str) -> None:
        # Create a new process to train or use an agent
        raise NotImplementedError

    @abstractmethod
    def disconnect_trainer(self, feature: str, scenario: str) -> None:
        # Terminate the process
        raise NotImplementedError

    @abstractmethod
    def create_and_train(self, test_runner: TestRunner, feature: str, scenario: str, queue: multiprocess.Queue):
        # Create a new behavior and train it
        raise NotImplementedError

    @abstractmethod
    def create_and_play(self, test_runner: TestRunner, feature: str, scenario: str, queue: multiprocess.Queue):
        # Create a new behavior and play it
        raise NotImplementedError

    @abstractmethod
    def play(self):
        raise NotImplementedError

    @abstractmethod
    def train(self):
        raise NotImplementedError

    @abstractmethod
    def reset_trainer(self):
        raise NotImplementedError

    @abstractmethod
    def create_trainer(self, test_runner: TestRunner, feature: str, scenario: str, observation_r, action_r, reward_r, terminated_r,
                       config_r) -> ITrainer:
        # Abstract method to create a behavior for a specific feature and scenario
        # This method should be implemented by the concrete behavior manager
        raise NotImplementedError

    @abstractmethod
    def _trainer_name(self, feature, scenario) -> str:
        # Abstract method to create a behavior name for a specific feature and scenario
        # This method should be implemented by the concrete behavior manager
        raise NotImplementedError

    @abstractmethod
    def _model_path(self, feature, scenario) -> str:
        # Abstract method to create a model path for a specific feature and scenario
        # This method should be implemented by the concrete behavior manager
        raise NotImplementedError


class StableBaselinesTrainerManager(TrainerManager):
    """
    Concrete behavior manager for stable baselines trainers.rst
    Use to train each agent on a different model
    """

    def reset_trainer(self):
        pass

    def play(self):
        pass

    def train(self):
        pass

    def create_trainer(self, test_runner: TestRunner, feature: str, scenario: str, observation_r, action_r, reward_r, terminated_r,
                       config_r) -> ITrainer:
        # We use the decorators to implement the behavior's methods

        class ConcreteTrainer(StableBaselinesTrainer):
            def convert_obs(self) -> OBST:
                return observation_r[feature](self)

            def convert_reward(self) -> float:
                return reward_r[feature](self)

            def convert_terminated(self) -> bool:
                return terminated_r[feature](self)

            def convert_actions(self, raws_actions) -> List[str]:
                return action_r[feature](self, raws_actions)

        try:
            trainer = ConcreteTrainer(entity_manager=AutoEntityManager(JsonGameElementStateConverter()), test_runner=test_runner,)

            config_r[feature](trainer)
            trainer.make()
        except Exception as e:
            raise Exception(f"Error while creating behavior: {e}")

        return trainer

    def connect_trainer(self, test_runner: TestRunner, feature: str, scenario: str) -> None:
        # Create a new process to train or  use an agent
        name = self._trainer_name(feature, scenario)

        registry_queue = multiprocess.Queue()
        registry_queue.put(
            (observation_registry, action_registry, reward_registry, terminated_registry, config_registry))

        if self._mode == TRAIN_MODE:
            self.create_and_train(test_runner, feature, scenario, registry_queue)
        elif self._mode == TEST_MODE:
            self.create_and_play(test_runner, feature, scenario, registry_queue)

    def disconnect_trainer(self, feature: str, scenario: str) -> None:
        # Terminate the process
        name = self._trainer_name(feature, scenario)
        if name in self._trainer_processes:
            self._trainer_processes[name].terminate()
            self._trainer_processes[name].join()
            del self._trainer_processes[name]

    def create_and_train(self, test_runner: TestRunner, feature: str, scenario: str, queue: multiprocess.Queue):
        self._init_logger()
        # Create a new behavior and train it
        observation_r, action_r, reward_r, terminated_r, config_r = queue.get()
        trainer = self.create_trainer(test_runner, feature, scenario, observation_r, action_r, reward_r, terminated_r,
                                      config_r)
        trainer.train(self._model_path(feature, scenario),
                      logs_path=self._model_path(feature, scenario) + "/../_logs" if self._do_logs else None,
                      logs_name=scenario, previous_model_path=self._previous_model_path)

    def create_and_play(self, test_runner: TestRunner, feature: str, scenario: str, queue: multiprocess.Queue):
        self._init_logger()
        # Create a new behavior and play it
        logging.basicConfig(format='%(levelname)s:%(message)s', level=self._logging_level)
        observation_r, action_r, reward_r, terminated_r, config_r = queue.get()
        trainer = self.create_trainer(test_runner, feature, scenario, observation_r, action_r, reward_r, terminated_r,
                                      config_r)
        trainer.load(self._model_path(feature, scenario) + "/best_model")
        trainer.play(timesteps=None)

    def _trainer_name(self, feature, scenario) -> str:
        return feature + "_" + scenario

    def _model_path(self, feature, scenario) -> str:
        return "./models/" + feature + "/" + scenario


class VecStableBaselinesTrainerManager(StableBaselinesTrainerManager):
    """
    Concrete behavior manager for stable baselines trainers.rst
    Use to train all agents on the same model
    """

    def __init__(self, port: int,
                 mode=TEST_MODE, do_logs=False, model_path: str = None, logging_level=logging.NOTSET):
        super().__init__(mode=mode, port=port, do_logs=do_logs, model_path=model_path,
                         logging_level=logging_level)

        # Create a vectorized behavior
        # This behavior will train all agents on the same model
        self.vec_trainer = VecStableBaselinesTrainer()
        self._training_services_datas = set()
        self._trained_feature = None
        self._process = None

    def connect_trainer(self, test_runner: TestRunner, feature: str, scenario: str) -> None:
        # Add a new training service to the vectorized behavior
        if self._trained_feature is None:
            self._trained_feature = feature
        self._training_services_datas.add((feature, scenario))

    def reset_trainer(self):
        self._process.terminate()
        self._process.join()

        self.vec_trainer = VecStableBaselinesTrainer()
        self._trained_feature = None
        self._process = None
        self._training_services_datas = set()

    def train(self):
        registry_queue = multiprocess.Queue()
        registry_queue.put(
            (observation_registry, action_registry, reward_registry, terminated_registry, config_registry))
        self._train_agent(registry_queue)

    def _init_vec_trainer(self, registry_queue):
        self._init_logger()
        observation_r, action_r, reward_r, terminated_r, config_r = registry_queue.get()

        for (feature, scenario, port) in self._training_services_datas:
            self.vec_trainer.add_training_service(
                self.create_trainer(feature, scenario, port, observation_r, action_r, reward_r, terminated_r, config_r))

        self.vec_trainer.make()

    def _train_agent(self, registry_queue):
        self._init_vec_trainer(registry_queue)
        logging.info("Training model")
        self.vec_trainer.train(self._model_path(self._trained_feature, ""),
                               logs_path=self._model_path(self._trained_feature,
                                                          "") + "/_logs" if self._do_logs else None,
                               logs_name=self._trained_feature if self._do_logs else None,
                               previous_model_path=self._previous_model_path)
        logging.info("Saving model")
        self.vec_trainer.save(self._model_path(self._trained_feature, "") + "/best_model")

    def play(self):
        registry_queue = multiprocess.Queue()
        registry_queue.put(
            (observation_registry, action_registry, reward_registry, terminated_registry, config_registry))

        process = multiprocess.Process(target=self._play_agent, args=(registry_queue,))
        process.start()
        self._process = process

    def _play_agent(self, registry_queue):
        self._init_vec_trainer(registry_queue)
        # logging.info("Loading model")
        self.vec_trainer.load(self._model_path(self._trained_feature, "") + "/best_model")
        logging.info("Playing model")
        self.vec_trainer.play()

    def _trainer_name(self, feature, scenario) -> str:
        return feature

    def _model_path(self, feature, scenario) -> str:
        return "./models/" + feature
