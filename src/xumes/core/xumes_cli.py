import csv
import logging
import platform
from multiprocessing import set_start_method
from typing import List

import click
import shlex
import re


from xumes.core.modes import TRAIN_MODE, TEST_MODE
from xumes.modules.human.human_playing_test_manager import HumanPlayingTestManager
from xumes.test_runner.implementations.features_impl.gherkin_feature_strategy import GherkinFeatureStrategy
from xumes.test_runner.implementations.rest_impl.communication_service_rest import CommunicationServiceRest
from xumes.modules.reinforcement_learning.rl_test_manager import RLTestManager
from xumes.modules.reinforcement_learning.vec_rl_test_manager import VecRLTestManager


@click.group()
def cli():
    pass


def get_debug_level(debug, info):
    if debug:
        return logging.DEBUG
    if info:
        return logging.INFO

    return logging.CRITICAL


def split_names(names: str) -> List[str]:
    """
    Two cases:
        - names='a,b,c' -> ["a", "b", "c"]
        - names='"a, a","b, b","c, c"' -> ["a, a", "b, b", "c, c"]
    Args:
        names (str): A string of names separated by commas. If a name contains a comma, it should be enclosed in quotes.

    Returns:
        List[str]: The list of names
    """
    pattern = r'[^,\s][^,]*[^,\s]*|"[^"]*"'
    return [name.strip('"') for name in re.findall(pattern, names)]


@cli.command()
@click.option("--vectorize", "-v", is_flag=True, help="Vectorize the training.")
@click.option("--timesteps", "-ts", default=None, help="Number of timesteps to test the game.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--log", is_flag=True, help="Log the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--features_path", default=None, type=click.Path(), help="Path of the ./features folder.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--alpha", "-a", default=0.001, help="Alpha of the training.")
@click.option("--fps", default=-1, help="Limit of FPS.")
@click.option("--headless", is_flag=False, help="Run the game in headless mode.")
@click.option("-h", default=-1, help="Headless and fix FPS.")
def test(debug, features_path, steps_path, timesteps, iterations, info, log, alpha,
         features,
         scenarios,
         tags,
         vectorize,
         fps, headless, h):
    if iterations is not None:
        iterations = int(iterations)
    else:
        raise Exception("Number of iterations must be set")

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

    if h > 0:
        headless = True
        fps = h

    render = not headless

    test_manager = test_manager_class(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TEST_MODE,
        logging_level=logging_level,
        iterations=iterations,
        render=render,
        fps_limit=fps,
        comm_service=CommunicationServiceRest(host="127.0.0.1", port=8080)
    )

    test_manager.test_all(features_path)


@cli.command()
@click.option("--tensorboard", "-tb", is_flag=True, help="Save logs to _logs folder to be use with the tensorboard.")
@click.option("--vectorize", "-v", is_flag=True, help="Vectorize the training.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--features_path", default=None, type=click.Path(), help="Path of the ./features folder.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--model", default=None, type=click.Path(),
              help="Path of the model to load if you want to use a base model for your training.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--fps", default=-1, help="Limit of FPS.")
@click.option("--headless", is_flag=False, help="Run the game in headless mode.")
@click.option("-h", default=-1, help="Headless and fix FPS.")
def train(debug, steps_path, info, tensorboard, model, features_path, vectorize, features, scenarios, tags, fps,
          headless, h):
    # change start method to fork to avoid errors with multiprocessing
    # Windows does not support the fork start method
    if platform.system() != "Windows":
        set_start_method('fork')

    logging_level = get_debug_level(debug, info)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

    if vectorize:
        test_manager_class = VecRLTestManager
    else:
        test_manager_class = RLTestManager

    if h > 0:
        headless = True
        fps = h


    render = not headless

    test_manager = test_manager_class(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TRAIN_MODE,
        logging_level=logging_level,
        render=render,
        fps_limit=fps,
        comm_service=CommunicationServiceRest(host="127.0.0.1", port=8080)
    )

    test_manager.test_all(features_path)


@cli.command()
@click.option("--timesteps", "-ts", default=None, help="Number of timesteps to test the game.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--log", is_flag=True, help="Log the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--features_path", default=None, type=click.Path(), help="Path of the ./features folder.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
def play(debug, features_path, steps_path, timesteps, iterations, info, log,
         features,
         scenarios,
         tags):
    if iterations is not None:
        iterations = int(iterations)
    else:
        raise Exception("Number of iterations must be set")

    # change start method to fork to avoid errors with multiprocessing
    # Windows does not support the fork start method
    if platform.system() != "Windows":
        set_start_method('fork')

    logging_level = get_debug_level(debug, info)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

    mode = TRAIN_MODE

    test_manager = HumanPlayingTestManager(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TEST_MODE,
        logging_level=logging_level,
        iterations=iterations,
        render=True,
        comm_service=CommunicationServiceRest(host="127.0.0.1", port=8080)
    )

    test_manager.test_all(features_path)
