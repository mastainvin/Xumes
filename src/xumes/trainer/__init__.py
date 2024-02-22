from xumes.trainer.trainer_manager import observation, reward, action, config, terminated, StableBaselinesTrainerManager, VecStableBaselinesTrainerManager
from gymnasium.envs.registration import register

register(
    id="xumes-v0",
    entry_point="xumes.trainer.implementations.gym_impl.gym_envs.gym_env.gym_adapter_env.gym_adapter:GymAdapter",
)
