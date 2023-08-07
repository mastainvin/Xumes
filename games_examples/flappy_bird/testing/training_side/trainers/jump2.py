import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces
from games_examples.flappy_bird.testing.training_side.helpers.lidar import Lidar
from games_examples.flappy_bird.params import LIDAR_MAX_DIST

from xumes.training_module import observation, reward, terminated, action, config


@config
def train_impl(game_context):
    game_context.lidar = None
    game_context.points = 0

    game_context.observation_space = spaces.Dict({
        "speedup": spaces.Box(-float('inf'), 300, shape=(1,), dtype=float),
        "lidar": spaces.Box(0, LIDAR_MAX_DIST, shape=(7,), dtype=int),
    })
    game_context.action_space = spaces.Discrete(2)
    game_context.max_episode_length = 2000
    game_context.total_timesteps = int(2e4)
    game_context.algorithm_type = "MultiInputPolicy"
    game_context.algorithm = stable_baselines3.PPO
    game_context.random_reset_rate = 0.0


@observation
def train_impl(game_context):
    if not game_context.lidar and game_context.pipe_generator and game_context.player:
        game_context.lidar = Lidar(game_context.pipe_generator, game_context.player)

    game_context.lidar.reset()
    game_context.lidar.vision()
    lidar = [line.distance for line in game_context.lidar.sight_lines]
    return {"speedup": np.array([game_context.player.speedup]), "lidar": np.array(lidar)}


@reward
def train_impl(game_context):
    if game_context.player.points > game_context.points:
        game_context.points = game_context.player.points
        return 1
    if game_context.game.terminated:
        return -1
    return 0


@terminated
def train_impl(game_context):
    term = game_context.game.terminated or game_context.player.points >= 2
    if term:
        game_context.lidar.reset()
        game_context.points = 0
    return term


@action
def train_impl(game_context, raw_actions):
    if raw_actions == 1:
        return ["space"]
    return ["nothing"]
