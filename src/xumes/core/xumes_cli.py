import logging
import os
import platform
from multiprocessing import set_start_method

import click

from xumes.core.modes import TRAIN_MODE, FEATURE_MODE, SCENARIO_MODE
from xumes.test_runner.implementations.features_impl.gherkin_feature_strategy import GherkinFeatureStrategy
from xumes.test_runner.implementations.rest_impl.communication_service_rest import CommunicationServiceRest
from xumes.test_runner.test_manager import TestManager, VecRLTestManager, RLTestManager



@click.group()
def cli():
    pass


def get_debug_level(debug, info):
    if debug:
        return logging.DEBUG
    if info:
        return logging.INFO

    return logging.CRITICAL


@cli.command()
@click.option("--render", is_flag=True, help="Render the game.")
@click.option("--timesteps", "-ts", default=None, help="Number of timesteps to test the game.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--log", is_flag=True, help="Log the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--ip", default="localhost", help="IP of the training server.")
@click.option("--port", default=5000, help="Port of the training server.")
@click.option("--features_path", default=None, type=click.Path(), help="Path of the ./features folder.")
@click.option("--model_path", default=None, type=click.Path(), help="Path of the model.")
@click.option("--alpha", "-a", default=0.001, help="Alpha of the training.")
def test(debug, render, ip, port, model_path, features_path, trainers_path, timesteps, iterations, info, log, alpha,
         features,
         scenarios,
         tags):
    # change start method to fork to avoid errors with multiprocessing
    # Windows does not support the fork start method
    if platform.system() != "Windows":
        set_start_method('fork')

    # if not timesteps and not iterations:
    #     print("You must choose a number of timesteps or iterations to test the game.")
    #     return
    #
    # if log:
    #     log = True
    # else:
    #     log = False
    #
    # logging_level = get_debug_level(debug, info)
    # logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)
    #
    # mode = TEST_MODE
    #
    # if timesteps:
    #     timesteps = int(timesteps)
    #
    # if iterations:
    #     iterations = int(iterations)
    #
    # if features:
    #     # Parse features list to list of str
    #     features = features.split(",")
    #     features = [f.strip() for f in features]
    #
    # if scenarios:
    #     # Parse scenarios list to list of str
    #     scenarios = scenarios.split(",")
    #     scenarios = [s.strip() for s in scenarios]
    #
    # if tags:
    #     # Parse tags list to list of str
    #     tags = tags.split(",")
    #     tags = [t.strip() for t in tags]
    #
    # communication_service = CommunicationServiceSocket(host='127.0.0.1')
    #
    # feature = Feature(name="PipeSizeDelta")
    # scenario = Scenario(feature=feature, name="0_100")
    # feature_strategy = DummyFeatureStrategy()
    # feature_strategy.retrieve_feature(features_path)
    #
    # test_runner = feature_strategy.build_test_runner(scenario=scenario, iterations=iterations, mode=TEST_MODE,
    #                                                  comm_service=communication_service)
    # test_runner.run(port=8081)
    #
    # trainer_manager = StableBaselinesTrainerManager(mode=TEST_MODE,
    #                                                 trainers_path=trainers_path)
    #
    # trainer = trainer_manager.create_trainer(test_runner, "PipeSizeTest", "scenario", observation_registry,
    #                                          action_registry,
    #                                          reward_registry, terminated_registry, config_registry)
    #
    # trainer.load(model_path)
    # trainer.play()


@cli.command()
@click.option("--tensorboard", "-tb", is_flag=True, help="Save logs to _logs folder to be use with the tensorboard.")
@click.option("--vectorize", "-v", is_flag=True, help="Vectorize the training.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--port", default=5000, help="Port of the training server.")
@click.option("--features_path", default=None, type=click.Path(), help="Path of the ./features folder.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--model", default=None, type=click.Path(),
              help="Path of the model to load if you want to use a base model for your training.")
def train(debug, steps_path, info, port, tensorboard, model, features_path, vectorize):
    # change start method to fork to avoid errors with multiprocessing
    # Windows does not support the fork start method
    if platform.system() != "Windows":
        set_start_method('fork')

    logging_level = get_debug_level(debug, info)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

    mode = TRAIN_MODE

    if vectorize:
        test_manager_class = VecRLTestManager
    else:
        test_manager_class = RLTestManager

    test_manager = test_manager_class(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path),
        mode=TRAIN_MODE,
        logging_level=logging_level,
        comm_service=CommunicationServiceRest(host="127.0.0.1", port=8080)
    )

    test_manager.test_all(features_path)
