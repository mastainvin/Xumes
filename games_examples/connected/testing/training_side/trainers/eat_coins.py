import time

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces


from xumes.training_module import observation, reward, terminated, action, config
from games_examples.connected.src.params import HEIGHT, WIDTH,SPEED,SPACE_BETWEEN,CENTER
from games_examples.connected.src.generator import Generator
from games_examples.connected.src.tile import Tiles
from games_examples.connected.src.ball import Balls
from games_examples.connected.src.coin import Coins
from xumes.training_module import observation, reward, terminated, action, config
from games_examples.connected.testing.training_side.helpers.lidar import Lidar
from games_examples.connected.src.params import LIDAR_MAX_DIST

# RADIUS=70



@config
def train_impl(train_context):
    train_context.tileseq1 = [1]
    train_context.tileseq2 = [-1]
    train_context.tid = 0
    train_context.is_going_to_collide_tile = []
    train_context.ball_dtheta = []
    train_context.score = 0
    train_context.penalty = 0
    train_context.dis_coin = 500
    train_context.last_coinx = 58
    train_context.last_tilex = 30
    train_context.time1 = time.time()
    train_context.time2 = train_context.time1

    train_context.lidar = None
    train_context.points = 0

    train_context.observation_space = spaces.Dict({
        # "speedup": spaces.Box(-float('inf'), 300, shape=(1,), dtype=float),
        "lidar": spaces.Box(0, LIDAR_MAX_DIST, shape=(7,), dtype=int),
    })

    # train_context.observation_space = spaces.Dict({

        # 'ball_to_coin_x':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        # 'ball_to_t_x':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        # 'ball_to_coin_y':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        # 'ball_to_t_y':spaces.Box(-1000, 1000, shape=(1,), dtype=np.int32),
        # 'ball_x': spaces.Box(CENTER[0]-70, CENTER[0]+70, shape=(1,), dtype=np.int32),#74 214
        # 'ball_y': spaces.Box(CENTER[1]-70, CENTER[1]+70, shape=(1,), dtype=np.int32),#186 326
        # 'ball_dtheta':spaces.Box(-2, 2, shape=(1,), dtype=np.int32),
        # 'coins_x': spaces.Box(0, WIDTH+10, dtype=np.int32, shape=(1,)),
        # 'coins_y': spaces.Box(0, HEIGHT, dtype=np.int32, shape=(1,)),
        # 't_x': spaces.Box(0, WIDTH+10, dtype=np.int32, shape=(1,)),
        # 't_y': spaces.Box(0, HEIGHT, dtype=np.int32, shape=(1,)),
        # 't_type': spaces.Box(1, 3, dtype=np.int32, shape=(1,)),


        # 'is_going_to_collide_tile1':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_going_to_collide_tile23':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_above_tile_center':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_under_tile_center':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_up':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_down':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_left':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_right':spaces.Box(0,1,dtype=np.int32,shape=(1,)),
        # 'is_going_to_collide_coin':spaces.Box(0,1,dtype=np.int32,shape=(1,)),

    # })
    # print(train_context.observation_space.shape,"shape")
    train_context.action_space = spaces.Discrete(3)
    train_context.max_episode_length = 3000
    train_context.total_timesteps = int(4000000)
    train_context.algorithm_type = "MultiInputPolicy"
    train_context.algorithm = stable_baselines3.PPO




