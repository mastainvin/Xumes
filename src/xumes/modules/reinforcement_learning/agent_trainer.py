from abc import ABC
from typing import final, TypeVar

from xumes.modules.reinforcement_learning.i_trainer import ITrainer

from xumes.test_automation.given_script import TestStep, GivenScript

OBST = TypeVar("OBST")


class AgentTrainer(ITrainer, ABC):

    def __init__(self, agent):
        self.agent = agent
        self.given_script = None

    @final
    def get_reward(self):
        return self.agent.reward()

    @final
    def do_reset(self):
        self.agent.test_runner.reset()

    @final
    def episode_finished(self):
        return self.agent.test_runner.episode_finished()

    @final
    def get_terminated(self):
        return (self.agent.terminated() or self.agent.test_runner.game_state == "reset"
                or self.agent.test_runner.game_state == "random_reset")

    @final
    def get_obs(self) -> OBST:
        self.agent.test_runner.retrieve_state()
        return self.agent.observation()

    @final
    def push_actions_and_get_obs(self, actions) -> OBST:
        actions = self.agent.actions(actions)

        if isinstance(actions, TestStep):
            if self.given_script is None:
                self.given_script = GivenScript(self.agent.test_runner)
            self.given_script.clean()
            self.given_script.add_step(actions)
            self.given_script.execute()
        else:
            self.agent.test_runner.push_action_and_get_state(actions)

        return self.agent.observation()
