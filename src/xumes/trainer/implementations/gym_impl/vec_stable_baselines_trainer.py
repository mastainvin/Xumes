import logging
from typing import Optional, List

from stable_baselines3.common.callbacks import EvalCallback
# noinspection PyUnresolvedReferences
from stable_baselines3.common.vec_env import SubprocVecEnv, DummyVecEnv, VecEnvWrapper

from xumes.core.errors.running_ends_error import RunningEndsError
from xumes.trainer.i_trainer import ITrainer
from xumes.trainer.training_service import MarkovTrainingService


class VecStableBaselinesTrainer(ITrainer):

    def __init__(self):
        self._vec_env = None
        self._markov_training_services: List[MarkovTrainingService] = []
        self._envs = []
        self._first_training_service = None
        self.model = None

    def add_training_service(self, training_service):
        self._markov_training_services.append(training_service)
        if self._first_training_service is None:
            self._first_training_service = training_service
        self._envs.append(lambda: training_service.env)

    def make(self):
        self._vec_env = DummyVecEnv(self._envs)

    def train(self, save_path: str = None, eval_freq: int = 10000, logs_path: Optional[str] = None,
              logs_name: Optional[str] = None, previous_model_path: Optional[str] = None):
        if self._first_training_service is None:
            raise Exception("No training services added")

        if self._vec_env is None:
            self.make()

        algorithm = self._first_training_service.algorithm
        algorithm_type = self._first_training_service.algorithm_type
        total_timesteps = self._first_training_service.total_timesteps

        eval_callback = None
        if save_path:
            eval_callback = EvalCallback(self._vec_env, best_model_save_path=save_path,
                                         log_path=save_path, eval_freq=eval_freq,
                                         deterministic=True, render=False)

        if previous_model_path:
            self.model = algorithm(algorithm_type, self._vec_env, verbose=1, tensorboard_log=logs_path).load(
                previous_model_path, env=self._vec_env).learn(
                total_timesteps,
                callback=eval_callback,
                tb_log_name=logs_name
            )
        else:
            self.model = algorithm(algorithm_type, self._vec_env, verbose=1, tensorboard_log=logs_path).learn(
                total_timesteps,
                callback=eval_callback,
                tb_log_name=logs_name
            )

        for training_service in self._markov_training_services:
            training_service.finished()

    def save(self, path: str):
        self.model.save(path)

    def load(self, path: str):
        if self._first_training_service is None:
            raise Exception("No training services added")

        if self._vec_env is None:
            self.make()

        algorithm = self._first_training_service.algorithm
        algorithm_type = self._first_training_service.algorithm_type

        self.model = algorithm(algorithm_type, self._vec_env, verbose=1).load(path, env=self._vec_env)

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
            actions, _ = self.model.predict(obs)
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
            while True:
                step()
        else:
            for _ in range(timesteps):
                step()
