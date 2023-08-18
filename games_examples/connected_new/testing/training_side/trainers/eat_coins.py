import time

import numpy as np
import stable_baselines3
from gymnasium.vector.utils import spaces


from xumes.training_module import observation, reward, terminated, action, config
from games_examples.connected_new.objects import Balls, Coins, Tiles, WIDTH, HEIGHT, CENTER

# RADIUS=70



@config
def train_impl(train_context):
    # list
    # train_context.dis_coin = []
    # train_context.dis_tile = []
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

        'ball_x': spaces.Box(CENTER[0]-70, CENTER[0]+70, shape=(1,), dtype=np.int32),
        'ball_y': spaces.Box(CENTER[1]-70, CENTER[1]+70, shape=(1,), dtype=np.int32),
        'ball_dtheta':spaces.Box(-2, 2, shape=(1,), dtype=np.int32),
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
        'ball_dtheta': np.array([train_context.game.ball.dtheta]),
        'coins_x': np.array([int(train_context.game.coin.x+8)]),
        'coins_y': np.array([int(train_context.game.coin.y+8)]),
        't_x': np.array([train_context.game.tile.x]),
        't_y': np.array([train_context.game.tile.y]),
        't_type': np.array([train_context.game.tile.type])
    }
    # print("Received states:", train_context.states,train_context.observation_space, train_context.coin,train_context.tile)
    return train_context.states
    #     here use tile instead of t


