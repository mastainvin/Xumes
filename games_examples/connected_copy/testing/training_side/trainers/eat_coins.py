import time

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces


from xumes.training_module import observation, reward, terminated, action, config
from games_examples.connected_copy.objects import Balls, Coins, Tiles, WIDTH, HEIGHT, CENTER

# RADIUS=70



@config
def train_impl(train_context):
    # list
    # train_context.dis_coin = []
    # train_context.dis_tile = []
    train_context.tileseq1 = [1]
    train_context.tileseq2 = [-1]
    train_context.tid=0
    train_context.is_going_to_collide_tile = []
    train_context.ball_dtheta = []
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
        'at_left':spaces.Box(0, 1, shape=(1,), dtype=np.int32),
        'at_right': spaces.Box(0, 1, shape=(1,), dtype=np.int32),
        'ball_to_coin_x':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        'ball_to_t_x':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        'ball_to_coin_y':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        'ball_to_t_y':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        'ball_x': spaces.Box(CENTER[0]-70, CENTER[0]+70, shape=(1,), dtype=np.int32),#74 214
        'ball_y': spaces.Box(CENTER[1]-70, CENTER[1]+70, shape=(1,), dtype=np.int32),#186 326
        'ball_dtheta':spaces.Box(-2, 2, shape=(1,), dtype=np.int32),
        'coins_x': spaces.Box(0, WIDTH+10, dtype=np.int32, shape=(1,)),
        'coins_y': spaces.Box(0, HEIGHT, dtype=np.int32, shape=(1,)),
        't_x': spaces.Box(0, WIDTH+10, dtype=np.int32, shape=(1,)),
        't_y': spaces.Box(0, HEIGHT, dtype=np.int32, shape=(1,)),
        't_type': spaces.Box(1, 3, dtype=np.int32, shape=(1,)),
        'is_going_to_collide_tile1':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_going_to_collide_tile23':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_above_tile_center':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_under_tile_center':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_up':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_down':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_left':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_right':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        'is_going_to_collide_coin':spaces.Box(0,1,dtype=np.int32,shape=(1,)),

    })
    # print(train_context.observation_space.shape,"shape")
    train_context.action_space = spaces.MultiDiscrete([3, 2])
    train_context.max_episode_length = 3000
    train_context.total_timesteps = int(250000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO




@observation
def train_impl(train_context):

    train_context.states = {
        'at_left':np.array([1 if train_context.game.ball.rect.x+6<=CENTER[0] else 0]),
        'at_right':np.array([1 if train_context.game.ball.rect.x+6>CENTER[0] else 0]),
        'ball_to_coin_x': np.array([train_context.game.ball.rect.x+6-int(train_context.game.coin.x+8)]),
        'ball_to_t_x': np.array([train_context.game.ball.rect.x+6-train_context.game.tile.x]),
        'ball_to_coin_y': np.array([train_context.game.ball.rect.x+6-int(train_context.game.coin.y+8)]),
        'ball_to_t_y': np.array([train_context.game.ball.rect.x+6-train_context.game.tile.y]),
        'ball_x': np.array([train_context.game.ball.rect.x+6]),
        'ball_y': np.array([train_context.game.ball.rect.y+6]),
        'ball_dtheta': np.array([train_context.game.ball.dtheta]),
        'coins_x': np.array([int(train_context.game.coin.x+8)]),
        'coins_y': np.array([int(train_context.game.coin.y+8)]),
        't_x': np.array([train_context.game.tile.x]),
        't_y': np.array([train_context.game.tile.y]),
        't_type': np.array([train_context.game.tile.type]),
        'is_going_to_collide_tile1':([1 if train_context.game.ball.rect.y<train_context.game.tile.y+15 and \
                    train_context.game.ball.rect.y+12>train_context.game.tile.y-15 else 0]),#10->15
        'is_going_to_collide_tile23':([1 if train_context.game.ball.rect.y < train_context.game.tile.y + 35 and \
                    train_context.game.ball.rect.y + 12 > train_context.game.tile.y-35 else 0]),#25->35
        'is_above_tile_center':([1 if train_context.game.ball.rect.y + 6<=train_context.game.tile.y else 0]),
        'is_under_tile_center': ([1 if train_context.game.ball.rect.y + 6>train_context.game.tile.y else 0]),

        'is_up':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.x+6-CENTER[0]))<=0 else 0]),
        'is_down':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.x+6-CENTER[0]))>=0 else 0]),
        'is_left':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.y+6-CENTER[1]))>=0 else 0]),
        'is_right':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.y+6-CENTER[1]))<=0 else 0]),
        'is_going_to_collide_coin': ([1 if train_context.game.ball.rect.y < train_context.game.coin.y + 16 and \
                    train_context.game.ball.rect.y + 12 > train_context.game.coin.y else 0])
    }
    # print("R:", train_context.game.ball.rect.x+6,train_context.game.ball.rect.y+6,train_context.game.coin.py.x+8,train_context.game.coin.py.y+8,train_context.game.tile.x,train_context.game.tile.y)
    return train_context.states
    #     here use tile instead of t



