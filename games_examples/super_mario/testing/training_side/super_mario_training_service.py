import logging
import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces
from games_examples.super_mario.classes.Level import nb_entites

from xumes.trainer import StableBaselinesTrainer, JsonGameElementStateConverter, CommunicationServiceTrainingMq, AutoEntityManager


class SuperMarioTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager,
                 communication_service,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm,
                 random_reset_rate: float):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm, random_reset_rate)

        self.player_x, self.coins, self.points, self.player_state = 0, 0, 0, 0
        self.actions = ["nothing", "nothing"]

    def convert_obs(self):

        dct = {
            'mario_rect': np.array([self.mario.rect]),
            'mario_powerUpState': np.array([self.mario.powerUpState]),
            'ending_level': np.array([self.mario.ending_level]),
            'dashboard_coins': np.array([self.mario.dashboard.coins]),
            'dashboard_points': np.array([self.mario.dashboard.points]),
        }

        for idx, entity in enumerate(self.mario.levelObj.entityList):
            dct[f'entity_{idx}_name'] = np.array([entity.name])
            dct[f'entity_{idx}_type'] = np.array([entity.type])
            dct[f'entity_{idx}_position'] = np.array([entity.position.x, entity.position.y])
            dct[f'entity_{idx}_alive'] = np.array([entity.alive])
            dct[f'entity_{idx}_active'] = np.array([entity.active])
            dct[f'entity_{idx}_bouncing'] = np.array([entity.bouncing])
            dct[f'entity_{idx}_onGround'] = np.array([entity.onGround])

        return dct

    def convert_reward(self):

        reward = 0

        if self.mario.dashboard.coins > self.coins:
            reward += 0.6
        if self.mario.dashboard.points > self.points:
            reward += 0.5
        if self.game.terminated or (self.player_state > self.mario.powerUpState):
            reward -= 5
        if self.ending_level:
            reward += 5

        xDiff = self.mario.rect[0] - self.player_x
        if xDiff >= 8:
            reward += 1
        elif xDiff > 0:
            reward += 0.5
        elif xDiff >= -8:
            reward -= 1.0
        else:
            reward -= 1.5

        return reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raw_actions):
        #print(raw_actions)
        moves = [["nothing", "space"], ["nothing", "up"], ["nothing", "left"], ["nothing", "right"]]
        return [moves[0][int(raw_actions[0])], moves[1][int(raw_actions[1])],
                moves[2][int(raw_actions[2])], moves[3][int(raw_actions[3])]]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    dct = {
        'mario_rect': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'mario_powerUpState': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'ending_level': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_coins': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_points': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
    }

    for idx in range(nb_entites):
        dct[f'entity_{idx}_name'] = spaces.Discrete(10)
        dct[f'entity_{idx}_type'] = spaces.Discrete(3)
        dct[f'entity_{idx}_position'] = spaces.Box(low=0, high=1, shape=(2,), dtype=np.float32)
        dct[f'entity_{idx}_alive'] = spaces.Discrete(2)
        dct[f'entity_{idx}_active'] = spaces.Discrete(2)
        dct[f'entity_{idx}_bouncing'] = spaces.Discrete(2)
        dct[f'entity_{idx}_onGround'] = spaces.Discrete(2)

    training_service = SuperMarioTrainingService(
        entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(dct),
        action_space=spaces.MultiBinary(4),
        max_episode_length=2000,
        total_timesteps=int(50000),
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO,
        random_reset_rate=0.0
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            training_service.train(save_path="./models", log_path="./logs", test_name="test")
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model.zip")
            training_service.play(100000)
