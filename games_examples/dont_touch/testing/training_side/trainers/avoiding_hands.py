import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces
from games_examples.flappy_bird.testing.training_side.helpers.lidar import Lidar
from games_examples.flappy_bird.params import LIDAR_MAX_DIST

from xumes.training_module import observation, reward, terminated, action, config


@config
def train_impl(train_context):

    train_context.actions = ["nothing", "nothing"]

    train_context.observation_space = spaces.Dict({
        'player_position': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'left_hand_position': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'left_hand_speed': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'right_hand_position': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'right_hand_speed': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'scoreboard_current_score': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
        'scoreboard_max_score': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
    })
    train_context.action_space = spaces.Discrete(2)
    train_context.max_episode_length = 2000
    train_context.total_timesteps = int(5e5)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO


@observation
def train_impl(train_context):

    dct = {
        'player_position': np.array([train_context.player.rect]),
        'scoreboard_current_score': np.array([train_context.scoreboard._current_score]),
        'scoreboard_max_score': np.array([train_context.scoreboard._max_score])
    }

    if train_context.H1 is not None:
        dct["left_hand_position"] = np.array([train_context.H1.rect])
        dct["left_hand_speed"] = np.array([train_context.H1.new_spd])
    if train_context.H2 is not None:
        dct["right_hand_position"] = np.array([train_context.H2.rect])
        dct["right_hand_speed"] = np.array([train_context.H2.new_spd])

    return dct


@reward
def train_impl(train_context):
    if train_context.player.points > train_context.points:
        train_context.points = train_context.player.points
        return 1
    if train_context.game.terminated:
        return -1
    return 0


@terminated
def train_impl(train_context):
    term = train_context.game.terminated or train_context.player.points >= 2
    return term


@action
def train_impl(train_context, raw_actions):
    direction = ["nothing", "left", "right"]
    position = ["nothing", "up", "down"]
    train_context.actions = [direction[raw_actions[0]], position[raw_actions[1]]]
    return train_context.actions
