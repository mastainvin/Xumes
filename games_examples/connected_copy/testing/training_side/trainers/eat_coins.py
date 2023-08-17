import time

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces


from xumes.training_module import observation, reward, terminated, action, config
from games_examples.connected_new.objects import Balls, Coins, Tiles, WIDTH, HEIGHT, CENTER

@config
def train_impl(train_context):

    train_context.score = 0
    train_context.dis_coin=500
    train_context.last_coinx=58
    train_context.last_tilex=30

    train_context.time1 = time.time()
    train_context.time2 = train_context.time1
    train_context.x1 = -10000
    train_context.x2 = 0
    train_context.y1 = -10000
    train_context.y2 = 0

    train_context.observation_space = spaces.Dict({

        'ball_x': spaces.Box(CENTER[0]-70, CENTER[0]+70, shape=(1,), dtype=np.int32),
        'ball_y': spaces.Box(CENTER[1]-70, CENTER[1]+70, shape=(1,), dtype=np.int32),
        'coins_x': spaces.Box(0, WIDTH+10, dtype=np.int32, shape=(1,)),
        'coins_y': spaces.Box(0, HEIGHT, dtype=np.int32, shape=(1,)),
        't_x': spaces.Box(0, WIDTH+10, dtype=np.int32, shape=(1,)),
        't_y': spaces.Box(0, HEIGHT, dtype=np.int32, shape=(1,)),
        't_type': spaces.Box(1, 3, dtype=np.int32, shape=(1,))
    })
    # print(train_context.observation_space.shape,"shape")
    train_context.action_space = spaces.Discrete(2)
    train_context.max_episode_length = 3000
    train_context.total_timesteps = int(200000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO




@observation
def train_impl(train_context):

    train_context.states = {
        'ball_x': np.array([train_context.game.ball.rect.x+6]),
        'ball_y': np.array([train_context.game.ball.rect.y+6]),
        'coins_x': np.array([int(train_context.game.coin.x+7.5)]),
        'coins_y': np.array([int(train_context.game.coin.y+7.5)]),
        't_x': np.array([train_context.game.tile.x]),
        't_y': np.array([train_context.game.tile.y]),
        't_type': np.array([train_context.game.tile.type])
    }
    # print("Received states:", train_context.states,train_context.observation_space, train_context.coin,train_context.tile)
    return train_context.states
    #     here use tile instead of t


@reward
def train_impl(train_context):
    reward = 0

    if train_context.game.score > train_context.score:
        train_context.score = train_context.game.score
        print("+++++++++++10")
        reward += 10
        # return reward

    if train_context.game.terminated:
        train_context.score = 0
        print("tttttttttttterminated")
        reward -= 10
        # return reward

    dis_coin=abs(train_context.game.ball.rect.y + 6 - train_context.game.coin.y - 7.5)
    # dis_tile=abs(train_context.game.ball.rect.y - train_context.game.tile.y)
    # is_going_to_collide_tile1 = train_context.game.ball.rect.y<train_context.game.tile.y+10 and \
    #                 train_context.game.ball.rect.y+12>train_context.game.tile.y-10
    # is_going_to_collide_tile23 = train_context.game.ball.rect.y < train_context.game.tile.y + 25 and \
    #                 train_context.game.ball.rect.y + 12 > train_context.game.tile.y - 25
    is_going_to_collide_coin = train_context.game.ball.rect.y < train_context.game.coin.y + 15 and \
                    train_context.game.ball.rect.y + 12 > train_context.game.coin.y

    coin_on_the_right = train_context.game.ball.rect.x+12<train_context.game.coin.x
    # tile13_on_the_right = train_context.game.ball.rect.x+12<train_context.game.tile.x-25
    # tile2_on_the_right = train_context.game.ball.rect.x+12<train_context.game.tile.x-10

    # if not train_context.last_tilex==train_context.game.tile.x: #there is a tile on the screen
    # if 32<train_context.game.tile.x<298 and not train_context.last_tilex == train_context.game.tile.x:
    #     if tile13_on_the_right and train_context.game.tile.type==1 and is_going_to_collide_tile1:
    #         print("-2")
    #         reward -= 2
    #     elif tile2_on_the_right and train_context.game.tile.type==2 and is_going_to_collide_tile23:
    #         print("-2")
    #         reward -= 2
    #     elif tile13_on_the_right and train_context.game.tile.type==3 and is_going_to_collide_tile23:
    #         print("-2")
    #         reward -= 2
    if coin_on_the_right and 58<train_context.game.coin.x<298 and not train_context.last_coinx == train_context.game.coin.x: #there is a coin on the screen
        if is_going_to_collide_coin:
            print("+4")
            reward += 4
        # newly added
        else:
            if dis_coin < train_context.dis_coin:
                print("+4")
                reward += 4

    # else:  #is not going to collide with tiles
    #
    # if dis_coin<train_context.dis_coin and not train_context.last_coinx==train_context.coin.x:
    #     reward += 1
    #     train_context.dis_coin=dis_coin
    #     train_context.last_coinx = train_context.coin.x
    # else:
    #     if




    # if not train_context.game.terminated and train_context.game.score <= train_context.score:
    #     # print("0.1")
    #     reward += 1
    train_context.dis_coin = dis_coin
    train_context.last_tilex = train_context.game.tile.x
    train_context.last_coinx = train_context.game.coin.x
    return reward


@terminated
def train_impl(train_context):
    term = train_context.game.terminated or  train_context.game.score>=1
    return False


@action
def train_impl(train_context, raw_actions):

    direction = ["nothing", "space"]
    train_context.actions = [direction[raw_actions]]
    return train_context.actions
