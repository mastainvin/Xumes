import logging
from abc import abstractmethod
from typing import List

from xumes import Input


class HasContext:

    @property
    def context(self):
        raise NotImplementedError


class TestStep(HasContext):

    def __init__(self) -> None:
        self._has_context = None

    @property
    def context(self):
        return self._has_context.context

    def set_has_context(self, has_context: HasContext) -> None:
        self._has_context = has_context

    @abstractmethod
    def step(self) -> List[Input]:
        """
        Method executed at each game frame.

        :return: A list of `Input` objects.
        """
        raise NotImplementedError

    @abstractmethod
    def is_complete(self) -> bool:
        """
        Defines if the step is finished or not.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        In the case a reset is needed for the future use of this step.
        """
        raise NotImplementedError


class GivenScript(HasContext):

    def __init__(self, test_runner):
        super().__init__()
        self._steps: List[TestStep] = []
        self._current_step_index = 0
        self._current_step = None
        self._test_runner = test_runner

    @property
    def context(self):
        return self._test_runner.get_context()

    def execute(self):
        while not self.terminated():
            self._test_runner.push_action_and_get_state(self.step())

    def step(self) -> List[Input]:
        if self._current_step_index >= len(self._steps):
            return []

        current_state = self._steps[self._current_step_index]
        actions = current_state.step()

        if current_state.is_complete():
            self._current_step_index += 1

        return actions

    def add_step(self, step):
        step.set_has_context(self)
        self._steps.append(step)
        if not self._current_step:
            self._current_step = step

    def reset(self):
        self._current_step_index = 0
        for step in self._steps:
            step.reset()

    def clean(self):
        self._steps.clear()
        self._current_step_index = 0
        self._current_step = None

    def terminated(self) -> bool:
        return self._current_step_index >= len(self._steps)


class SequentialStep(TestStep):
    """
    Executes a series of sub-steps sequentially, moving to the next step once the current one is complete.

    Attributes:
        - states (List[TestStep]): A list of TestStep objects to be executed in sequence.
    """
    def __init__(self, states: List[TestStep]):
        super().__init__()
        self.states = states
        for step in states:
            step.set_has_context(self)
        self.current_state_index = 0

    def step(self) -> List[Input]:

        current_state = self.states[self.current_state_index]
        actions = current_state.step()

        if current_state.is_complete():
            self.current_state_index += 1

        return actions

    def is_complete(self) -> bool:
        if self.current_state_index >= len(self.states):
            self.current_state_index = 0
            return True
        return False

    def reset(self):
        self.current_state_index = 0
        for step in self.states:
            step.reset()


class DelayStep(TestStep):
    """
    Introduces a delay before allowing another step to execute. Waits for a specified number of cycles before proceeding.

    Attributes:
        - state (TestStep): The step to be executed after the delay.
        - delay (int): The number of cycles to wait before the state can proceed.
    """
    def __init__(self, state: TestStep, delay: int):
        super().__init__()
        self.state = state
        self.state.set_has_context(self)
        self.initial_delay = delay
        self.delay = delay

    def step(self) -> List[Input]:
        if self.delay > 0:
            self.delay -= 1
            return []

        return self.state.step()

    def is_complete(self) -> bool:
        if self.delay > 0:
            return False
        return self.state.is_complete()

    def reset(self):
        self.delay = self.initial_delay
        self.state.reset()


class CombinedStep(TestStep):
    """
    Executes multiple sub-steps in parallel, combining their actions each cycle. The step completes when all sub-steps are finished.

    Attributes:
        - states (List[TestStep]): A list of TestStep objects to be executed in parallel.
    """
    def __init__(self, states: List[TestStep]):
        super().__init__()
        self.states = states
        for step in self.states:
            step.set_has_context(self)

    def step(self) -> List[Input]:
        inputs = []
        for state in self.states:
            inputs.extend(state.step())
        return inputs

    def is_complete(self) -> bool:
        return all(state.is_complete() for state in self.states)

    def reset(self):
        for state in self.states:
            state.reset()


class WaitStep(TestStep):
    """
    Passively waits for a defined number of cycles before marking the step as complete.

    Attributes:
        - wait_time (int): The number of cycles to wait before completion.
    """
    def __init__(self, wait_time):
        super().__init__()
        self.initial_wait_time = wait_time
        self.wait_time = wait_time
        self.elapsed_time = 0

    def step(self) -> List[Input]:
        self.elapsed_time += 1
        return []

    def is_complete(self) -> bool:
        return self.elapsed_time >= self.wait_time

    def reset(self):
        self.elapsed_time = 0
        self.wait_time = self.initial_wait_time


class WaitUntilStep(WaitStep):
    """
    Waits until a custom condition (wait_function) is met or a timeout occurs.

    Attributes:
        - wait_function (Callable): A function that returns True when the condition is met.
        - timeout (int): The maximum number of cycles to wait before timing out.
    """
    def __init__(self, wait_function, timeout):
        super().__init__(timeout)
        self.is_completed = False
        self.wait_function = wait_function

    def is_complete(self) -> bool:
        if not self.is_completed:
            self.is_completed = self.wait_function()

        return super().is_complete() or self.is_completed

    def reset(self):
        super().reset()


class RepeatStep(TestStep):
    """
    Repeats a given step a specified number of times before marking it as complete.

    Attributes:
        - step (TestStep): The step to be repeated.
        - times (int): The number of times to repeat the step.
    """
    def __init__(self, step: TestStep, times: int):
        super().__init__()
        self.step_object = step
        self.step_object.set_has_context(self)
        self.times = times
        self.current_time = 0

    def step(self) -> List[Input]:
        if self.current_time < self.times:
            self.current_time += 1
            return self.step_object.step()
        return []

    def is_complete(self) -> bool:
        return self.current_time >= self.times

    def reset(self):
        self.current_time = 0
        self.step_object.reset()


class RepeatUntilStep(WaitUntilStep):
    """
    Repeats a step until a custom condition is met or a timeout occurs, while executing wait logic.

    Attributes:
        - step (TestStep): The step to be repeated.
        - wait_function (Callable): A function that returns True when the condition is met.
        - timeout (int): The maximum number of cycles to wait before timing out.
    """
    def __init__(self, step: TestStep, wait_function, timeout):
        super().__init__(wait_function, timeout)
        self.step_object = step
        self.step_object.set_has_context(self)

    def step(self) -> List[Input]:
        actions = super().step()
        actions.extend(self.step_object.step())
        return actions

    def reset(self):
        super().reset()
        self.step_object.reset()

class LogStep(TestStep):
    """
    Logs a message at each step and then immediately completes. Used for logging actions.

    Attributes:
        - log (str): The message to log at each step.
    """
    def __init__(self, log):
        super().__init__()
        self.log = log

    def step(self) -> List[Input]:
        logging.info(self.log)
        return []

    def is_complete(self) -> bool:
        return True

    def reset(self):
        pass
