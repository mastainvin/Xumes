import sys
from typing import List

import numpy as np
import stable_baselines3
from gymnasium import spaces

from games_examples.batkill.testing.training_side.entites.batkiller_entity_manager import BatKillerEntityManager
from games_examples.batkill.play import worldx, worldy, nb_bats
from xumes.training_module import StableBaselinesTrainer, CommunicationServiceTrainingMq, JsonGameElementStateConverter, \
    EntityManager


class BatKillerTrainingService(StableBaselinesTrainer):

    def __init__(self,
                 entity_manager: EntityManager,
                 communication_service,
                 observation_space,
                 action_space,
                 max_episode_length: int,
                 total_timesteps: int,
                 algorithm_type: str,
                 algorithm):
        super().__init__(entity_manager, communication_service, observation_space, action_space, max_episode_length,
                         total_timesteps, algorithm_type, algorithm)

        self.score = 0
        self.lives = 5
        self.actions = ["nothing" for _ in range(3)]

    def convert_obs(self):

        player = self.get_entity("player")

        dct = {
            'player_x': np.array([(player.position[0] / worldx) * 2 - 1]),
            'player_y': np.array([(player.position[1] / worldy) * 2 - 1]),
            'player_direction': np.array([player.direction]),
            'player_attack': np.array([(
                                     player.attack_state / player.attack_duration) * 2 - 1]),
            'player_cooldown': np.array([(
                                       player.cool_down_state / player.cool_down_duration) * 2 - 1])
        }
        for idx in range(nb_bats):
            try:
                bat = self.get_entity("bat_"+str(idx))
                is_dead = bat.dead
            except KeyError:
                is_dead = True
            if not is_dead:
                dct[f'bat_{idx}_alive'] = np.array([1])
                dct[f'bat_{idx}_direction'] = np.array([bat.direction])
                dct[f'bat_{idx}_x'] = np.array([(bat.position[0] / worldx) * 2 - 1])
                dct[f'bat_{idx}_speed'] = np.array([bat.speed])
                dct[f'bat_{idx}_distance_to_player'] = np.array([(bat.position[0] - player.position[0]) / worldx])
                if bat.direction == -1:
                    if bat.position[0] > player.position[0]:
                        bat_facing_player = 1
                    else:
                        bat_facing_player = -1
                else:
                    if bat.position[0] < player.position[0]:
                        bat_facing_player = 1
                    else:
                        bat_facing_player = -1
                if player.direction == -1:
                    if player.position[0] > bat.position[0]:
                        player_facing_bat = 1
                    else:
                        player_facing_bat = -1
                else:
                    if player.position[0] < bat.position[0]:
                        player_facing_bat = 1
                    else:
                        player_facing_bat = -1
                if player_facing_bat > 0:
                    attack_rect = player.attack_rect
                    if (
                            bat.collider_rect and
                            attack_rect and
                            player.cool_down_state == 0 and
                            player.attack_state == 0
                    ):
                        bat_in_range = 1
                    else:
                        bat_in_range = -1
                else:
                    bat_in_range = -1

                dct[f'bat_{idx}_bat_facing_player'] = np.array([bat_facing_player])
                dct[f'bat_{idx}_player_facing_bat'] = np.array([player_facing_bat])
                dct[f'bat_{idx}_in_attack_range'] = np.array([bat_in_range])
            else:
                dct[f'bat_{idx}_alive'] = np.array([-1])
                dct[f'bat_{idx}_direction'] = np.array([0])
                dct[f'bat_{idx}_x'] = np.array([-1])
                dct[f'bat_{idx}_speed'] = np.array([0])
                dct[f'bat_{idx}_distance_to_player'] = np.array([0])
                dct[f'bat_{idx}_bat_facing_player'] = np.array([0])
                dct[f'bat_{idx}_player_facing_bat'] = np.array([0])
                dct[f'bat_{idx}_in_attack_range'] = np.array([0])

        return dct

    def convert_terminated(self) -> bool:
        return self.game_state == "lose"

    def convert_actions(self, raws_actions) -> List[str]:
        direction = ["nothing", "left", "right"]
        position = ["nothing", "up"]
        attack = ["nothing", "space"]

        self.actions = [direction[raws_actions[0]], position[raws_actions[1]], attack[raws_actions[2]]]
        return self.actions

    def convert_reward(self):

        player = self.get_entity("player")

        reward = 0

        #if "space" in self.actions:
        #    reward -= 0.1
        if "up" in self.actions:
            reward -= 0.2
        if "space" in self.actions and player.score == self.score:
            reward -= 0.1

        if player.score != self.score:
            reward += 5
            self.score = player.score
        if player.lives != self.lives:
            reward -= 7
            self.lives = player.lives

        if player.facing_nearest_bat is True:
            reward += 0.2

        #FIX ME
        for i in range(nb_bats):
            try:
                bat = self.get_entity("bat_"+str(i))
                existed_bat = True
            except KeyError:
                existed_bat = False
            if existed_bat:
                if bat.direction == -1:
                    if bat.position[0] < player.position[0]:
                        reward += 0.1
                else:
                    if bat.position[0] > player.position[0]:
                        reward += 0.1

        return reward


if __name__ == "__main__":

    dct = {'player_x': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
           'player_y': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
           'player_direction': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
           'player_attack': spaces.Box(-1, 1, dtype=np.float32, shape=(1,)),
           'player_cooldown': spaces.Box(-1, 1, dtype=np.float32, shape=(1,))
           }
    for idx in range(nb_bats):
        dct[f'bat_{idx}_alive'] = spaces.Box(-1, 1, dtype=np.int16, shape=(1,))
        dct[f'bat_{idx}_direction'] = spaces.Box(-1, 1, dtype=np.int16, shape=(1,))
        dct[f'bat_{idx}_x'] = spaces.Box(-1, 1, shape=(1,))
        dct[f'bat_{idx}_speed'] = spaces.Box(0, 100, shape=(1,))
        dct[f'bat_{idx}_distance_to_player'] = spaces.Box(-1, 1, shape=(1,))
        dct[f'bat_{idx}_bat_facing_player'] = spaces.Box(-1, 1, shape=(1,))
        dct[f'bat_{idx}_player_facing_bat'] = spaces.Box(-1, 1, shape=(1,))
        dct[f'bat_{idx}_in_attack_range'] = spaces.Box(-1, 1, shape=(1,))

    training_service = BatKillerTrainingService(
        entity_manager=BatKillerEntityManager(
            JsonGameElementStateConverter()
        ),
        communication_service=CommunicationServiceTrainingMq(),
        observation_space=spaces.Dict(dct),
        action_space=spaces.MultiDiscrete([3, 2, 2]),
        max_episode_length=20000,
        total_timesteps=1000000,
        algorithm_type="MultiInputPolicy",
        algorithm=stable_baselines3.PPO
    )

    if len(sys.argv) == 2:
        if sys.argv[1] == "-train":
            training_service.train()
            training_service.save("./models/model")
        elif sys.argv[1] == "-play":
            training_service.load("./models/model")
            training_service.play(100000)
