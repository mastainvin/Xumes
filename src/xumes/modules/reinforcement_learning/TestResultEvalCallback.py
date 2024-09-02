import numpy as np
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.results_plotter import load_results
import os


class CustomEvalCallback(EvalCallback):
    def __init__(self,
                 eval_env,
                 test_result_func_per_env,  # Function to test each env individually
                 log_dir,
                 best_model_save_path=None,
                 n_eval_episodes=5,
                 eval_freq=10000,
                 deterministic=True,
                 render=False,
                 tensorboard_writer=None):
        super(CustomEvalCallback, self).__init__(
            eval_env=eval_env,
            best_model_save_path=best_model_save_path,
            n_eval_episodes=n_eval_episodes,
            eval_freq=eval_freq,
            deterministic=deterministic,
            render=render)

        self.test_result_func_per_env = test_result_func_per_env
        self.tensorboard_writer = tensorboard_writer
        self.log_dir = log_dir
        self.eval_success = []
        self.last_success = 0

    def _on_step(self) -> bool:
        result = super(CustomEvalCallback, self)._on_step()
        if self.n_calls % self.eval_freq == 0:
            # Collect the test results for all environments
            successes = [self.test_result_func_per_env(env_idx) for env_idx in range(self.eval_env.num_envs)]
            mean_success = np.mean(successes)
            self.eval_success.append(mean_success)

            # Log the mean success rate to TensorBoard
            if self.tensorboard_writer is not None:
                log_name = "eval/mean_success_rate"
                print(f"Logging {log_name}: {mean_success} at step {self.num_timesteps}")  # Log information
                self.tensorboard_writer.add_scalar(log_name, mean_success, self.num_timesteps)
                self.tensorboard_writer.flush()  # Force the flush to ensure it gets written

            # Update the last success with the mean value
            self.last_success = mean_success

        return result

    def _on_training_end(self):
        # Optionally save the final evaluation success rates
        np.save(os.path.join(self.log_dir, 'eval_mean_success.npy'), self.eval_success)
