import logging

from xumes.core.manager import Manager
from xumes.core.modes import TRAIN_MODE
from xumes.test_runner.implementations.socket_impl.communication_service_game_socket import \
    CommunicationServiceGameSocket
from xumes.test_runner.test_runner import TestRunner
from xumes.trainer import StableBaselinesTrainerManager
from xumes.trainer.trainer_manager import observation_registry, action_registry, reward_registry, terminated_registry, config_registry

# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
communication_service = CommunicationServiceGameSocket(host='127.0.0.1')

test_runner = TestRunner(communication_service)
test_runner.run(port=8081)


trainer_manager = StableBaselinesTrainerManager(mode=TRAIN_MODE, trainers_path="/home/vincent/Documents/Xumes_project/flappy_bird/test/pipe_size_delta/trainers/")

trainer = trainer_manager.create_trainer(test_runner, "jump", "scenario", observation_registry, action_registry, reward_registry, terminated_registry, config_registry)


trainer.train(previous_model_path="/home/vincent/Documents/Xumes_project/flappy_bird/test/pipe_size_delta/trainers/pretrained")
trainer.save("/home/vincent/Documents/Xumes_project/flappy_bird/test/pipe_size_delta/trainers/pretrained2")
