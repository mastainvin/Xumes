import logging
import os

import click

from xumes.core.modes import TRAIN_MODE, TEST_MODE, RENDER_MODE, FEATURE_MODE, SCENARIO_MODE
from xumes.game_module.implementations import CommunicationServiceTestManagerRestApi
from xumes.game_module.implementations.features_impl.basic_feature_strategy import BasicFeatureStrategy
from xumes.game_module.test_manager import PygameTestManager
from xumes.training_module import VecStableBaselinesTrainerManager, StableBaselinesTrainerManager
from xumes.training_module.implementations.rest_impl.communication_service_trainer_manager_rest_api import \
    CommunicationServiceTrainerManagerRestApi


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
@click.option("--test", is_flag=True, help="Test mode.")
@click.option("--train", is_flag=True, help="Train mode.")
@click.option("--timesteps", "-t", default=None, help="Number of timesteps to test the game.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--ip", default="localhost", help="IP of the training server.")
@click.option("--port", default=5000, help="Port of the training server.")
@click.option("--path", default=None, type=click.Path(), help="Path of the ./tests folder.")
def tester(train, debug, render, test, ip, port, path, timesteps, iterations, info):
    if path:
        os.chdir(path)
    else:
        print("You must choose a path to save the model.")
        return

    if not train and not test:
        print("You must choose between --train or --test.")
        return

    if test and not timesteps and not iterations:
        print("You must choose a number of timesteps or iterations to test the game.")
        return

    logging.basicConfig(format='%(levelname)s:%(message)s', level=get_debug_level(debug, info))

    if train:
        mode = TRAIN_MODE
    else:
        mode = TEST_MODE
    if render:
        mode = RENDER_MODE

    if timesteps:
        timesteps = int(timesteps)

    if iterations:
        iterations = int(iterations)

    test_manager = PygameTestManager(communication_service=CommunicationServiceTestManagerRestApi(ip=ip, port=port),
                                     feature_strategy=BasicFeatureStrategy(),
                                     mode=mode, timesteps=timesteps, iterations=iterations)
    test_manager.test_all()


@cli.command()
@click.option("--test", is_flag=True, help="Test mode")
@click.option("--train", is_flag=True, help="Train mode.")
@click.option("--mode", default=FEATURE_MODE, help="Mode of the training. (scenario, feature=default)")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--port", default=5000, help="Port of the training server.")
@click.option("--path", default=None, type=click.Path(), help="Path of the ./trainers folder.")
def trainer(train, debug, test, path, mode, port, info):
    if path:
        os.chdir(path)
    if not path:
        print("You must choose a path to save the model.")
        return

    logging.basicConfig(format='%(levelname)s:%(message)s', level=get_debug_level(debug, info))

    if not train and not test:
        print("You must choose between --train or --test.")
        return

    if mode == "scenario":
        model_mode = SCENARIO_MODE
    else:
        model_mode = FEATURE_MODE

    if train:
        mode = TRAIN_MODE
    else:
        mode = TEST_MODE

    training_manager = None

    if model_mode == FEATURE_MODE:
        training_manager = VecStableBaselinesTrainerManager(CommunicationServiceTrainerManagerRestApi(), port,
                                                            mode=mode)
    elif model_mode == SCENARIO_MODE:
        training_manager = StableBaselinesTrainerManager(CommunicationServiceTrainerManagerRestApi(), mode=mode)

    if training_manager is not None:
        training_manager.run_communication_service()
    else:
        print("You must choose a valid mode.")
        return
