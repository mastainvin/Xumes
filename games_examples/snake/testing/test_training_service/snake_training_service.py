import sys
from abc import ABC
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces

from src.xumes import EntityManager
from src.xumes import ICommunicationServiceTraining
from src.xumes import JsonGameElementStateConverter
from src.xumes import StableBaselinesTrainer, \
    OBST
from src.xumes import \
    CommunicationServiceTrainingMq
from games_examples.snake.play import cell_number
from games_examples.snake.testing.test_training_service.entities.snake_entity_manager import SnakeEntityManager


class SnakeTrainingService(StableBaselinesTrainer, ABC):

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service: ICommunicationServiceTraining,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm)
        self.distance = float('inf')

    def convert_obs(self) -> OBST:
        snake = self.get_entity("snake")
        snake_head = snake.body[0]
        fruit = self.get_entity("fruit")

        return {
            "fruit_above_snake": np.array([1 if snake_head[1] > fruit.y else 0]),
            "fruit_right_snake": np.array([1 if snake_head[0] < fruit.x else 0]),
            "fruit_below_snake": np.array([1 if snake_head[1] < fruit.y else 0]),
            "fruit_left_snake": np.array([1 if snake_head[0] > fruit.x else 0]),
            "obstacle_above": np.array(
                [1 if snake_head[1] - 1 == 0 or (snake_head[0], snake_head[1] - 1) in snake.body else 0]),
            "obstacle_right": np.array(
                [1 if snake_head[0] + 1 == cell_number or (snake_head[0] + 1, snake_head[1]) in snake.body else 0]),
            "obstacle_bellow": np.array(
                [1 if snake_head[1] + 1 == cell_number or (snake_head[0], snake_head[1] + 1) in snake.body else 0]),
            "obstacle_left": np.array(
                [1 if snake_head[0] - 1 == 0 or (snake_head[0] - 1, snake_head[1]) in snake.body else 0]),
            "direction_up": np.array([1 if snake.direction == (0, -1) else 0]),
            "direction_right": np.array([1 if snake.direction == (1, 0) else 0]),
            "direction_down": np.array([1 if snake.direction == (0, 1) else 0]),
            "direction_left": np.array([1 if snake.direction == (-1, 0) else 0]),
        }

    def convert_reward(self) -> float:
        snake = self.get_entity("snake")
        fruit = self.get_entity("fruit")

        head_x, head_y = snake.body[0][0], snake.body[0][1]
        distance = np.abs(fruit.x - head_x) + np.abs(fruit.y - head_y)

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
        return self.game_state == "lose"

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
    training_service = SnakeTrainingService(
        entity_manager=SnakeEntityManager(
            JsonGameElementStateConverter()
        ),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict({
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
        }),
        action_space=spaces.Discrete(5),
        max_episode_length=500,
        total_timesteps=int(2e5),
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO
    )

    if len(sys.argv) == 2:
        if sys.argv[1] == "-train":
            training_service.train()
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model")
            training_service.play(100000)