@observation
def train_impl(train_context):
    if not train_context.lidar and train_context.generator and train_context.ball:
        train_context.lidar = Lidar(train_context.generator, train_context.ball)

    train_context.lidar.reset()
    train_context.lidar.vision()
    lidar = [line.distance for line in train_context.lidar.sight_lines]
    return { "lidar": np.array(lidar)}
    # train_context.states = {
        # 'ball_to_coin_x': np.array([train_context.ball.x + 6 - int(train_context.coin.x + 8)]),
        # 'ball_to_t_x': np.array([train_context.ball.x + 6 - train_context.tile.x + train_context.tile.width / 2]),
        # 'ball_to_coin_y': np.array([train_context.ball.x + 6 - int(train_context.coin.y + 8)]),
        # 'ball_to_t_y': np.array([train_context.ball.x + 6 - train_context.tile.y + train_context.tile.height / 2]),
        # 'ball_x': np.array([train_context.ball.x + 6]),
        # 'ball_y': np.array([train_context.ball.y + 6]),
        # 'ball_dtheta': np.array([train_context.ball.dtheta]),
        # 'coins_x': np.array([int(train_context.coin.x + 8)]),
        # 'coins_y': np.array([int(train_context.coin.y + 8)]),
        # 't_x': np.array([train_context.tile.x + train_context.tile.width / 2]),
        # 't_y': np.array([train_context.tile.y + train_context.tile.height / 2]),
        # 't_type': np.array([train_context.tile.type]),

        # 'is_going_to_collide_tile1':([1 if train_context.game.ball.rect.y<train_context.game.tile.y+15 and \
        #             train_context.game.ball.rect.y+12>train_context.game.tile.y-15 else 0]),#10->15
        # 'is_going_to_collide_tile23':([1 if train_context.game.ball.rect.y < train_context.game.tile.y + 35 and \
        #             train_context.game.ball.rect.y + 12 > train_context.game.tile.y-35 else 0]),#25->35
        # 'is_above_tile_center':([1 if train_context.game.ball.rect.y + 6<=train_context.game.tile.y else 0]),
        # 'is_under_tile_center': ([1 if train_context.game.ball.rect.y + 6>train_context.game.tile.y else 0]),

        # 'is_up':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.x+6-CENTER[0]))<=0 else 0]),
        # 'is_down':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.x+6-CENTER[0]))>=0 else 0]),
        # 'is_left':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.y+6-CENTER[1]))>=0 else 0]),
        # 'is_right':([1 if (train_context.game.ball.dtheta * (train_context.game.ball.rect.y+6-CENTER[1]))<=0 else 0]),
        # 'is_going_to_collide_coin': ([1 if train_context.game.ball.rect.y < train_context.game.coin.y + 16 and \
        #             train_context.game.ball.rect.y + 12 > train_context.game.coin.y else 0])
    # }
    # print("R:", train_context.game.ball.rect.x+6,train_context.game.ball.rect.y+6,train_context.game.coin.py.x+8,train_context.game.coin.py.y+8,train_context.game.tile.x,train_context.game.tile.y)
    # return train_context.states
    #     here use tile instead of t



