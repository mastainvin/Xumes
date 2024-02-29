import logging

from xumes.core.manager import Manager
from xumes.core.modes import TRAIN_MODE, TEST_MODE
from xumes.test_runner.feature_strategy import FeatureStrategy, DummyFeatureStrategy, Feature, Scenario
from xumes.test_runner.implementations.socket_impl.communication_service_game_socket import \
    CommunicationServiceGameSocket
from xumes.test_runner.test_runner import TestRunner
from xumes.trainer import StableBaselinesTrainerManager
from xumes.trainer.trainer_manager import observation_registry, action_registry, reward_registry, terminated_registry, config_registry

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
communication_service = CommunicationServiceGameSocket(host='127.0.0.1')

feature = Feature(name="PipeSizeDelta")
scenario = Scenario(feature=feature, name="0_100")
feature_strategy = DummyFeatureStrategy()

test_runner = feature_strategy.build_test_runner(scenario=scenario, iterations=100, mode=TEST_MODE, comm_service=communication_service)
test_runner.run(port=8081)


trainer_manager = StableBaselinesTrainerManager(mode=TEST_MODE, trainers_path="/home/vincent/Documents/Xumes_project/flappy_bird/test/pipe_size_delta/trainers/")

trainer = trainer_manager.create_trainer(test_runner, "jump", "scenario", observation_registry, action_registry, reward_registry, terminated_registry, config_registry)


trainer.load("/home/vincent/Documents/Xumes_project/flappy_bird/test/pipe_size_delta/trainers/pretrained/best_model")
trainer.play()

#  --fixed-fps 10 --headless --disable-render-loop