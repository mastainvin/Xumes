import logging
import os
import pickle

import pygame

from xumes import Script, Imitator, Agent, Imitable
from xumes.core.parameters_registry import ParametersRegistry
from xumes.test_automation.behavior import Behavior
from xumes.test_automation.episode_control import UserControlledEpisodeControl
from xumes.test_automation.test_manager import TestManager


class CollectorScript(Script):

    def __init__(self, imitator: Imitator, path: str, collector, screen, scenario):
        super().__init__()
        self._imitator = imitator
        self._screen = None
        self._episode_data = []
        self._path = path
        self._collector = collector
        self._number_of_episode = 0
        self._count = 0
        self._screen = screen
        self._scenario = scenario
        self._font = pygame.font.Font(None, 36)

        self._pause = False

        self._observation = None

        self._keep_episode = True

        self._episode_length = (ParametersRegistry()).get("episode_length")
        if self._episode_length is None:
            self._episode_length = None
        else:
            self._episode_length = int(self._episode_length)

    def reset(self):
        """
            Reset the environment
        """
        super().reset()
        self._test_runner.retrieve_state()
        self._observation = self.get_observation()

    def step(self):
        """
            Collect the data from the human tester using pygame with a pygame window
        """

        self._count += 1

        self.draw()

        action = None
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pass

        self.wait_pause(keys)

        action = self._imitator.convert_input(keys)
        new_observation = self.get_observation()
        reward = self.get_reward()
        terminated = self._imitator.terminated()

        self._episode_data.append((self._observation, action, reward, new_observation, terminated))

        self._observation = new_observation

        return self._imitator.agent.actions(action)

    def wait_pause(self, keys):
        if keys[pygame.K_ESCAPE]:
            while True:
                for event in pygame.event.get():
                    pass
                keys = pygame.key.get_pressed()
                self.draw_pause()
                if keys[pygame.K_RETURN]:
                    break

    def wait_episode_end(self) -> bool:
        while True:
            for event in pygame.event.get():
                pass
            keys = pygame.key.get_pressed()
            self.draw_episode_end()
            if keys[pygame.K_RETURN]:
                return True
            if keys[pygame.K_BACKSPACE]:
                return False

    def draw(self):
        self._screen.fill((0, 0, 0))  # Fill the screen with black
        self.draw_count()
        self.draw_title()
        self.draw_number_of_episode()
        self.draw_feature_name()
        self.draw_scenario_name()
        self.draw_echap_to_pause()
        pygame.display.flip()  # Update the full display surface to the screen

    def draw_pause(self):
        self._screen.fill((0, 0, 0))  # Fill the screen with black
        self.draw_echap_to_unpause()
        pygame.display.flip()  # Update the full display surface to the screen

    def get_observation(self):
        """
            Get the observation from the environment
        """
        return self._imitator.agent.observation()

    def get_reward(self):
        """
            Get the reward from the environment
        """
        return self._imitator.agent.reward()

    def terminated(self) -> bool:
        terminated = self._imitator.terminated()

        if terminated:

            if self.wait_episode_end():
                self._number_of_episode += 1
                self._collector.append(self._episode_data)
            else:
                assert isinstance(self._test_runner.episode_control, UserControlledEpisodeControl)
                self.test_runner.episode_control.decrement_test()

            self._episode_data = []

            self._count = 0

        return self._imitator.terminated()

    def draw_count(self):
        text = self._font.render(f"Episode length: {self._count}", True, (255, 255, 255))
        self._screen.blit(text, (20, 50))

    def draw_title(self):
        text = self._font.render("Data Collection in Progress", True, (255, 255, 255))
        self._screen.blit(text, (20, 20))  # Display the text

    def draw_number_of_episode(self):
        text = self._font.render(f"Number of episodes: {self._number_of_episode}", True, (255, 255, 255))
        self._screen.blit(text, (20, 80))

    def draw_feature_name(self):
        text = self._font.render(f"Feature: {self._scenario.feature.name}", True, (255, 255, 255))
        self._screen.blit(text, (20, 110))

    def draw_scenario_name(self):
        text = self._font.render(f"Scenario: {self._scenario.name}", True, (255, 255, 255))
        self._screen.blit(text, (20, 140))

    def draw_echap_to_pause(self):
        text = self._font.render("Press Echap to pause", True, (255, 255, 255))
        self._screen.blit(text, (20, 170))

    def draw_echap_to_unpause(self):
        text = self._font.render("Press Enter to unpause", True, (255, 255, 255))
        self._screen.blit(text, (20, 20))

    def draw_episode_end(self):
        # Enter if the user wants to keep the episode
        # or delete if the user wants to discard the episode
        self._screen.fill((0, 0, 0))  # Fill the screen with black
        text = self._font.render("Press Enter to keep the episode or Delete to discard it", True, (255, 255, 255))
        self._screen.blit(text, (20, 20))  # Display the text
        pygame.display.flip()


def init_pygame():
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Adjust window size
    pygame.display.set_caption("Data Collection Game")  # Set window title
    clock = pygame.time.Clock()

    return screen, clock


def wait_start(screen):
    # Wait for user to tap on enter key to start the data collection
    font = pygame.font.Font(None, 36)
    while True:
        # draw message on screen
        screen.fill((0, 0, 0))  # Fill the screen with black
        text = font.render("Press Enter to start data collection", True, (255, 255, 255))
        screen.blit(text, (20, 20))  # Display the text
        pygame.display.flip()  # Update the full display surface to the screen
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


class CollectorTestManager(TestManager):

    def _run_scenarios(self, feature, scenario_datas, active_processes):
        reversed_scenario_datas = list(scenario_datas.keys())

        screen, clock = init_pygame()
        collector = []

        path = None

        for scenario in reversed_scenario_datas:
            feature = scenario.feature
            test_runner = scenario_datas[scenario].test_runner

            when_result = test_runner.when()
            if len(when_result) > 1:
                raise Exception("Only one when step is allowed")

            behavior: Behavior = when_result[next(iter(when_result))]

            if not isinstance(behavior, (Agent, Imitable)):
                raise Exception("Only Imitable Agent is allowed")

            agent: Agent = behavior
            agent.set_test_runner(test_runner)
            agent.set_mode(self._mode)

            imitable: Imitable = behavior
            imitator = imitable.imitator()

            imitator.set_agent(agent)
            imitator.set_mode(self._mode)
            imitator.set_test_runner(test_runner)

            if not path:
                path = imitator.path + "/collected_data.pkl"

            collector_script = CollectorScript(imitator, path, collector, screen, scenario)
            collector_script.set_mode(self._mode)
            collector_script.set_test_runner(test_runner)
            collector_script.set_do_logging(self.do_logs)

            # Wait for user to tap on enter key to start the data collection
            wait_start(screen)

            collector_script.execute(scenario.feature, scenario)

        existing_data = []

        clean = ParametersRegistry()["clean"]
        if not clean:
            try:
                # Read existing data
                with open(path, "rb") as f:
                    existing_data = pickle.load(f)
            except (EOFError, FileNotFoundError):
                logging.error("No existing data found")

        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Add new episode data
        existing_data.extend(collector)

        # Write updated data back to file
        with open(path, "wb") as f:
            pickle.dump(existing_data, f)