@reward
def train_impl(train_context):
    # train_context.ball_y.append(train_context.game.ball.rect.y + 6)
    # train_context.dis_coin.append(abs(train_context.game.ball.rect.y + 6 - train_context.game.coin.py.y - 8))
    # train_context.dis_tile.append(abs(train_context.game.ball.rect.y + 6 - train_context.game.tile.y))
    # print(train_context.generator.pipes[0], "pipes[0]")
    # print(train_context.generator.pipes[0].rect[4],"pipes[0].rect[4]")




    #
    reward = 0
    correct_direction = False

    if train_context.ball.points > train_context.score:
        train_context.score = train_context.ball.points
        print("+++++++++++15 eat a coin.py")
        reward += 15
        # return reward

    if train_context.game.terminated:
        train_context.score = 0
        train_context.penalty = 0
        # train_context.ball_y.clear()
        print("tttttttttttterminated -15")
        reward -= 25
    if train_context.ball.penalty >train_context.penalty:
        train_context.penalty=train_context.ball.penalty
        reward-=10

    if train_context.ball.dtheta==0:
        reward-=10
    # if not len(train_context.generator.pipes)==0:
    #     is_tile_not_moving=train_context.last_tilex == train_context.generator.pipes[0].rect[4] and train_context.generator.pipes[0].kind =='tile'
    #     is_tile_in_collision_pos_x= 32<train_context.generator.pipes[0].rect[4]<298 and train_context.generator.pipes[0].kind =='tile'
    #     is_tile_in_collision_pos_y=train_context.ball.y - 6 < train_context.generator.pipes[0].rect[5] + round(train_context.generator.pipes[0].h / 2) and \
    #     train_context.ball.y + 6 > train_context.generator.pipes[0].rect[5] - round(train_context.generator.pipes[0].h / 2) and \
    #                                train_context.generator.pipes[0].kind == 'tile'
    #     is_coin_not_moving = train_context.last_coinx == train_context.generator.pipes[0].rect[4] and \
    #                          train_context.generator.pipes[0].kind == 'coin'
    #     is_coin_in_collision_pos_x=train_context.generator.pipes[0].kind =='coin'
    #     is_coin_in_collision_pos_y=train_context.ball.y - 6 < train_context.generator.pipes[0].rect[5] + round(train_context.generator.pipes[0].h / 2) and \
    #     train_context.ball.y + 6 > train_context.generator.pipes[0].rect[5] - round(train_context.generator.pipes[0].h / 2) and \
    #                                train_context.generator.pipes[0].kind == 'coin'
        # if is_tile_not_moving:
        #     train_context.ball_dtheta.clear()
        #     train_context.is_going_to_collide_tile.clear()
        # train_context.ball_dtheta.append(train_context.ball.dtheta)
    # # # # 若有tile
    # # if 32 < train_context.game.tile.x < 298 and not train_context.last_tilex == train_context.game.tile.x:
    #     if is_tile_in_collision_pos_x and not is_tile_not_moving:
    #         if is_tile_in_collision_pos_y:
    #             train_context.tileseq1.append(train_context.tileseq1[-1]+1)
    #             train_context.tileseq2.append(train_context.tileseq1[-1])
    #             train_context.tid=train_context.tileseq1[-1]
    #             # reward -= 0.05
    #             # print('-0.1  1')
    #         if train_context.tileseq1[-1]==train_context.tid and\
    #                 train_context.tileseq2[-1]==train_context.tid and \
    #                 not is_tile_in_collision_pos_y :
    #             train_context.tileseq2.pop()
    #
    #
    #
    #
    #         if train_context.tileseq1[-1]==train_context.tid and\
    #                 not train_context.tileseq2[-1]==train_context.tid:
    #             reward += 7
    #             print('+10 avoid',train_context.tileseq1[-1], train_context.tid, train_context.tileseq2[-1])
    #             train_context.tileseq1.append(0)
    #             train_context.tileseq2.clear()
    #             train_context.tileseq2.append(-1)
    #
    #         if is_coin_in_collision_pos_x and not is_coin_not_moving:
    #             if is_coin_in_collision_pos_y:
    #                 reward += 0.3
    #             elif not is_coin_in_collision_pos_y:
    #                 if abs(train_context.generator.pipes[0].rect[5]-train_context.ball.y)-\
    #                     abs(train_context.generator.pipes[0].rect[5]-train_context.ball.y-train_context.ball.dtheta)>0:
    #                     reward+=0.4
        # is_going_to_collide_coin = train_context.game.ball.rect.y < train_context.game.coin.y + 16 and \
        #                            train_context.game.ball.rect.y + 12 > train_context.game.coin.y
        # coin_on_the_right = train_context.game.ball.rect.x+12<train_context.game.coin.x
        # if train_context.game.score==0 and coin_on_the_right and 88 < train_context.game.coin.x < 228 and \
        #   not train_context.last_coinx == train_context.game.coin.x and not (62<train_context.game.tile.x<238 and not train_context.last_tilex == train_context.game.tile.x) and\
        #   not is_going_to_collide_coin:
        # # if abs(train_context.game.ball.rect.y+6-train_context.game.coin.py.y-8)<50 and (train_context.game.tile.type==2 or train_context.game.tile.type==3):
        #     if abs(train_context.game.ball.rect.y+6-train_context.game.coin.y-8)>abs(train_context.game.ball.rect.y+6+train_context.game.ball.dtheta-train_context.game.coin.y-8):
        #         reward += 0.05
        #         print('+0.05')
        #     elif abs(train_context.game.ball.rect.y+6-train_context.game.coin.y-8)<abs(train_context.game.ball.rect.y+6+train_context.game.ball.dtheta-train_context.game.coin.y-8):
        #         reward-=0.05
        #         print('-0.05')
        #
        #
            # if train_context.generator.pipes[0].kind =='tile':
            #
            #     train_context.last_tilex = train_context.generator.pipes[0].rect[4]
            # elif train_context.generator.pipes[0].kind =='coin':
            #     train_context.last_coinx = train_context.generator.pipes[0].rect[4]
    return reward


@terminated
def train_impl(train_context):
    term = train_context.game.terminated \
           or train_context.score>=3
    if term:
        train_context.score = 0
    return term


@action
def train_impl(train_context, raw_actions):
    direction = ["nothing","up","down"]
    train_context.actions = [direction[raw_actions]]
    return train_context.actions
    # if raw_actions == 1:
    #     return ["up"]
    # elif raw_actions == 2:
    #     return ["down"]
    # return ["nothing"]

