import logging
import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces

from src.xumes.training_module import StableBaselinesTrainer, JsonGameElementStateConverter, \
                                        CommunicationServiceTrainingMq, AutoEntityManager

cell_size = 30
cell_number = 15
class SnakeTrainingService(StableBaselinesTrainer):

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

    def convert_obs(self) :

        snake_head_x = self.snake.body[0][0]
        snake_head_y = self.snake.body[0][1]

        # fruit = self.get_entity("fruit")
        fruit_x = self.fruit.pos.x
        fruit_y = self.fruit.pos.y

        return {
            "fruit_above_snake": np.array([1 if snake_head_y > fruit_y else 0]),
            "fruit_right_snake": np.array([1 if snake_head_x < fruit_x else 0]),
            "fruit_below_snake": np.array([1 if snake_head_y < fruit_y else 0]),
            "fruit_left_snake": np.array([1 if snake_head_x > fruit_x else 0]),
            "obstacle_above": np.array(
                [1 if snake_head_y - 1 == 0 or (snake_head_x, snake_head_y - 1) in self.snake.body else 0]),
            "obstacle_right": np.array(
                [1 if snake_head_x + 1 == cell_number or (snake_head_x + 1, snake_head_y) in self.snake.body else 0]),
            "obstacle_bellow": np.array(
                [1 if snake_head_y + 1 == cell_number or (snake_head_x, snake_head_y + 1) in self.snake.body else 0]),
            "obstacle_left": np.array(
                [1 if snake_head_x - 1 == 0 or (snake_head_x - 1, snake_head_y) in self.snake.body else 0]),
            "direction_up": np.array([1 if self.snake.direction == (0, -1) else 0]),
            "direction_right": np.array([1 if self.snake.direction == (1, 0) else 0]),
            "direction_down": np.array([1 if self.snake.direction == (0, 1) else 0]),
            "direction_left": np.array([1 if self.snake.direction == (-1, 0) else 0]),
        }

    def convert_reward(self) -> float:
        reward = 0

        fruit_x = self.fruit.x
        fruit_y = self.fruit.y

        snake_x, snake_y = self.snake.body[0][0], self.snake.body[0][1]
        distance = np.abs(fruit_x - snake_x) + np.abs(fruit_y - snake_y)

        if distance < self.distance:
            close_reward = 1
        elif distance > self.distance:
            close_reward = -1
        else:
            close_reward = 0

        if self.game_state == "fruit_ate":
            return 10
        elif self.game_state == "lose":
            return -100
        else:
            return close_reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        if raws_actions == 1:
            return ['up']
        elif raws_actions == 2:
            return ['down']
        elif raws_actions == 3:
            return ['left']
        elif raws_actions == 4:
            return ['right']
        return ['nothing']


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        dct = {
            "fruit_above_snake": spaces.Box(0, 1, shape=(1,), dtype=int),
            "fruit_right_snake": spaces.Box(0, 1, shape=(1,), dtype=int),
            "fruit_below_snake": spaces.Box(0, 1, shape=(1,), dtype=int),
            "fruit_left_snake": spaces.Box(0, 1, shape=(1,), dtype=int),
            "obstacle_above": spaces.Box(0, 1, shape=(1,), dtype=int),
            "obstacle_right": spaces.Box(0, 1, shape=(1,), dtype=int),
            "obstacle_bellow": spaces.Box(0, 1, shape=(1,), dtype=int),
            "obstacle_left": spaces.Box(0, 1, shape=(1,), dtype=int),
            "direction_up": spaces.Box(0, 1, shape=(1,), dtype=int),
            "direction_right": spaces.Box(0, 1, shape=(1,), dtype=int),
            "direction_down": spaces.Box(0, 1, shape=(1,), dtype=int),
            "direction_left": spaces.Box(0, 1, shape=(1,), dtype=int),
        }
    training_service = SnakeTrainingService(
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
