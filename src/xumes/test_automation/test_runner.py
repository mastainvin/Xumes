import logging
from typing import TypeVar, final

from xumes.assertions.assertion_bucket import AssertionBucket
from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.core.modes import TEST_MODE
from xumes.core.registry import exec_registry_function
from xumes.entity.entity_manager import AutoEntityManager
from xumes.entity.implementations.json_impl.json_game_element_state_converter import \
    JsonGameElementStateConverter
from xumes.test_automation.driver import Driver
from xumes.test_automation.game_instance_service import GameInstanceService
from xumes.test_automation.test_context import TestContext

OBST = TypeVar("OBST")


class TestRunner:
    """
    The `TestRunner` class is a central component of Xumes. It manages communication between communication service,
    the execution of the game itself, and external events that can modify the game state.
    """

    def __init__(self, game_instance_service: GameInstanceService, number_max_of_steps: int = None,
                 number_max_of_tests: int = None,
                 mode: str = TEST_MODE, feature_name: str = None,
                 scenario_name: str = None, test_queue=None, steps=None, registry_queue=None):
        """
        The constructor for the GameService class.
        """
        self._game_instance_service: GameInstanceService = game_instance_service
        self._feature = feature_name
        self._scenario = scenario_name
        self._mode = mode
        self._number_of_steps = 0
        self._number_max_of_steps = number_max_of_steps
        self._number_of_tests = 0
        self._number_max_of_tests = number_max_of_tests
        self._steps = steps
        self._entity_manager = AutoEntityManager(JsonGameElementStateConverter())

        self._assertion_bucket = AssertionBucket(test_name=f"{self._feature}/{self._scenario}",
                                                 queue=test_queue)
        self.driver = Driver()

        self._config_registry, self._given_registry, self._when_registry, self._then_registry = registry_queue.get()

        self._context = TestContext(self._entity_manager, self.driver, self._assertion_bucket)

    def get_context(self):
        return self._context

    def run(self, port):
        self._game_instance_service.run(port)

    def config(self):
        self._config_registry[self._steps](self)
        return self.driver()

    def given(self):
        exec_registry_function(registry=self._given_registry[self._steps], game_context=self._context,
                               scenario_name=self._scenario)

    def when(self):
        return exec_registry_function(registry=self._when_registry[self._steps], game_context=self._context,
                                      scenario_name=self._scenario)

    def then(self):
        return exec_registry_function(registry=self._then_registry[self._steps], game_context=self._context,
                                      scenario_name=self._scenario)

    def episode_finished(self) -> bool:
        # when an episode is finished, we collect the assertions
        if self._mode == TEST_MODE:
            if self._number_of_tests >= self._number_max_of_tests:
                self._do_assert()
                raise RunningEndsError
            else:
                try:
                    self.then()
                    self._assertion_bucket.reset_iterator()
                except KeyError:
                    pass
            self._number_of_tests += 1

        return True

    def _do_assert(self) -> None:
        self._assertion_bucket.assertion_mode()
        self.then()
        self._assertion_bucket.send_results()
        self._assertion_bucket.clear()
        self._assertion_bucket.collect_mode()

    @final
    def reset(self):
        """
        Resets the game state by calling the given and reset methods of the TestRunner instance.
        """
        self.given()
        self._game_instance_service.reset()

    @final
    def push_action_and_get_state(self, actions):
        """
        Pushes actions to the TestRunner and retrieves the game state.

        Parameters:
            actions: The actions to be pushed to the TestRunner.
        """
        logging.debug(f"Pushing actions: {actions}")
        methods = self.driver()
        states = self._game_instance_service.push_actions_and_get_state(actions, methods)
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._entity_manager.convert(state)

    @final
    def finished(self):
        """
        Checks if the game has finished by calling the finish method of the TestRunner instance.

        Returns:
            bool: True if the game has finished, False otherwise.
        """
        return self._game_instance_service.finish()

    @final
    def retrieve_state(self) -> None:
        """
        Retrieves the game state by calling the get_state method of the TestRunner instance.
        """
        # self._test_runner.run_loop()
        states = self._game_instance_service.get_state()
        logging.debug(f"Received states: {states}")
        for state in states.items():
            self._entity_manager.convert(state)

    @final
    @property
    def game_state(self):
        """
        Retrieves the game state by calling the get_entity_manager method of the TestRunner instance.

        Returns:
            The current game state.
        """
        return self._entity_manager

    @final
    def get_entity(self, name):
        return self._entity_manager.get(name)
