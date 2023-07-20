import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces
from xumes.training_module import observation, config, reward, action, terminated

from games_examples.snake_new.play import Main
from games_examples.snake_new.src import snake, fruit
from games_examples.snake_new.src.fruit import cell_number
from games_examples.snake_new.src.snake import Snake


@config
def train_impl(train_context):

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
    train_context.action_space = spaces.MultiDiscrete(5)
    train_context.max_episode_length = 2000
    train_context.total_timesteps = int(2e5)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO


@observation
def train_impl(train_context):
    return {
        "fruit_above_snake": np.array([1 if train_context.body[train_context.fruit.pos[1]] else 0]),
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

    distance = np.abs( train_context.fruit.pos[0] - train_context.snake.body[0]) + np.abs( train_context.fruit.pos[1] -  train_context.snake.body[1])
    # print(distance, distance,"dis")
    # 蛇头与水果同行同列
    # If the head of the snake is in the same line( col or row)
    # 如果蛇头与水果同行或同列
    if np.abs( train_context.fruit.pos[0] - train_context.snake.body[0]) * np.abs( train_context.fruit.pos[1] -  train_context.snake.body[1]) == 0:

        # If any body block of the snake is in the same col with both the head and the fruit
        # and The direction of the snake is not the opposite direction of "head ---> fruit".
        # 如果蛇身在蛇头和水果的同列，并且蛇的方向不是蛇头指向水果的方向的反方向
        if (np.abs(train_context.fruit.pos[0] - train_context.snake.body[0]) == 0) and (
                (train_context.fruit.pos[1] - train_context.snake.body[1]) * train_context.snake.direction[1]) >= 0:

            c1 = 0
            c2 = 0
            # for index, element in enumerate(snake.body):
            #     if element != 0 and element % 2 == 0:
            #         # 取得蛇身的x坐标（左右坐标）
            #         if element - fruit.pos[0]==0:
            #             # 如果这个蛇身块与水果在同一列
            #             c1+=1
            # getting x coordinates for every body block
            # 取得蛇身的x坐标（左右坐标）
            for index, element in enumerate(train_context.snake.body):
                if index != 0 and index % 2 == 0:

                    # If this exact body block is in the same col with the fruit
                    # 如果这个蛇身块与水果在同一列
                    if element -  train_context.fruit.pos[0] == 0:

                        c1 += 1
                        # If this body block lays between the head and the fruit, c2+=1
                        # 如果蛇身在蛇头和水果的同列，并且蛇身在蛇头和水果中间
                        if (train_context.snake.body[index + 1] - train_context.fruit.pos[1]) * (
                                 train_context.snake.body[index + 1] - train_context.snake.body[1]) <= 0:
                            c2 += 1
            if c2 == 0:  # 所有蛇身都不在蛇头和水果中间 if all body blocks are not in the middle of head and fruit
                close_reward += 10
                if (train_context.fruit.pos[1] - train_context.snake.body[1]) * train_context.snake.direction[1] > 0:
                    # 如果蛇还是朝着水果前进的 If the snake is moving forward to the fruit
                    close_reward += 30

        # same logic, but for the condition that
        # the snake is in the same row ( not the same col ) with both the head and the fruit

        # # If any body block of the snake is in the same row with both the head and the fruit
        # # and The direction of the snake is not the opposite direction of "head ---> fruit".
        # 如果蛇身在蛇头和水果的同行，并且蛇的方向不是蛇头指向水果的方向的反方向
        elif (np.abs( train_context.fruit.pos[1] - train_context.snake.body[1]) == 0) and (
                (train_context.fruit.pos[0] - train_context.snake.body[0]) * train_context.snake.direction[0]) >= 0:

            c1 = 0
            c2 = 0
            # getting y coordinates for every body block
            # 取得蛇身的y坐标（上下坐标）
            for index, element in enumerate( train_context.snake.body):
                if index != 1 and index % 2 == 1:
                    # If this exact body block is in the same row to the fruit
                    # 如果这个蛇身块与水果在同一行
                    if element - train_context.fruit.pos[1] == 0:

                        c1 += 1
                        if (train_context.snake.body[index - 1] - train_context.fruit.pos[0]) * (
                                 train_context.snake.body[index - 1] - train_context.snake.body[0]) <= 0:
                            # If this body block lays between the head and the fruit, c2+=1
                            # 如果蛇身在蛇头和水果的同行，并且蛇身在蛇头和水果中间
                            c2 += 1
            if c2 == 0:  # 所有蛇身都不在蛇头和水果中间 if all body blocks are not in the middle of head and fruit
                close_reward += 10
                if ( train_context.fruit.pos[0] -  train_context.snake.body[0]) *  train_context.snake.direction[0] > 0:
                    # 如果蛇还是朝着水果前进的 If the snake is moving forward to the fruit
                    close_reward += 30

    # check_fail
    # the head of the snake is not in the game field(from 0 to cell_number-1 for both dimensions)
    if not 0 <=  train_context.snake.body[0] < cell_number or not 0 <=  train_context.snake.body[1] < cell_number:
        close_reward -= 30
    # if the head bump into any body block
    else:
        # getting all y coordinates for body blocks
        for indexy, elementy in enumerate(train_context.snake.body):
            if indexy != 1 and indexy % 2 == 1:
                # if a body clock has the same coordinates with the head
                if elementy == train_context.snake.body[1] and train_context.snake.body[indexy - 1] ==  train_context.snake.body[0]:
                    close_reward -= 30
                    break  # 跳出循环 jump out of the loop

    # 离边界非常近，则给予-10
    # if the head is going to bump into the wall after the next move, reward-=10
    if (train_context.snake.body[0] < 1 and train_context.snake.direction[0] == -1) or \
            (train_context.snake.body[1] < 1 and train_context.snake.direction[1] == -1) or \
            (train_context.snake.body[0] > cell_number - 2 and train_context.snake.direction[0] == 1) or \
            (train_context.snake.body[1] > cell_number - 2 and train_context.snake.direction[1] == 1):
        close_reward -= 10
    # if the head is going to bump into a body block
    else:
        # getting all y coordinates for body blocks
        for indexy, elementy in enumerate( train_context.snake.body):
            if indexy != 1 and indexy % 2 == 1:
                # if a body clock has the same coordinates with the head
                if elementy == train_context.snake.body[1] + train_context.snake.direction[1] and train_context.snake.body[indexy - 1] == \
                         train_context.snake.body[0] + train_context.snake.direction[0]:
                    close_reward -= 10
                    break  # jump out of the loop

    # check_ate(collision):
    # if head has the same coordinates with fruit
    if (train_context.fruit.pos[0] == train_context.snake.body[0] and train_context.fruit.pos[1] ==  train_context.snake.body[1]) or \
            train_context.fruit.pos[0] == train_context.snake.body[0] + train_context.snake.direction[0] \
            and train_context.fruit.pos[1] == train_context.snake.body[1] + train_context.snake.direction[1]:
        close_reward += 80

    # if the snake is moving towards the fruit
    if distance < distance:
        close_reward += 5
        distance = distance
    #
    elif distance > distance:
        close_reward += -1
        distance = distance

    else:
        close_reward += 0
        distance = distance

    distance = distance
    print("reward:", close_reward)
    return close_reward


@terminated
def train_impl(train_context):
    return train_context.main.terminated


@action
def train_impl(train_context, raw_actions):
    if snake.direction[0] == 0:
        direction = ["nothing", "left", "right"]
    elif snake.direction[1] == 0:
        direction = ["nothing", "up", "down"]
    actions = [direction[raw_actions[0]]]
    return actions
