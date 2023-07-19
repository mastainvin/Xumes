import inspect
import os
from typing import List, Dict

from xumes.core.step import Step

import inspect
import os
import dill


def create_registry_content():
    registry = {}

    def registrar(content: str):
        def decorator(func):
            file_path = inspect.getsourcefile(func)
            file_name = os.path.basename(file_path[:-3])
            if file_name not in registry:
                registry[file_name] = [Step(func, content)]
            else:
                registry[file_name].append(Step(func, content))
            return func

        return decorator

    registrar.all = registry
    return registrar


def exec_registry_function(registry: List[Step], game_context, scenario_name: str):
    """
    Execute all functions from registry
    :param scenario_name:
    :param registry:  of functions
    :param game_context: where the functions will be executed
    """
    for r in registry:
        r.func(game_context, **r.params[scenario_name])


def get_content_from_registry(registry: List[Step]):
    """
    Get all content from registry
    :param registry:  we want to get the content
    """
    return [step.content for step in registry]


def create_registry():
    registry = {}

    def registrar(func):
        file_path = inspect.getsourcefile(func)
        file_name = os.path.basename(file_path[:-3])
        registry[file_name] = func
        return func

    registrar.all = registry
    return registrar
