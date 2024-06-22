from abc import ABC
from typing import final, TypeVar

from xumes.modules.reinforcement_learning.i_trainer import ITrainer

OBST = TypeVar("OBST")


class AgentTrainer(ITrainer, ABC):

    def __init__(self, agent):
        self.agent = agent

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
        self.agent.test_runner.push_action_and_get_state(self.agent.actions(actions))
        return self.agent.observation()
