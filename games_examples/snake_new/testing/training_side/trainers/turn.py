import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces
from xumes.training_module import observation, config, reward, action, terminated


from games_examples.snake_new.src import snake, fruit
from games_examples.snake_new.src.fruit import cell_number



@config
def train_impl(train_context):

    train_context.distance = float('inf')

    train_context.observation_space = spaces.Dict({
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
        "direction_left": spaces.Box(0, 1, shape=(1,), dtype=int)
        })
    train_context.action_space = spaces.Discrete(5)
    train_context.max_episode_length = 2000
    train_context.total_timesteps = int(250000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO
    train_context.distance=100


@observation
def train_impl(train_context):
    return {
        "fruit_above_snake": np.array([1 if train_context.snake.body[1] > train_context.fruit.pos[1] else 0]),
        "fruit_right_snake": np.array([1 if train_context.snake.body[0] < train_context.fruit.pos[0] else 0]),
        "fruit_below_snake": np.array([1 if train_context.snake.body[1] < train_context.fruit.pos[1] else 0]),
        "fruit_left_snake": np.array([1 if train_context.snake.body[0] > train_context.fruit.pos[0] else 0]),
        "obstacle_above": np.array(
            [1 if train_context.snake.body[1] - 1 == 0 or (
             train_context.snake.body[0],  train_context.snake.body[1] - 1) in train_context.snake.body else 0]),
        "obstacle_right": np.array(
            [1 if train_context.snake.body[0] + 1 == cell_number or (
             train_context.snake.body[0] + 1,  train_context.snake.body[1]) in train_context.snake.body else 0]),
        "obstacle_bellow": np.array(
            [1 if train_context.snake.body[1] + 1 == cell_number or (
             train_context.snake.body[0],  train_context.snake.body[1] + 1) in train_context.snake.body else 0]),
        "obstacle_left": np.array(
            [1 if  train_context.snake.body[0] - 1 == 0 or (
             train_context.snake.body[0] - 1,  train_context.snake.body[1]) in train_context.snake.body else 0]),
        "direction_up": np.array([1 if train_context.snake.direction == (0, -1) else 0]),
        "direction_right": np.array([1 if train_context.snake.direction == (1, 0) else 0]),
        "direction_down": np.array([1 if train_context.snake.direction == (0, 1) else 0]),
        "direction_left": np.array([1 if train_context.snake.direction == (-1, 0) else 0]),
    }


@reward
def train_impl(train_context):
    close_reward = 0
    # print(train_context.snake.body, train_context.snake.direction, train_context.snake.new_block, train_context.fruit.pos,"booody")
    head_x, head_y = train_context.snake.body[0], train_context.snake.body[1]

    distance = np.abs(train_context.fruit.pos[0] - head_x) + np.abs(train_context.fruit.pos[1] - head_y)

    if distance < train_context.distance:

        close_reward += 2
    elif distance > train_context.distance:

        close_reward -= 2
    else:
        close_reward = 0
    if (train_context.fruit.pos[0] == train_context.snake.body[0] and train_context.fruit.pos[1] == train_context.snake.body[1]) or train_context.snake.new_block:
        # eat

        close_reward += 10
    if train_context.game.terminated:  #Boolean

        close_reward -= 10
    train_context.distance=distance
    return close_reward


@terminated
def train_impl(train_context):
    print(train_context.snake.body, "booooool")

    term =  train_context.game.terminated or  len(train_context.snake.body)>8
    # if term:
    if train_context.game.terminated:
        print("term1")
    if len(train_context.snake.body)>8:
        print("term3")
        # train_context.snake.body=train_context.snake.body[0:6]
        # print(len(train_context.snake.body), "booooool2")
    # if term:
        # train_context.snake.body=[5.0, 10.0, 4.0, 10.0, 3.0, 10.0]
    return term


@action
def train_impl(train_context, raw_actions):

    direction = ["nothing", "up", "down","right","left"]
    train_context.actions = [direction[raw_actions]]
    return train_context.actions
