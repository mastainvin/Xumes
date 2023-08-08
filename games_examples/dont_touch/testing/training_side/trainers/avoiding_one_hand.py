import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from xumes.training_module import observation, reward, terminated, action, config

@config
def train_impl(train_context):

    train_context.actions = ["nothing", "nothing"]
    train_context.xDiff = 0
    train_context.score = 0

    dct = {
        'player_position': spaces.Box(-1, 1, dtype=np.float64, shape=(2,)),
        'scoreboard_current_score': spaces.Box(-1, 1, dtype=np.int64, shape=(1,)),
        'scoreboard_max_score': spaces.Box(-1, 1, dtype=np.int64, shape=(1,)),
        'hand_side': spaces.Box(-1, 1, dtype=np.int64, shape=(1,)),
        'hand_x': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'hand_y': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'hand_speed': spaces.Box(-1, 1, dtype=np.float64, shape=(1,))
    }

    train_context.observation_space = spaces.Dict(dct)
    train_context.action_space = spaces.MultiDiscrete([3, 3])
    train_context.max_episode_length = 1000
    train_context.total_timesteps = int(30000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO


@observation
def train_impl(train_context):

    return {
        'player_position': np.array([train_context.player.player_position]),
        'scoreboard_current_score': np.array([train_context.scoreboard.current_score]),
        'scoreboard_max_score': np.array([train_context.scoreboard.max_score]),
        'hand_side': np.array([train_context.hand.hand_side]),
        'hand_x': np.array([train_context.hand.new_x]),
        'hand_y': np.array([train_context.hand.new_y]),
        'hand_speed': np.array([train_context.hand.new_spd])
    }


@reward
def train_impl(train_context):

    reward = 0
    xHand, yLeft = train_context.hand.new_x, train_context.hand.new_y
    xPlayer, yPlayer = train_context.player.player_position[0], train_context.player.player_position[1]


    def reward_right(xDiff):
        if xDiff < train_context.xDiff:
            return 0.1
        else:
            return -0.1

    def reward_left(xDiff):
        if xDiff > train_context.xDiff:
            return 0.1
        else:
            return -0.1

    if train_context.game.terminated:
        reward -= 1
    if train_context.scoreboard.current_score > train_context.score:
        reward += 1

    xDiff = xPlayer - xHand

    if train_context.hand.hand_side == 0:
        reward += reward_left(xDiff)
    else:
        reward += reward_right(xDiff)


    train_context.xDiff = xDiff
    train_context.score = train_context.scoreboard.current_score

    return reward



@terminated
def train_impl(train_context):
    return train_context.game.terminated or train_context.scoreboard.current_score >= 1


@action
def train_impl(train_context, raw_actions):
    direction = ["nothing", "left", "right"]
    position = ["nothing", "up", "down"]
    train_context.actions = [direction[raw_actions[0]], position[raw_actions[1]]]
    return train_context.actions
