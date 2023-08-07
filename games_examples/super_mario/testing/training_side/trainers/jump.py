import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces

from xumes.training_module import observation, reward, terminated, action, config

from games_examples.super_mario.classes.Level import nb_entites


@config
def train_impl(game_context):

    game_context.player_x, game_context.coins, game_context.points, game_context.player_state = 0, 0, 0, 0
    game_context.actions = ["nothing", "nothing", "nothing", "nothing"]

    dct = {
        'mario_rect': spaces.Box(-1, 1, dtype=np.float32, shape=(2,)),
        'mario_powerUpState': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'ending_level': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_coins': spaces.Box(0, 1, dtype=np.float32, shape=(1,)),
        'dashboard_points': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
    }

    game_context.observation_space = spaces.Dict(dct)
    game_context.action_space = spaces.MultiBinary(4)
    game_context.max_episode_length = 500
    game_context.total_timesteps = int(12228)
    game_context.algorithm_type = "MultiInputPolicy"
    game_context.algorithm = stable_baselines3.PPO
    game_context.random_reset_rate = 0.0

@observation
def train_impl(game_context):
    return {
        'mario_rect': np.array(game_context.mario.rect),
        'mario_powerUpState': np.array([game_context.mario.powerUpState]),
        'ending_level': np.array([game_context.mario.ending_level]),
        'dashboard_coins': np.array([game_context.mario.dashboard.coins]),
        'dashboard_points': np.array([game_context.mario.dashboard.points])
    }


@reward
def train_impl(game_context):
    reward = 0
    if game_context.mario.rect[0] > 384:
        reward += 1
    else:
        reward -= 1

    xDiff = game_context.mario.rect[0] - game_context.player_x
    if xDiff > 0:
        reward += 0.1
    else:
        reward -= 0.1

    return reward


@terminated
def train_impl(game_context):
    term = game_context.game.terminated or game_context.mario.rect[0] >= 448
    return term


@action
def train_impl(game_context, raw_actions):
    moves = [["nothing", "space"], ["nothing", "up"], ["nothing", "left"], ["nothing", "right"]]
    game_context.actions = [moves[0][int(raw_actions[0])], moves[1][int(raw_actions[1])],
                            moves[2][int(raw_actions[2])], moves[3][int(raw_actions[3])]]
    return game_context.actions




