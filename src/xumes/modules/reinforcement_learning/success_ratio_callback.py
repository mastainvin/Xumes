import numpy as np
from stable_baselines3.common.callbacks import EvalCallback, BaseCallback
import os


class SuccessRatioCallback(BaseCallback):
    def _on_step(self) -> bool:
        return True

    def __init__(self,
                 eval_env,
                 test_result_func_per_env,  # Function to test each env individually
                 log_dir,
                 n_eval_episodes=5,
                 eval_freq=10000,
                 tensorboard_writer=None):
        super(SuccessRatioCallback, self).__init__()

        self.eval_env = eval_env
        self.eval_freq = eval_freq
        self.test_result_func_per_env = test_result_func_per_env
        self.tensorboard_writer = tensorboard_writer
        self.log_dir = log_dir
        self.eval_success = []

    def _on_rollout_end(self):
        super(SuccessRatioCallback, self)._on_rollout_end()

        # Collect the test results for all environments
        success_ratios = [self.test_result_func_per_env(env_idx) for env_idx in range(self.eval_env.num_envs)]
        sum_success = np.sum(success_ratios)
        print(success_ratios, sum_success)
        self.eval_success.append(sum_success)

        # Log the sum success rate to TensorBoard
        if self.tensorboard_writer is not None:
            log_name = "rollout/sum_success_rate"
            print(f"Logging {log_name}: {sum_success} at step {self.num_timesteps}")  # Log information
            self.tensorboard_writer.add_scalar(log_name, sum_success, self.num_timesteps)
            self.tensorboard_writer.flush()  # Force the flush to ensure it gets written

    def _on_training_end(self):
        # Optionally save the final evaluation success rates
        np.save(os.path.join(self.log_dir, 'eval_mean_success.npy'), self.eval_success)