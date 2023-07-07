import sys
from typing import List
import logging

import stable_baselines3
from gymnasium import spaces
import numpy as np
from src.xumes.training_module import StableBaselinesTrainer, AutoEntityManager, JsonGameElementStateConverter, \
    CommunicationServiceTrainingMq


class ConnectedTrainingService(StableBaselinesTrainer):

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
        self.actions = ["nothing"]

    def convert_obs(self):
        return {
            'ball_pos': np.array([self.balls.pos_list]),
            'score': np.array([self.balls.score]),
            'highscore': np.array([self.balls.highscore]),
            'coins_x': np.array([self.coins.x]),
            'coins_y': np.array([self.coins.y]),
            'tiles_x': np.array([self.tiles.x]),
            'tiles_y': np.array([self.tiles.y]),
            'tiles_type': np.array([self.tiles.type]),
            'particle_x': np.array([self.particle.x]),
            'particle_y': np.array([self.particle.y])
        }

    def convert_reward(self) -> float:
        reward = 0

        if self.balls.pos_list < self.game.HEIGHT - 20:
            reward += 0.2
        if self.balls.score > self.score:
            reward += 5
            self.score = self.balls.score
        if self.balls.score >= self.balls.highscore:
            reward += 10
        if self.game.terminated:
            reward -= 5

        if self.tiles.y < self.balls.pos_list:
            reward += 10

        return reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        position = ["nothing", "space"]
        self.actions = [position[raws_actions[1]]]
        return self.actions

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    dct = {
        'ball_pos': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'score': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'highscore': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'coins_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'coins_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_type': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'particle_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'particle_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))

    }

    training_service = ConnectedTrainingService(
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




