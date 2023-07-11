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


    def convert_obs(self):


        return {
            'dist_coin_x': np.array([self.game.ball.rect.x - self.game.coin.x ]),
            'dist_coin_y': np.array([self.game.ball.rect.y - self.game.coin.y]),
            'dist_tiles_x': np.array([self.game.ball.rect.x - self.game.t.x]),
            'dist_tiles_y': np.array([self.game.ball.rect.y - self.game.t.y]),
            'tiles_type': np.array([self.game.t.type])

        }

    def convert_reward(self) -> float:
        #reward = 0

        #if self.game.ball.score > self.score :
            #reward += 5
            #self.score = self.game.ball.score

        #if self.game.ball.score > self.game.ball.highscore:
            #reward += 8

        #if self.game.terminated:
            #reward -= 10

        #return reward

        if self.game.terminated:
            self.score = 0
            return -1

        if self.game.ball.score > self.score:
            self.score = self.game.ball.score
            return 1
        else:
            return 0.1

    def convert_terminated(self) -> bool:
        if self.game.terminated:
            self.score = 0
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        if raws_actions == 1:
            return ["space"]
        return ["nothing"]

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    dct = {

        'dist_coin_x':spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'dist_coin_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'dist_tiles_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'dist_tiles_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_type': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))

    }

    training_service = ConnectedTrainingService(
        entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(dct),
        action_space=spaces.Discrete(2),
        max_episode_length=20000,
        total_timesteps=100000,
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




