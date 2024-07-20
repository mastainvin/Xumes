from abc import abstractmethod


class ImitationLearningAlgorithm:
    """
    Base class for imitation learning algorithms.
    Made to be used in the Imitator class.
    Implements algorithm from the imitation library.
    """

    def __init__(self, n_epochs=20):
        self._n_epochs = n_epochs

    @abstractmethod
    def execute(self,
                venv,
                gen_algo,
                rng,
                demonstrations,
                device):
        """
        Execute the imitation learning algorithm.
        Args:
            venv: The environment.
            gen_algo: The generator algorithm.
            rng: The random number generator.
            demonstrations: The demonstrations.
            device: The device to be used.
        """
        pass
