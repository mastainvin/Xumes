import time

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces


from xumes.training_module import observation, reward, terminated, action, config
from games_examples.flappy_bird.testing.training_side.helpers.lidar import Lidar
from games_examples.flappy_bird.params import LIDAR_MAX_DIST

@config
def train_impl(train_context):

    train_context.score = 0

    train_context.time1 = time.time()
    train_context.time2 = train_context.time1
    train_context.x1 = -10000
    train_context.x2 = 0
    train_context.y1 = -10000
    train_context.y2 = 0

    train_context.observation_space = spaces.Dict({
        'ball_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'ball_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'coins_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'coins_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'tiles_type': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
    })
    train_context.action_space = spaces.Discrete(2)
    train_context.max_episode_length = 2000
    train_context.total_timesteps = int(10000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO




@observation
def train_impl(train_context):

    train_context.states = {
        'ball_x': np.array(train_context.ball.rect.x),
        'ball_y': np.array(train_context.ball.rect.y),
        'coins_x': np.array(train_context.coin.rect.x),
        'coins_y': np.array(train_context.coin.rect.y),
        'tiles_x': np.array(train_context.tile.rect.x),
        'tiles_y': np.array(train_context.tile.rect.y),
        'tiles_type': np.array(train_context.tile.type)
    }
    print("Received states:", train_context.states)
    return train_context.states
    #     here use tile instead of t


@reward
def train_impl(train_context):
    reward = 0

    if train_context.game.terminated:
        train_context.score = 0
        reward += -1

    # if self.game.ball.score > self.score:
    #     self.score = self.game.ball.score
    #     return 1
    else:
        reward += 0.3
    # il gagne un coin -> 1 si il perds -1 0
    #
    # if self.game.ball.score > self.score :
    #     self.score = self.game.ball.score
    #     reward += 1
    #
    # if self.game.terminated:
    #     return -1
    # return 0

    # if self.game.ball.rect.x < self.game.t.x:
    # reward += 10
    # if self.game.ball.score > self.score:
    # reward += 5
    # self.score = self.game.ball.score
    # if self.game.ball.score >= self.game.ball.highscore:
    # reward += 10
    # if self.game.terminated:
    # reward -= 5

    return reward


@terminated
def train_impl(train_context):
    return train_context.game.terminated


@action
def train_impl(train_context, raw_actions):

    direction = ["nothing", "space"]
    train_context.actions = [direction[raw_actions]]
    return train_context.actions