@reward
def train_impl(train_context):
    # train_context.ball_y.append(train_context.game.ball.rect.y + 6)
    # train_context.dis_coin.append(abs(train_context.game.ball.rect.y + 6 - train_context.game.coin.py.y - 8))
    # train_context.dis_tile.append(abs(train_context.game.ball.rect.y + 6 - train_context.game.tile.y))
    if train_context.last_tilex == train_context.game.tile.x:
        train_context.ball_dtheta.clear()
        train_context.is_going_to_collide_tile.clear()
    train_context.ball_dtheta.append(train_context.game.ball.dtheta)



    #
    reward = 0
    correct_direction = False

    if train_context.game.score > train_context.score:
        train_context.score = train_context.game.score
        print("+++++++++++15 eat a coin.py")
        reward += 15
        # return reward

    if train_context.game.terminated:
        train_context.score = 0
        # train_context.ball_y.clear()
        print("tttttttttttterminated -15")
        reward -= 15
    #
    # # # 若有tile
    # # if 32 < train_context.game.tile.x < 298 and not train_context.last_tilex == train_context.game.tile.x:
    if 32<train_context.game.tile.x<298 and not train_context.last_tilex == train_context.game.tile.x:
        if train_context.game.ball.rect.y<train_context.game.tile.y+15 and \
                train_context.game.ball.rect.y+12>train_context.game.tile.y-15 and \
                    train_context.game.tile.type==1:
            train_context.tileseq1.append(train_context.tileseq1[-1]+1)
            train_context.tileseq2.append(train_context.tileseq1[-1])
            train_context.tid=train_context.tileseq1[-1]
            # reward -= 0.05
            # print('-0.1  1')
        if train_context.tileseq1[-1]==train_context.tid and train_context.tileseq2[-1]==train_context.tid and not (train_context.game.ball.rect.y<train_context.game.tile.y+15 and \
                train_context.game.ball.rect.y+12>train_context.game.tile.y-15) and train_context.game.tile.type==1:
            train_context.tileseq2.pop()

        if train_context.game.ball.rect.y<train_context.game.tile.y+30 and \
                train_context.game.ball.rect.y+12>train_context.game.tile.y-30 and \
                    (train_context.game.tile.type==2 or train_context.game.tile.type==3):
            train_context.tileseq1.append(train_context.tileseq1[-1]+1)
            train_context.tileseq2.append(train_context.tileseq1[-1])
            train_context.tid=train_context.tileseq1[-1]
            # reward -= 0.05
            # print('-0.1  2')
        if train_context.tileseq1[-1]==train_context.tid and train_context.tileseq2[-1]==train_context.tid and not (train_context.game.ball.rect.y<train_context.game.tile.y+30 and \
                train_context.game.ball.rect.y+12>train_context.game.tile.y-30) and (train_context.game.tile.type==2 or train_context.game.tile.type==3):
            train_context.tileseq2.pop()


        if train_context.tileseq1[-1]==train_context.tid and not train_context.tileseq2[-1]==train_context.tid:
            reward += 7
            print('+10 avoid',train_context.tileseq1[-1], train_context.tid, train_context.tileseq2[-1])
            train_context.tileseq1.append(0)
            train_context.tileseq2.clear()
            train_context.tileseq2.append(-1)
    is_going_to_collide_coin = train_context.game.ball.rect.y < train_context.game.coin.y + 16 and \
                               train_context.game.ball.rect.y + 12 > train_context.game.coin.y
    coin_on_the_right = train_context.game.ball.rect.x+12<train_context.game.coin.x
    if train_context.game.score==0 and coin_on_the_right and 88 < train_context.game.coin.x < 228 and \
      not train_context.last_coinx == train_context.game.coin.x and not (62<train_context.game.tile.x<238 and not train_context.last_tilex == train_context.game.tile.x) and\
      not is_going_to_collide_coin:
    # if abs(train_context.game.ball.rect.y+6-train_context.game.coin.py.y-8)<50 and (train_context.game.tile.type==2 or train_context.game.tile.type==3):
        if abs(train_context.game.ball.rect.y+6-train_context.game.coin.y-8)>abs(train_context.game.ball.rect.y+6+train_context.game.ball.dtheta-train_context.game.coin.y-8):
            reward += 0.05
            print('+0.05')
        elif abs(train_context.game.ball.rect.y+6-train_context.game.coin.y-8)<abs(train_context.game.ball.rect.y+6+train_context.game.ball.dtheta-train_context.game.coin.y-8):
            reward-=0.05
            print('-0.05')


    train_context.last_tilex = train_context.game.tile.x
    train_context.last_coinx = train_context.game.coin.x
    return reward


@terminated
def train_impl(train_context):
    term = train_context.game.terminated \
           or train_context.score>=1
    return term


@action
def train_impl(train_context, raw_actions):
    direction = ["nothing", "up","down"]
    stop = ["nothing", "space"]
    train_context.actions = [direction[raw_actions[0]], stop[raw_actions[1]]]
    return train_context.actions

