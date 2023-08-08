import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from xumes.training_module import observation, reward, terminated, action, config


@config
def train_impl(train_context):

    train_context.actions = ["nothing", "nothing"]
    train_context.xDiff, train_context.yDiff = 0, 0
    train_context.score = 0

    dct = {
        'player_position': spaces.Box(-1, 1, dtype=np.float64, shape=(2,)),
        'scoreboard_current_score': spaces.Box(-1, 1, dtype=np.int64, shape=(1,)),
        'scoreboard_max_score': spaces.Box(-1, 1, dtype=np.int64, shape=(1,)),
        'left_hand_x': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'left_hand_y': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'left_hand_speed': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'right_hand_x': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'right_hand_y': spaces.Box(-1, 1, dtype=np.float64, shape=(1,)),
        'right_hand_speed': spaces.Box(-1, 1, dtype=np.float64, shape=(1,))
    }


    train_context.observation_space = spaces.Dict(dct)
    train_context.action_space = spaces.MultiDiscrete([3, 3])
    train_context.max_episode_length = 1000
    train_context.total_timesteps = int(30000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO


@observation
def train_impl(train_context):

    dct = {
        'player_position': np.array([train_context.player.player_position]),
        'scoreboard_current_score': np.array([train_context.scoreboard.current_score]),
        'scoreboard_max_score': np.array([train_context.scoreboard.max_score])
    }

    if train_context.left_hand is not None:
        dct["left_hand_x"] = np.array([train_context.left_hand.new_x])
        dct["left_hand_y"] = np.array([train_context.left_hand.new_y])
        dct["left_hand_speed"] = np.array([train_context.left_hand.new_spd])
    else :
        dct["left_hand_x"] = np.array([float(-100)])
        dct["left_hand_y"] = np.array([float(-320)])
        dct["left_hand_speed"] = np.array([float(0)])
    if train_context.right_hand is not None:
        dct["right_hand_x"] = np.array([train_context.right_hand.new_x])
        dct["right_hand_y"] = np.array([train_context.right_hand.new_y])
        dct["right_hand_speed"] = np.array([train_context.right_hand.new_spd])
    else:
        dct["right_hand_x"] = np.array([float(400)])
        dct["right_hand_y"] = np.array([float(-40)])
        dct["right_hand_speed"] = np.array([float(0)])

    return dct


@reward
def train_impl(train_context):
    reward = 0

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

    if train_context.right_hand is not None:
        xRight, yRight = train_context.right_hand.new_x, train_context.right_hand.new_y
    if train_context.left_hand is not None:
        xLeft, yLeft = train_context.left_hand.new_x, train_context.left_hand.new_y
    xPlayer, yPlayer = train_context.player.player_position[0], train_context.player.player_position[1]

    if train_context.game.terminated:
        reward -= 1
    if train_context.scoreboard.current_score > train_context.score:
        reward += 1

    if train_context.right_hand is None:
        xDiff = xPlayer - xLeft
        reward += reward_left(xDiff)
        train_context.xDiff = xDiff
    elif train_context.left_hand is None:
        xDiff = xPlayer - xRight
        reward += reward_right(xDiff)
        train_context.xDiff = xDiff
    elif train_context.left_hand is not None and train_context.right_hand is not None:
        yDiffRight = np.abs(yPlayer - yRight)
        yDiffLeft = np.abs(yPlayer - yLeft)
        if yDiffLeft > yDiffRight:
            xDiff = xPlayer - xRight
            reward += reward_right(xDiff)
            train_context.xDiff = xDiff
        else:
            xDiff = xPlayer - xLeft
            reward += reward_left(xDiff)
            train_context.xDiff = xDiff

    train_context.score = train_context.scoreboard.current_score

    return reward



@terminated
def train_impl(train_context):
    if train_context.left_hand is None or train_context.right_hand is None:
        term = train_context.game.terminated or train_context.scoreboard.current_score >= 1
    else:
        term = train_context.game.terminated or train_context.scoreboard.current_score >= 2
    return term


@action
def train_impl(train_context, raw_actions):
    direction = ["nothing", "left", "right"]
    position = ["nothing", "up", "down"]
    train_context.actions = [direction[raw_actions[0]], position[raw_actions[1]]]
    return train_context.actions
