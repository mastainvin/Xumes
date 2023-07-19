import logging
import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces

from games_examples.dont_touch.src.config import Config

from src.xumes.training_module import StableBaselinesTrainer, JsonGameElementStateConverter, \
                                        CommunicationServiceTrainingMq, AutoEntityManager


class DontTouchTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager,
                 communication_service,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm, random_reset_rate):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm, random_reset_rate)

        self.score = 0
        self.actions = ["nothing", "nothing"]

    def convert_obs(self):

        return {
            'player_x': np.array([self.player.player_position[0]]),
            'player_y': np.array([self.player.player_position[1]]),
            'left_hand_x': np.array([self.left_hand.new_x]),
            'left_hand_y': np.array([self.left_hand.new_y]),
            'left_hand_speed': np.array([self.left_hand.new_spd]),
            'right_hand_x': np.array([self.right_hand.new_x]),
            'right_hand_y': np.array([self.right_hand.new_y]),
            'right_hand_speed': np.array([self.right_hand.new_spd]),
            'scoreboard_current_score': np.array([self.scoreboard._current_score]),
            'scoreboard_max_score': np.array([self.scoreboard._max_score])
        }

    def convert_reward(self) -> float:
        reward = 0

        if self.player.player_position[1] < Config.HEIGHT - 20:
            reward += 0.2
        if self.scoreboard._current_score > self.score:
            reward += 5
            self.score = self.scoreboard._current_score
        if self.scoreboard._current_score >= self.scoreboard._max_score:
            reward += 10
        if self.game.terminated:
            reward -= 5

        if self.left_hand.new_y > self.right_hand.new_y:
            if self.left_hand.new_x < self.player.player_position[0]:
                if self.right_hand.new_spd > self.left_hand.new_spd:
                    if self.player.player_position[1] > self.left_hand.new_y:
                        reward += 0.2
                else:
                    reward += 0.1
        else:
            if self.right_hand.new_x > self.player.player_position[0]:
                if self.left_hand.new_spd > self.right_hand.new_spd:
                    if self.player.player_position[1] > self.right_hand.new_y:
                        reward += 0.2
                else:
                    reward += 0.1

        return reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        direction = ["nothing", "left", "right"]
        position = ["nothing", "up", "down"]
        self.actions = [direction[raws_actions[0]], position[raws_actions[1]]]
        # need to be changed into :
        # direction = ["nothing", "left", "right", "up", "down"]
        # self.actions = [direction[raws_actions[0]]]
        # but if I do so, self.actions only choose from the first 3 choices in direction
        # for the former example, the line:
        # direction = ["nothing", "left", "right", "up", "down"]
        # is seen as
        # direction = ["nothing", "left", "right"]
        return self.actions


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    dct = {
        'player_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'player_y' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'left_hand_x' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'left_hand_y' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'left_hand_speed' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_x' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_y' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_speed' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'scoreboard_current_score' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'scoreboard_max_score' : spaces.Box(-1, 1, dtype=np.float32, shape=(1,))

    }

    training_service = DontTouchTrainingService(
        entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(dct),
        action_space=spaces.MultiDiscrete([3, 3]),
        max_episode_length=2000,
        total_timesteps=200000,
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO,
        random_reset_rate=0.0
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            training_service.train(save_path="./models", log_path="./logs", test_name="test")
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/best_model.zip")
            training_service.play(100000)