@reward
def train_impl(train_context):
    # train_context.ball_y.append(train_context.game.ball.rect.y + 6)
    # train_context.dis_coin.append(abs(train_context.game.ball.rect.y + 6 - train_context.game.coin.y - 8))
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
        # print("+++++++++++10")
        reward += 5
        # return reward

    if train_context.game.terminated:
        train_context.score = 0
        # train_context.ball_y.clear()
        # print("tttttttttttterminated")
        reward -= 3
        # return reward
    # 0.

    # if train_context.game.ball.rect.x + 6<= CENTER[0]:
    #     reward+=10

    danger1=train_context.game.ball.rect.y<train_context.game.tile.y+10 and \
                    train_context.game.ball.rect.y+12>train_context.game.tile.y-10
    danger23=train_context.game.ball.rect.y < train_context.game.tile.y + 25 and \
                    train_context.game.ball.rect.y + 12 > train_context.game.tile.y - 25
    is_going_to_collide_tile1 = train_context.game.ball.rect.y<train_context.game.tile.y+10 and \
                    train_context.game.ball.rect.y+12>train_context.game.tile.y-10
    is_going_to_collide_tile23 = train_context.game.ball.rect.y < train_context.game.tile.y + 25 and \
                    train_context.game.ball.rect.y + 12 > train_context.game.tile.y - 25
    is_going_to_collide_coin = train_context.game.ball.rect.y < train_context.game.coin.y + 16 and \
                    train_context.game.ball.rect.y + 12 > train_context.game.coin.y
    is_above_tile_center = train_context.game.ball.rect.y + 6<=train_context.game.tile.y
    is_under_tile_center = train_context.game.ball.rect.y + 6>train_context.game.tile.y
    coin_on_the_right = train_context.game.ball.rect.x+12<train_context.game.coin.x
    tile13_on_the_right = train_context.game.ball.rect.x+12<train_context.game.tile.x-25
    tile2_on_the_right = train_context.game.ball.rect.x+12<train_context.game.tile.x-10
    coin_tile1_not_overlapped = train_context.game.coin.y<train_context.game.tile.y+10 and \
                    train_context.game.coin.y+16>train_context.game.tile.y-10
    coin_tile23_not_overlapped = train_context.game.coin.y<train_context.game.tile.y+25 and \
                    train_context.game.coin.y+16>train_context.game.tile.y-25
    # 1.若有tile
    # 1.1若ball的y与tile重叠，
    # 1.1.1若tile不超过上下沿则必须y向着远离tile改变
    # 1.1.2若tile超过上沿则向下移动，tile超过下沿则向上移动
    # 1.2若无重叠并且cointile不重叠并且顺序是ball.y coin.y tile.y
    # 1.2则ball.y，则ball.y必须向着coin.y改变
    # 2.若无tile，则ball.y必须向着coin.y改变

    if train_context.game.ball.rect.x + 6 - CENTER[0]>0:
        reward-=3
    else:
        reward+=3

    # # 1.若有tile
    if 32<train_context.game.tile.x<298 and not train_context.last_tilex == train_context.game.tile.x:
        # 1.1若ball的y与tile重叠，
        if tile13_on_the_right and train_context.game.tile.type==1 and is_going_to_collide_tile1:
            train_context.is_going_to_collide_tile.append(True)
            if train_context.game.tile.y-10<=CENTER[1]-70+6:#需要下移
                if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
                    reward+=3
                    correct_direction =True
                    # print("avoid1")
                elif train_context.game.ball.rect.x + 6 - CENTER[0]==0 and train_context.game.ball.dtheta<0:
                    reward += 3
                    correct_direction = True
                else:
                    reward -= 3

            elif train_context.game.tile.y+10<=CENTER[1]+70-6:#需要上移
                if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0 :
                    reward+=3
                    correct_direction = True
                    # print("avoid1")
                elif train_context.game.ball.rect.x + 6 - CENTER[0]==0 and train_context.game.ball.dtheta>0:
                    reward += 3
                    correct_direction = True
                else:
                    reward -= 3

            else:#必须y向着远离tile改变
                if is_above_tile_center:
                    if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0:
                        reward+=3
                        correct_direction = True
                        # print("avoid1")
                    else:
                        reward -= 3
                elif is_under_tile_center:
                    if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
                        reward+=3
                        correct_direction = True
                        # print("avoid1")
                    else:
                        reward -= 3
        elif tile2_on_the_right and train_context.game.tile.type==2 and is_going_to_collide_tile23:
            train_context.is_going_to_collide_tile.append(True)
            if train_context.game.tile.y-25<=CENTER[1]-70+6:#需要下移
                if  train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
                    reward+=3
                    correct_direction = True
                    # print("avoid2")
                elif train_context.game.ball.rect.x + 6 - CENTER[0]==0 and train_context.game.ball.dtheta<0:
                    reward += 3
                    correct_direction = True
                else:
                    reward -= 3
            elif train_context.game.tile.y+25<=CENTER[1]+70-6:#需要上移
                if  train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0:
                    reward+=3
                    correct_direction = True
                    # print("avoid2")
                elif train_context.game.ball.rect.x + 6 - CENTER[0]==0 and train_context.game.ball.dtheta>0:
                    reward += 3
                    correct_direction = True
                else:
                    reward -= 3
            else:#必须y向着远离tile改变
                if is_above_tile_center:
                    if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0:
                        reward+=3
                        correct_direction = True
                        # print("avoid2")
                    else:
                        reward -= 3
                elif is_under_tile_center :
                    if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
                        # print("avoid2")
                        reward+=3
                        correct_direction = True
                    else:
                        reward -= 3
        elif tile13_on_the_right and train_context.game.tile.type==3 and is_going_to_collide_tile23:
            train_context.is_going_to_collide_tile.append(True)
            if train_context.game.tile.y-25<=CENTER[1]-70+6:#需要下移
                if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
                    # print("avoid3")
                    reward+=3
                    correct_direction = True
                elif train_context.game.ball.rect.x + 6 - CENTER[0]==0 and train_context.game.ball.dtheta<0:
                    reward += 3
                    correct_direction = True
                else:
                    reward -= 3
            elif train_context.game.tile.y+25<=CENTER[1]+70-6:#需要上移
                if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0:
                    # print("avoid3")
                    reward+=3
                    correct_direction = True
                elif train_context.game.ball.rect.x + 6 - CENTER[0]==0 and train_context.game.ball.dtheta>0:
                    reward += 3
                    correct_direction = True
                else:
                    reward -= 3
            else:#必须y向着远离tile改变
                if is_above_tile_center :
                    if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0:
                        # print("avoid3")
                        reward+=3
                        correct_direction = True
                    else:
                        reward -= 3
                elif is_under_tile_center :
                    if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
                        # print("avoid3")
                        reward+=3
                        correct_direction = True
                    else:
                        reward -= 3
            if len(train_context.is_going_to_collide_tile) >= 2 and len(train_context.ball_dtheta) >= 2:
                last_collide = train_context.is_going_to_collide_tile[-1]
                second_last_collide = train_context.is_going_to_collide_tile[-2]
                last_dtheta = train_context.ball_dtheta[-1]
                second_last_dtheta = train_context.ball_dtheta[-2]
                if last_collide and second_last_collide:
                    if last_dtheta * second_last_dtheta > 0 and correct_direction:
                        reward += 3
                    else:  # has a wrong direction or changed to a wrong direction
                        reward -= 3
    #     # 1.2若无重叠并且cointile不重叠并且顺序是ball.y coin.y tile.y  并且在左半
    #     else:
    #         train_context.is_going_to_collide_tile.append(False)
    #         if coin_on_the_right and 58<train_context.game.coin.x<298 and not train_context.last_coinx == train_context.game.coin.x:
    #             if (train_context.game.tile.type==1 and coin_tile1_not_overlapped) or \
    #                     ((train_context.game.tile.type==2 or train_context.game.tile.type==3) and coin_tile23_not_overlapped):
    #                 if (train_context.game.tile.y-train_context.game.coin.y-8)*(train_context.game.coin.y+8-train_context.game.ball.rect.y-6)>0:
    #                     if is_above_tile_center:#需要下移
    #                         if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])>0:
    #                             if train_context.game.ball.rect.x + 6 - CENTER[0]<=0:
    #                                 reward += 2
    #                                 # correct_direction = True
    #                                 # print("to coin")
    #                             else:
    #                                 reward -= 2
    #                     elif is_under_tile_center:#需要上移
    #                         if train_context.game.ball.dtheta*(train_context.game.ball.rect.x + 6 - CENTER[0])<0:
    #                             if train_context.game.ball.rect.x + 6 - CENTER[0]<=0:
    #                                 reward += 2
    #                                 # correct_direction = True
    #                                 # print("to coin")
    #                             else:
    #                                 reward -= 2
    # else:#若无tile
    #     train_context.is_going_to_collide_tile.append(False)
    #     if coin_on_the_right and 58 < train_context.game.coin.x < 298 and not train_context.last_coinx == train_context.game.coin.x:
    #         if  (train_context.game.coin.y+8-train_context.game.ball.rect.y-6)>0:#coin.y>ball.y,then should move down
    #             if train_context.game.ball.dtheta * (train_context.game.ball.rect.x + 6 - CENTER[0]) > 0:
    #                 if train_context.game.ball.rect.x + 6 - CENTER[0] <= 0:
    #                     reward += 2
    #                     correct_direction = True
    #                     # print("to coin no tile")
    #                 else:
    #                     reward -= 2
    #         elif  (train_context.game.coin.y+8-train_context.game.ball.rect.y-6)<0:
    #             if train_context.game.ball.dtheta * (train_context.game.ball.rect.x + 6 - CENTER[0]) < 0:
    #                 if train_context.game.ball.rect.x + 6 - CENTER[0] <= 0:
    #                     reward += 2
    #                     correct_direction = True
    #                     # print("to coin no tile")
    #                 else:
    #                     reward -= 2


    #
    #
    # elif coin_on_the_right and 58<train_context.game.coin.x<298 and not train_context.last_coinx == train_context.game.coin.x: #there is a coin on the screen
    #     if is_going_to_collide_coin:
    #         print("+4")
    #         reward += 4
    #     # newly added
    #     else:
    #         if dis_coin < train_context.dis_coin:
    #             print("+4")
    #             reward += 4
    #
    # # else:  #is not going to collide with tiles
    # #
    # # if dis_coin<train_context.dis_coin and not train_context.last_coinx==train_context.coin.x:
    # #     reward += 1
    # #     train_context.dis_coin=dis_coin
    # #     train_context.last_coinx = train_context.coin.x
    # # else:
    # #     if
    #
    #
    #
    #
    # # if not train_context.game.terminated and train_context.game.score <= train_context.score:
    # #     # print("0.1")
    # #     reward += 1
    # train_context.dis_coin = dis_coin
    train_context.last_tilex = train_context.game.tile.x
    train_context.last_coinx = train_context.game.coin.x
    return reward


@terminated
def train_impl(train_context):
    term = train_context.game.terminated
    return train_context.game.terminated


@action
def train_impl(train_context, raw_actions):

    direction = ["nothing", "space"]
    train_context.actions = [direction[raw_actions]]
    return train_context.actions
