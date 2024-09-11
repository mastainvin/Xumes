import logging
import os
from typing import Optional, List

from stable_baselines3.common.callbacks import EvalCallback, CallbackList
from stable_baselines3.common.vec_env import DummyVecEnv, VecEnvWrapper
from stable_baselines3.common.logger import configure
from torch.utils.tensorboard import SummaryWriter

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.modules.reinforcement_learning.success_ratio_callback import SuccessRatioCallback
from xumes.modules.reinforcement_learning.i_trainer import ITrainer
from xumes.modules.reinforcement_learning.stable_baselines_trainer import StableBaselinesTrainer


def find_path(path: str, name: str) -> str:
    counter = 1
    base_name = f"{name}_{counter}"
    full_path = os.path.join(path, base_name)

    while os.path.exists(full_path):
        counter += 1
        base_name = f"{name}_{counter}"
        full_path = os.path.join(path, base_name)

    return full_path


class VecStableBaselinesTrainer(ITrainer):

    def __init__(self):
        self._vec_env = None
        self._trainers: List[StableBaselinesTrainer] = []
        self._envs = []
        self._first_trainer = None
        self.policy = None
        self._made = False

    def add_trainer(self, trainer: StableBaselinesTrainer):
        self._trainers.append(trainer)
        if self._first_trainer is None:
            self._first_trainer = trainer
        self._envs.append(lambda: trainer.env)

    @property
    def venv(self):
        return self._vec_env

    def make(self):
        self._made = True
        self._vec_env = DummyVecEnv(self._envs)

    def train(self, save_path: str = None, eval_freq: int = 10000, logs_path: Optional[str] = None,
              logs_name: Optional[str] = None, previous_model_path: Optional[str] = None):

        if self._first_trainer is None:
            raise Exception("No training services added")

        if not self._made:
            self.make()

        policy_class = self._first_trainer.policy_class
        algorithm_type = self._first_trainer.algorithm_type
        total_timesteps = self._first_trainer.total_timesteps

        # Configure the logs path
        if logs_path and logs_name:
            logs_path = find_path(logs_path, logs_name)

        # Initialize the algorithm with TensorBoard logging
        self.make_algo(logs_path=logs_path)

        if previous_model_path:
            self.policy = self.policy.load(previous_model_path, env=self._vec_env)

        # Set up the logger if logs_path is provided
        if logs_path:
            main_logger = configure(folder=logs_path, format_strings=["stdout", "tensorboard"])
            self.policy.set_logger(main_logger)

        # Define the evaluation callback
        eval_callback = None
        if save_path:
            eval_callback = EvalCallback(
                self._vec_env,
                best_model_save_path=save_path,
                log_path=logs_path,
                eval_freq=eval_freq,
                deterministic=True,
                render=False
            )

        # Define the success ratio callback
        success_rate_callback = None
        if logs_path:
            eval_logs_path = os.path.join(logs_path, "success_rate")
            os.makedirs(eval_logs_path, exist_ok=True)

            def success_ratio_and_reset(env_idx):
                rate = self._trainers[env_idx].agent.test_runner.success_ratio()
                self._trainers[env_idx].agent.test_runner.reset_ratio()
                return rate

            success_rate_callback = SuccessRatioCallback(
                eval_env=self._vec_env,
                test_result_func_per_env=success_ratio_and_reset,
                log_dir=eval_logs_path,
                eval_freq=eval_freq,
                tensorboard_writer=SummaryWriter(log_dir=eval_logs_path)
            )

        # Combine callbacks
        combined_callback = CallbackList([cb for cb in [eval_callback, success_rate_callback] if cb is not None])

        # Start training
        self.policy = self.policy.learn(total_timesteps, callback=combined_callback)

    def save(self, path: str):
        self.policy.save(path)

    def free(self):
        if self._vec_env is not None:
            self._vec_env.close()
            self.policy = None

    def load(self, path: str):
        if self._first_trainer is None:
            raise Exception("No training services added")

        if not self._made:
            self.make()

        self.make_algo()
        self.policy = self.policy.load(path, env=self._vec_env)

    def make_algo(self, logs_path: Optional[str] = None):
        if self._first_trainer is None:
            raise Exception("No training services added")

        if not self._made:
            self.make()

        policy_class = self._first_trainer.policy_class
        algorithm_type = self._first_trainer.algorithm_type
        policy_kwargs = self._first_trainer.policy_kwargs if self._first_trainer.policy_kwargs else {}

        self.policy = policy_class(algorithm_type, self._vec_env, verbose=1, tensorboard_log=logs_path,
                                   policy_kwargs=policy_kwargs)


    def play(self, timesteps: int = None):

        class InferenceWrapper(VecEnvWrapper):
            def __init__(self, env):
                super(InferenceWrapper, self).__init__(env)
                self.training = False

            def reset(self):
                return self.venv.reset()

            def step_async(self, a):
                self.venv.step_async(a)

            def step_wait(self):
                return self.venv.step_wait()

        _envs = InferenceWrapper(self._vec_env)
        obs = _envs.reset()

        active_envs = [True] * len(self._envs)

        def step():
            nonlocal obs
            actions, _ = self.policy.predict(obs)
            for i in range(len(next(iter(obs.values())))):
                if active_envs[i]:
                    try:
                        single_action = actions[i]
                        single_obs, rewards, done, terminated, info = _envs.envs[i].step(single_action)

                        # Update obs
                        for key, val in single_obs.items():
                            obs[key][i] = val

                        if done or terminated:
                            _envs.envs[i].reset()
                    except RunningEndsError:
                        logging.info(f"Received stop signal for environment {i}. Closing environment.")
                        active_envs[i] = False
                        _envs.envs[i].close()

        if not timesteps:
            while any(active_envs):
                step()
        else:
            for _ in range(timesteps):
                step()

