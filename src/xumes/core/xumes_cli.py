import logging
import platform
from multiprocessing import set_start_method
from typing import List

import click
import re

from xumes.core.modes import TRAIN_MODE, TEST_MODE
from xumes.core.parameters_registry import ParametersRegistry
from xumes.modules.human.human_playing_test_manager import HumanPlayingTestManager
from xumes.modules.imitation_learning.collector_test_manager import CollectorTestManager
from xumes.modules.imitation_learning.vec_imitator_test_manager import VecImitatorTestManager
from xumes.test_automation.episode_control import UserControlledEpisodeControlFactory
from xumes.test_automation.implementations.features_impl.gherkin_feature_strategy import GherkinFeatureStrategy
from xumes.communication.implementations.rest_impl.com_game_engine_rest import ComGameEngineRest
from xumes.test_automation.implementations.test_manager.parallel_test_manager import ParallelTestManager
from xumes.modules.reinforcement_learning.vec_rl_test_manager import VecRLTestManager
from xumes.test_automation.test_manager import DummyTestManager


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
        - names='"a"' -> ["a"]
    Args:
        names (str): A string of names separated by commas. If a name contains a comma, it should be enclosed in quotes.

    Returns:
        List[str]: The list of names
    """
    pattern = r'[^,\s][^,]*[^,\s]*|"[^"]*"'
    return [name.strip('"') for name in re.findall(pattern, names)]


@cli.command()
@click.argument("features_path", type=click.Path(), required=False)
@click.option("--not_vectorize", "-nv", is_flag=True, help="Vectorize the training.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--log", is_flag=True, help="Log the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--alpha", "-a", default=0.001, help="Alpha of the training.")
@click.option("--fps", default=-1, help="Limit of FPS.")
@click.option("--headless", is_flag=False, help="Run the game in headless mode.")
@click.option("-h", default=-1, help="Headless and fix FPS.")
def test(debug, features_path, steps_path, iterations, info, log, alpha,
         features,
         scenarios,
         tags,
         not_vectorize,
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

    if not_vectorize is not None:
        if not not_vectorize:
            test_manager_class = VecRLTestManager
        else:
            test_manager_class = ParallelTestManager
    else:
        test_manager_class = VecRLTestManager

    if h > 0:
        headless = True
        fps = h

    render = not headless

    if features is not None:
        features = split_names(features)

    if scenarios is not None:
        scenarios = split_names(scenarios)

    test_manager = test_manager_class(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_path=features_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TEST_MODE,
        logging_level=logging_level,
        iterations=iterations,
        render=render,
        fps_limit=fps,
        comm_service=ComGameEngineRest(host="127.0.0.1", port=8080)
    )

    params = ParametersRegistry()
    params.register("alpha", alpha)
    params.register("iterations", iterations)
    params.register("features", features)
    params.register("scenarios", scenarios)
    params.register("tags", tags)
    params.register("log", log)
    params.register("headless", headless)
    params.register("features_path", features_path)
    params.register("steps_path", steps_path)
    params.register("alpha", alpha)
    params.register("fps", fps)
    params.register("not_vectorize", not_vectorize)

    test_manager.test_all(features_path)


@cli.command()
@click.argument("features_path", type=click.Path(), required=False)
@click.option("--tensorboard", "-tb", is_flag=True, help="Save logs to _logs folder to be use with the tensorboard.")
@click.option("--not_vectorize", "-nv", is_flag=True, help="Vectorize the training.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--model", default=None, type=click.Path(),
              help="Path of the model to load if you want to use a base model for your training.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--fps", default=-1, help="Limit of FPS.")
@click.option("--headless", is_flag=False, help="Run the game in headless mode.")
@click.option("-h", default=-1, help="Headless and fix FPS.")
@click.option("--imitate", is_flag=True, help="Train the model with imitation learning.")
def train(debug, steps_path, info, tensorboard, model, features_path, not_vectorize, features, scenarios, tags, fps,
          headless, h, imitate):
    # change start method to fork to avoid errors with multiprocessing
    # Windows does not support the fork start method
    if platform.system() != "Windows":
        set_start_method('fork')

    logging_level = get_debug_level(debug, info)
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)

    if imitate:
        test_manager_class = VecImitatorTestManager
    else:
        if not_vectorize is not None:
            if not not_vectorize:
                test_manager_class = VecRLTestManager
            else:
                test_manager_class = ParallelTestManager
        else:
            test_manager_class = VecRLTestManager

    if h > 0:
        headless = True
        fps = h

    render = not headless

    if features is not None:
        features = split_names(features)

    if scenarios is not None:
        scenarios = split_names(scenarios)

    test_manager = test_manager_class(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_path=features_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TRAIN_MODE,
        logging_level=logging_level,
        render=render,
        fps_limit=fps,
        do_logs=tensorboard,
        comm_service=ComGameEngineRest(host="127.0.0.1", port=8080)
    )

    params = ParametersRegistry()
    params.register("tensorboard", tensorboard)
    params.register("not_vectorize", not_vectorize)
    params.register("features_path", features_path)
    params.register("steps_path", steps_path)
    params.register("model", model)
    params.register("features", features)
    params.register("scenarios", scenarios)
    params.register("tags", tags)
    params.register("fps", fps)
    params.register("headless", headless)

    test_manager.test_all(features_path)


@cli.command()
@click.argument("features_path", type=click.Path(), required=False)
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--episode_length", "-el", default=None, help="Number of steps per episode.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--log", is_flag=True, help="Log the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--fps", default=-1, help="Limit of FPS.")
def play(debug, features_path, steps_path, iterations, info, log,
         features,
         scenarios,
         tags,
         episode_length, fps):
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

    if features is not None:
        features = split_names(features)

    if scenarios is not None:
        scenarios = split_names(scenarios)

    test_manager = HumanPlayingTestManager(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_path=features_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TEST_MODE,
        logging_level=logging_level,
        iterations=iterations,
        render=True,
        fps_limit=fps,
        comm_service=ComGameEngineRest(host="127.0.0.1", port=8080)
    )

    params = ParametersRegistry()
    params.register("iterations", iterations)
    params.register("features", features)
    params.register("scenarios", scenarios)
    params.register("tags", tags)
    params.register("log", log)
    params.register("features_path", features_path)
    params.register("steps_path", steps_path)
    params.register("episode_length", episode_length)

    test_manager.test_all(features_path)


@cli.command()
@click.argument("features_path", type=click.Path(), required=False)
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
def list(features, scenarios, tags, features_path="./", steps_path="./"):
    if features is not None:
        features = split_names(features)

    if scenarios is not None:
        scenarios = split_names(scenarios)
    test_manager = DummyTestManager(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path, features_names=features,
                                                features_path=features_path,
                                                scenarios_names=scenarios, tags=tags),
        comm_service=ComGameEngineRest(host="127.0.0.1", port=8080))

    test_manager.list_features(features_path)


@cli.command()
@click.argument("features_path", type=click.Path(), required=False)
@click.option("--episode_length", "-el", default=None, help="Number of steps per episode.")
@click.option("--iterations", "-i", default=None, help="Number of iterations to test the game.")
@click.option("--features", "-f", default=None, help="List of features to test.")
@click.option("--scenarios", "-s", default=None, help="List of scenarios to test.")
@click.option("--tags", default=None, help="Tags of the features to test.")
@click.option("--log", is_flag=True, help="Log the game.")
@click.option("--debug", is_flag=True, help="Debug debug level.")
@click.option("--info", is_flag=True, help="Info debug level.")
@click.option("--steps_path", default=None, type=click.Path(), help="Path of the ./steps folder.")
@click.option("--clean", is_flag=True, help="Clean the data.")
def collect(debug, features_path, steps_path, iterations, info, log,
            features,
            scenarios,
            tags,
            clean, episode_length):
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

    if features is not None:
        features = split_names(features)

    if scenarios is not None:
        scenarios = split_names(scenarios)

    test_manager = CollectorTestManager(
        feature_strategy=GherkinFeatureStrategy(steps_path=steps_path,
                                                features_path=features_path,
                                                features_names=features,
                                                scenarios_names=scenarios,
                                                tags=tags),
        mode=TEST_MODE,
        logging_level=logging_level,
        iterations=iterations,
        render=True,
        comm_service=ComGameEngineRest(host="127.0.0.1", port=8080),
        episode_control_factory=UserControlledEpisodeControlFactory(),
    )

    params = ParametersRegistry()
    params.register("iterations", iterations)
    params.register("features", features)
    params.register("scenarios", scenarios)
    params.register("tags", tags)
    params.register("log", log)
    params.register("features_path", features_path)
    params.register("steps_path", steps_path)
    params.register("clean", clean)
    params.register("episode_length", episode_length)

    test_manager.test_all(features_path)
