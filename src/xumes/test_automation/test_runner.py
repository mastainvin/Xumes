import logging
import time
from typing import TypeVar, final

from xumes.assertions.assertion_bucket import AssertionBucket, AssertionBucketTrain
from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.core.modes import TEST_MODE, TRAIN_MODE
from xumes.core.parameters_registry import ParametersRegistry
from xumes.core.registry import exec_registry_function
from xumes.entity.entity_manager import AutoEntityManager
from xumes.entity.implementations.json_impl.json_game_element_state_converter import \
    JsonGameElementStateConverter
from xumes.test_automation.driver import Driver
from xumes.test_automation.episode_control import EpisodeControl, DefaultEpisodeControl
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
                 scenario_name: str = None, test_queue=None, steps=None, registry_queue=None,
                 episode_control: EpisodeControl = None):
        """
        The constructor for the GameService class.
        """
        self._game_instance_service: GameInstanceService = game_instance_service
        self._feature = feature_name
        self._scenario = scenario_name
        self._mode = mode
        self._number_of_steps = 0
        self._number_max_of_steps = number_max_of_steps
        self._number_of_tests = 1
        self._number_max_of_tests = number_max_of_tests
        self._steps = steps
        self._entity_manager = AutoEntityManager(JsonGameElementStateConverter())

        if self._mode == TEST_MODE:
            self._assertion_bucket = AssertionBucket(test_name=f"{self._scenario}",
                                                     class_name=self._feature,
                                                     queue=test_queue)
        else:
            self._assertion_bucket = AssertionBucketTrain(test_name=f"{self._scenario}",
                                                          class_name=self._feature,
                                                          queue=test_queue)

        self.driver = Driver()

        self._config_registry, self._given_registry, self._when_registry, self._then_registry = registry_queue.get()

        self._context = TestContext(self._entity_manager, self.driver, self._assertion_bucket)

        if episode_control is None:
            self._episode_control = DefaultEpisodeControl(self._number_max_of_steps, self._number_max_of_tests)
        else:
            self._episode_control = episode_control

        self._test_start_time = 0.0

        self._test_result = False

        params = ParametersRegistry()
        self._do_tensorboard_logs = params.get("tensorboard")

        self._successes = 0
        self._nb_episode = 0

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
            try:
                self.then()
            except KeyError:
                pass

            self._test_result = self._assertion_bucket.to_next_episode()

            self._episode_control.increment_test()
            if not self._episode_control.should_continue(self._test_result):
                self._do_assert()
                raise RunningEndsError
        elif self._mode == TRAIN_MODE and self._do_tensorboard_logs:
                self.then()
                self._test_result = self._assertion_bucket.to_next_episode()
                if self._test_result:
                    self._successes += 1
                self._nb_episode += 1

        return False

    def success_ratio(self):
        rate = self._successes / self._nb_episode
        if rate >= 0.1:
            rate = 1
        return rate

    def reset_ratio(self):
        self._successes = 0
        self._nb_episode = 0

    def test_passed(self):
        return self._test_result

    @property
    def episode_control(self):
        return self._episode_control

    def _do_assert(self) -> None:
        test_time_end = time.time()
        test_time = round(test_time_end - self._test_start_time, 3)
        self._assertion_bucket.send_results(test_time)
        self._assertion_bucket.clear()

    @final
    def reset(self):
        """
        Resets the game state by calling the given and reset methods of the TestRunner instance.
        """
        if self._test_start_time == 0.0:
            self._test_start_time = time.time()
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
