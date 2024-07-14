from imitation.algorithms.adversarial import gail
from imitation.rewards.reward_nets import BasicShapedRewardNet
from imitation.util.networks import RunningNorm
from xumes.modules.imitation_learning.imitation_learning_algorithm import ImitationLearningAlgorithm


class GAIL(ImitationLearningAlgorithm):

    def __init__(self, total_time_steps: int):
        super().__init__()
        self._total_time_steps = total_time_steps

    def execute(self, venv, gen_algo, rng, demonstrations, device):
        reward_net = BasicShapedRewardNet(
            observation_space=venv.observation_space,
            action_space=venv.action_space,
            normalize_input_layer=RunningNorm,
        )

        trainer = gail.GAIL(
            reward_net=reward_net,
            venv=venv,
            demo_batch_size=32,
            gen_algo=gen_algo,
            demonstrations=demonstrations,
        )

        trainer.train(total_timesteps=self._total_time_steps)
