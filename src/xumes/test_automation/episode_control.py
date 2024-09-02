from abc import abstractmethod, ABC


class EpisodeControl(ABC):
    """
    Abstract base class for episode control. An episode control is responsible for managing the continuation of an episode.

    :param max_steps: The maximum number of steps in an episode.
    :param max_tests: The maximum number of tests in an episode.
    """

    def __init__(self, max_steps=None, max_tests=None):
        self.current_step = 0
        self.current_test = 0
        self.max_steps = max_steps
        self.max_tests = max_tests

    def increment_test(self):
        self.current_test += 1

    def increment_step(self):
        self.current_step += 1

    @abstractmethod
    def should_continue(self, test_result: bool):
        """Abstract method to determine if the episode should continue."""
        raise NotImplementedError()


class DefaultEpisodeControl(EpisodeControl):
    """
    Default implementation of EpisodeControl. The episode continues until the maximum number of steps or tests is reached.
    """

    def should_continue(self, test_result: bool):
        """
        Determines if the episode should continue. The episode continues until the maximum number of steps or tests is reached.

        :return: True if the episode should continue, False otherwise.
        """
        if test_result:
            return False

        if self.max_tests is not None and self.current_test >= self.max_tests:
            return False
        if self.max_steps is not None and self.current_step >= self.max_steps:
            return False
        return True


class UserControlledEpisodeControl(EpisodeControl):
    """
    User-controlled implementation of EpisodeControl. The user can manually stop and resume the episode.

    :param max_steps: The maximum number of steps in an episode.
    :param max_tests: The maximum number of tests in an episode.
    """

    def __init__(self, max_steps=None, max_tests=None):
        super().__init__(max_steps, max_tests)
        self.is_running = True

    def stop(self):
        """Stops the episode."""
        self.is_running = False

    def resume(self):
        """Resumes the episode."""
        self.is_running = True

    def decrement_test(self):
        """Decrements the current test count by 1."""
        self.current_test -= 1

    def decrement_step(self):
        """Decrements the current step count by 1."""
        self.current_step -= 1

    def should_continue(self, test_result: bool):
        """
        Determines if the episode should continue. The episode continues until the user stops it or the maximum number of steps or tests is reached.

        :return: True if the episode should continue, False otherwise.
        """
        if not self.is_running:
            return False
        if self.max_tests is not None and self.current_test >= self.max_tests:
            return False
        if self.max_steps is not None and self.current_step >= self.max_steps:
            return False
        return True


class EpisodeControlFactory(ABC):
    """
    Abstract base class for episode control factory. An episode control factory is responsible for creating episode controls.
    """

    @staticmethod
    @abstractmethod
    def create(max_steps=None, max_tests=None):
        """Abstract method to create an episode control."""
        raise NotImplementedError()


class DefaultEpisodeControlFactory(EpisodeControlFactory):
    """
    Factory for creating DefaultEpisodeControl instances.
    """

    @staticmethod
    def create(max_steps=None, max_tests=None):
        """
        Creates a DefaultEpisodeControl.

        :param max_steps: The maximum number of steps in an episode.
        :param max_tests: The maximum number of tests in an episode.
        :return: A DefaultEpisodeControl instance.
        """
        return DefaultEpisodeControl(max_steps, max_tests)


class UserControlledEpisodeControlFactory(EpisodeControlFactory):
    """
    Factory for creating UserControlledEpisodeControl instances.
    """

    @staticmethod
    def create(max_steps=None, max_tests=None):
        """
        Creates a UserControlledEpisodeControl.

        :param max_steps: The maximum number of steps in an episode.
        :param max_tests: The maximum number of tests in an episode.
        :return: A UserControlledEpisodeControl instance.
        """
        return UserControlledEpisodeControl(max_steps, max_tests)
