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


def exec_registry_function(registry: Dict[str, List[Step]], game_context, scenario_name: str):
    return_value = {}
    for steps in registry.values():
        for step in steps:
            func = step.func
            if scenario_name in step.params:
                for params in step.params[scenario_name]:
                    result = func(game_context, **params)
                    return_value[step] = result
    return return_value




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
