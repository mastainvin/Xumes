import logging
import sys
from typing import List
import random
import numpy as np
import stable_baselines3
from gymnasium import spaces

from src.xumes.training_module import StableBaselinesTrainer, JsonGameElementStateConverter, \
                                        CommunicationServiceTrainingMq, AutoEntityManager

cell_size = 30
cell_number = 15
class SnakeTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager,
                 communication_service,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm, random_reset_rate):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm, random_reset_rate)

        self.score = 0
        self.distance=100
        self.actions = ["nothing", "nothing"]

    def convert_obs(self) :
        return {
            "fruit_above_snake": np.array([1 if self.snake.body[1] > self.fruit.pos[1] else 0]),
            "fruit_right_snake": np.array([1 if self.snake.body[0] < self.fruit.pos[0] else 0]),
            "fruit_below_snake": np.array([1 if self.snake.body[1] < self.fruit.pos[1] else 0]),
            "fruit_left_snake": np.array([1 if self.snake.body[0] > self.fruit.pos[0] else 0]),
            "obstacle_above": np.array(
                [1 if self.snake.body[1] - 1 == 0 or (self.snake.body[0], self.snake.body[1] - 1) in self.snake.body else 0]),
            "obstacle_right": np.array(
                [1 if self.snake.body[0] + 1 == cell_number or (self.snake.body[0] + 1, self.snake.body[1]) in self.snake.body else 0]),
            "obstacle_bellow": np.array(
                [1 if self.snake.body[1] + 1 == cell_number or (self.snake.body[0], self.snake.body[1] + 1) in self.snake.body else 0]),
            "obstacle_left": np.array(
                [1 if self.snake.body[0] - 1 == 0 or (self.snake.body[0] - 1, self.snake.body[1]) in self.snake.body else 0]),
            "direction_up": np.array([1 if self.snake.direction == (0, -1) else 0]),
            "direction_right": np.array([1 if self.snake.direction == (1, 0) else 0]),
            "direction_down": np.array([1 if self.snake.direction == (0, 1) else 0]),
            "direction_left": np.array([1 if self.snake.direction == (-1, 0) else 0]),
        }
    def convert_reward(self) -> float:
        close_reward = 0

        distance = np.abs(self.fruit.pos[0] - self.snake.body[0]) + np.abs(self.fruit.pos[1] - self.snake.body[1])
        # print(self.distance, distance,"dis")
        # 蛇头与水果同行同列
        # If the head of the snake is in the same line( col or row)
        # 如果蛇头与水果同行或同列
        if np.abs(self.fruit.pos[0] - self.snake.body[0]) * np.abs(self.fruit.pos[1] - self.snake.body[1]) ==0:

            # If any body block of the snake is in the same col with both the head and the fruit
            # and The direction of the snake is not the opposite direction of "head ---> fruit".
            # 如果蛇身在蛇头和水果的同列，并且蛇的方向不是蛇头指向水果的方向的反方向
            if(np.abs(self.fruit.pos[0] - self.snake.body[0])==0) and ((self.fruit.pos[1] - self.snake.body[1])*self.snake.direction[1])>=0:

                c1=0
                c2=0
                # for index, element in enumerate(self.snake.body):
                #     if element != 0 and element % 2 == 0:
                #         # 取得蛇身的x坐标（左右坐标）
                #         if element - self.fruit.pos[0]==0:
                #             # 如果这个蛇身块与水果在同一列
                #             c1+=1
                # getting x coordinates for every body block
                # 取得蛇身的x坐标（左右坐标）
                for index, element in enumerate(self.snake.body):
                    if index != 0 and index % 2 == 0:

                        # If this exact body block is in the same col with the fruit
                        # 如果这个蛇身块与水果在同一列
                        if element - self.fruit.pos[0] == 0:

                            c1 += 1
                            # If this body block lays between the head and the fruit, c2+=1
                            # 如果蛇身在蛇头和水果的同列，并且蛇身在蛇头和水果中间
                            if (self.snake.body[index+1] - self.fruit.pos[1])*(self.snake.body[index+1] - self.snake.body[1])<=0:

                                c2+=1
                if c2==0: # 所有蛇身都不在蛇头和水果中间 if all body blocks are not in the middle of head and fruit
                    close_reward+=10
                    if (self.fruit.pos[1] - self.snake.body[1])*self.snake.direction[1]>0:
                        #如果蛇还是朝着水果前进的 If the snake is moving forward to the fruit
                        close_reward+=30

            # same logic, but for the condition that
            # the snake is in the same row ( not the same col ) with both the head and the fruit

            # # If any body block of the snake is in the same row with both the head and the fruit
            # # and The direction of the snake is not the opposite direction of "head ---> fruit".
            # 如果蛇身在蛇头和水果的同行，并且蛇的方向不是蛇头指向水果的方向的反方向
            elif (np.abs(self.fruit.pos[1] - self.snake.body[1]) == 0) and  (
                    (self.fruit.pos[0] - self.snake.body[0]) * self.snake.direction[0]) >= 0:

                c1 = 0
                c2 = 0
                # getting y coordinates for every body block
                # 取得蛇身的y坐标（上下坐标）
                for index, element in enumerate(self.snake.body):
                    if index != 1 and index % 2 == 1:
                        # If this exact body block is in the same row to the fruit
                        # 如果这个蛇身块与水果在同一行
                        if element - self.fruit.pos[1] == 0:

                            c1 += 1
                            if (self.snake.body[index - 1] - self.fruit.pos[0]) * (
                                    self.snake.body[index - 1] - self.snake.body[0]) <= 0:
                                # If this body block lays between the head and the fruit, c2+=1
                                # 如果蛇身在蛇头和水果的同行，并且蛇身在蛇头和水果中间
                                c2 += 1
                if c2 == 0:  # 所有蛇身都不在蛇头和水果中间 if all body blocks are not in the middle of head and fruit
                    close_reward += 10
                    if (self.fruit.pos[0] - self.snake.body[0]) * self.snake.direction[0] > 0:
                        # 如果蛇还是朝着水果前进的 If the snake is moving forward to the fruit
                        close_reward += 30


        # check_fail
        # the head of the snake is not in the game field(from 0 to cell_number-1 for both dimensions)
        if not 0 <= self.snake.body[0]< cell_number or not 0 <= self.snake.body[1] < cell_number:
            close_reward -= 30
        # if the head bump into any body block
        else:
            # getting all y coordinates for body blocks
            for indexy, elementy in enumerate(self.snake.body):
                if indexy != 1 and indexy % 2 == 1:
                    # if a body clock has the same coordinates with the head
                    if elementy == self.snake.body[1] and self.snake.body[indexy-1] == self.snake.body[0]:
                        close_reward -= 30
                        break  # 跳出循环 jump out of the loop

        # 离边界非常近，则给予-10
        # if the head is going to bump into the wall after the next move, reward-=10
        if (self.snake.body[0] < 1 and self.snake.direction[0]==-1) or \
                (self.snake.body[1] < 1 and self.snake.direction[1]==-1) or \
                (self.snake.body[0]>cell_number-2 and self.snake.direction[0]==1) or \
                (self.snake.body[1] > cell_number - 2 and self.snake.direction[1] == 1):
            close_reward -= 10
        # if the head is going to bump into a body block
        else:
            # getting all y coordinates for body blocks
            for indexy, elementy in enumerate(self.snake.body):
                if indexy != 1 and indexy % 2 == 1:
                    # if a body clock has the same coordinates with the head
                    if elementy==self.snake.body[1]+self.snake.direction[1] and self.snake.body[indexy-1]==self.snake.body[0]+self.snake.direction[0]:
                        close_reward -= 10
                        break  # jump out of the loop



        # check_ate(collision):
        # if head has the same coordinates with fruit
        if (self.fruit.pos[0] == self.snake.body[0] and self.fruit.pos[1]==self.snake.body[1]) or \
                self.fruit.pos[0] == self.snake.body[0] +self.snake.direction[0] \
                and self.fruit.pos[1] == self.snake.body[1]  +self.snake.direction[1] :
            close_reward += 80

        # if the snake is moving towards the fruit
        if distance < self.distance:
            close_reward += 5
            self.distance=distance
        #
        elif distance > self.distance:
            close_reward += -1
            self.distance = distance

        else:
            close_reward += 0
            self.distance = distance

        self.distance = distance
        print("reward:",close_reward)
        return close_reward

    def convert_terminated(self) -> bool:
        return self.game.terminated

    def convert_actions(self, raws_actions) -> List[str]:
        # n=random.randint(1,6)
        # if n==1:
        #     direction  = ["nothing", "up", "left"]
        # elif n==2:
        #     direction  = ["nothing", "down", "right"]
        # elif n==3:
        #     direction  = ["nothing", "up", "right"]
        # elif n==4:
        #     direction  = ["nothing", "up", "down"]
        # elif n==5:
        #     direction  = ["nothing", "down", "left"]
        # elif n==6:
        #     direction  = ["nothing", "left", "right"]
        # n=random.randint(1,2)
        if self.snake.direction[0]==0:
            direction = ["nothing", "left", "right"]
        elif self.snake.direction[1]==0:
            direction= ["nothing", "up", "down"]
        self.actions = [direction[raws_actions[0]]]
        return self.actions


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        elif sys.argv[1] == "-play":
            logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

        dct = {
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
            "direction_left": spaces.Box(0, 1, shape=(1,), dtype=int),
        }
    training_service = SnakeTrainingService(
        entity_manager=AutoEntityManager(JsonGameElementStateConverter()),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(dct),
        action_space=spaces.MultiDiscrete([3, 3]),
        max_episode_length=2000,
        total_timesteps=100000,
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO,
        random_reset_rate=0.0
    )

    if len(sys.argv) > 1:
        if sys.argv[1] == "-train":
            training_service.load("./models/model1")
            training_service.train(save_path="./models", log_path="./logs", test_name="test")
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model.zip")
            training_service.play(100000)
