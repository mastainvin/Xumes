import gymnasium
from imitation.algorithms import bc

from xumes.modules.imitation_learning.imitation_learning_algorithm import ImitationLearningAlgorithm


class BC(ImitationLearningAlgorithm):
    """
    Behavior Cloning algorithm.
    """

    def execute(self, venv, gen_algo, rng, demonstrations, device):
        trainer = bc.BC(
            observation_space=venv.observation_space,
            action_space=venv.action_space,
            policy=gen_algo.policy,
            rng=rng,
            demonstrations=demonstrations,
            device=device,
        )

        trainer.train(n_epochs=self._n_epochs)
